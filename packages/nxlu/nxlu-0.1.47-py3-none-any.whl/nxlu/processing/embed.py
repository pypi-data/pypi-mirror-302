import gc
import logging
import warnings
from collections import defaultdict
from pathlib import Path
from typing import Any

import faiss
import networkx as nx
import numpy as np
import torch
from huggingface_hub import PyTorchModelHubMixin
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import (
    quantize_embeddings,
    semantic_search_faiss,
)
from torch import nn
from transformers import AutoModel

from nxlu.processing.preprocess import create_subgraph, lcc

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

__all__ = ["CustomModel", "QuerySubgraph"]

faiss.omp_set_num_threads(1)

EDGE_ID_SEPARATOR = "||"


class CustomModel(nn.Module, PyTorchModelHubMixin):
    """Custom neural network model for domain classification.

    Attributes
    ----------
    model : transformers.AutoModel
        The pre-trained transformer model.
    dropout : torch.nn.Dropout
        Dropout layer for regularization.
    fc : torch.nn.Linear
        Fully connected layer for classification.
    """

    def __init__(self, config):
        super().__init__()
        self.model = AutoModel.from_pretrained(config["base_model"])
        self.dropout = nn.Dropout(config["fc_dropout"])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config["id2label"]))

    def forward(self, input_ids, attention_mask):
        """Forward pass through the network.

        Parameters
        ----------
        input_ids : torch.Tensor
            Token IDs.
        attention_mask : torch.Tensor
            Attention masks.

        Returns
        -------
        torch.Tensor
            Softmax probabilities for each class.
        """
        features = self.model(
            input_ids=input_ids, attention_mask=attention_mask
        ).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)


class SentenceTransformerEmbedding:
    """A class to handle text embeddings using SentenceTransformer."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 32):
        """Initialize the SentenceTransformer model.

        Parameters
        ----------
        model_name : str
            The name of the pre-trained embedding model.
        batch_size : int
            The size of chunks to use to embed the data. Default is 32.
        """
        try:
            self.model = SentenceTransformer(
                model_name,
                cache_folder=str(Path.home() / "nxlu_cache"),
                model_kwargs={"torch_dtype": "float16"},
            )
            self.batch_size = batch_size
        except Exception:
            logger.exception(f"Failed to load SentenceTransformer model '{model_name}'")
            raise

    def get_query_embedding(self, query: str) -> list[float]:
        """Get embedding for a single query string.

        Parameters
        ----------
        query : str
            The query string.

        Returns
        -------
        list[float]
            The embedding vector.
        """
        try:
            embedding = self.model.encode([query])
            return embedding.tolist()
        except Exception:
            logger.exception(f"Failed to encode query '{query}'")
            raise

    def get_text_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text string.

        Parameters
        ----------
        text : str
            The text string.

        Returns
        -------
        list[float]
            The embedding vector.
        """
        try:
            embedding = self.model.encode([text])
            return embedding.tolist()
        except Exception:
            logger.exception(f"Failed to encode text '{text}'")
            raise

    def get_text_embeddings(self, texts: list[str]) -> np.ndarray:
        """Get embeddings for a list of text strings.

        Parameters
        ----------
        texts : list[str]
            The list of text strings.

        Returns
        -------
        np.ndarray
            The array of embedding vectors.
        """
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
            )
        except Exception:
            logger.exception("Failed to encode texts")
            raise
        else:
            return embeddings


class QuerySubgraph:
    """A class to manage and query a subgraph using vector embeddings with FAISS.

    It maintains separate FAISS indices for nodes and edges for comprehensive querying.
    """

    def __init__(
        self,
        similarity_metric: str = "cosine",
        mmr_threshold: float = 0.2,
        embedding_model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 32,
        precision: str = "float32",
    ):
        """Initialize the QuerySubgraph class.

        Parameters
        ----------
        similarity_metric : str
            The similarity metric used for querying ('cosine' or 'euclidean').
        mmr_threshold : float
            The threshold for Maximal Marginal Relevance (MMR).
        embedding_model_name : str
            The name of the pre-trained embedding model.
        batch_size : int
            The size of chunks to use to embed the data. Default is 32.
        """
        self.data_graph = nx.Graph()
        self.similarity_metric = similarity_metric
        self.mmr_threshold = mmr_threshold
        self.batch_size = batch_size
        self.precision = precision
        self.embedding_model_name = embedding_model_name
        self.embedding_model = SentenceTransformerEmbedding(
            self.embedding_model_name, self.batch_size
        )

        # FAISS indices
        self.dim = self.embedding_model.model.get_sentence_embedding_dimension()
        self.index_nodes = self._initialize_faiss_index()
        self.index_edges = self._initialize_faiss_index()

        self.node_text_map = []
        self.edge_text_map = []

        self.node_id_map = {}  # faiss_index -> node_id
        self.edge_id_map = {}  # faiss_index -> edge_id

    def _initialize_faiss_index(self) -> faiss.Index:
        """Initialize a FAISS index based on the similarity metric.

        Returns
        -------
        faiss.Index
            The initialized FAISS index.
        """
        if self.similarity_metric == "cosine":
            index = faiss.IndexFlatIP(self.dim)
        elif self.similarity_metric == "euclidean":
            index = faiss.IndexFlatL2(self.dim)
        else:
            raise ValueError(f"Unsupported similarity metric: {self.similarity_metric}")

        logger.info(f"Initialized FAISS index for {self.similarity_metric} similarity.")
        return index

    def save_indices(self, node_index_path: str, edge_index_path: str) -> None:
        """Save FAISS indices to disk.

        Parameters
        ----------
        node_index_path : str
            File path to save the node FAISS index.
        edge_index_path : str
            File path to save the edge FAISS index.

        Returns
        -------
        None
        """
        faiss.write_index(self.index_nodes, node_index_path)
        faiss.write_index(self.index_edges, edge_index_path)
        logger.info(
            f"FAISS indices saved to '{node_index_path}' and '{edge_index_path}'."
        )

    def load_indices(self, node_index_path: str, edge_index_path: str) -> None:
        """Load FAISS indices from disk.

        Parameters
        ----------
        node_index_path : str
            File path from where to load the node FAISS index.
        edge_index_path : str
            File path from where to load the edge FAISS index.

        Returns
        -------
        None
        """
        if Path(node_index_path).exists():
            self.index_nodes = faiss.read_index(node_index_path)
            logger.info(f"FAISS node index loaded from '{node_index_path}'.")
        else:
            logger.warning(f"Node index file '{node_index_path}' does not exist.")

        if Path(edge_index_path).exists():
            self.index_edges = faiss.read_index(edge_index_path)
            logger.info(f"FAISS edge index loaded from '{edge_index_path}'.")
        else:
            logger.warning(f"Edge index file '{edge_index_path}' does not exist.")

    def load_data_graph(
        self,
        data: list[tuple[str, str, dict[str, Any]]],
        nodes: dict[str, dict[str, Any]],
        min_component_size: int = 2,
    ) -> None:
        """Load the actual data graph, ensuring only nodes in significant connected
        components are included.

        Parameters
        ----------
        data : List[Tuple[str, str, Dict[str, Any]]]
            A list of edges in the form of (node1, node2, attributes) where attributes
            contain edge information (e.g., weight).
        nodes : Dict[str, Dict[str, Any]]
            A dictionary where keys are node identifiers and values are dictionaries of
            node attributes.
        min_component_size : int, optional
            The minimum number of nodes a connected component must have to be included,
            by default 2.

        Returns
        -------
        None
        """
        if not isinstance(data, list) or not all(
            isinstance(edge, tuple) and len(edge) == 3 for edge in data
        ):
            logger.error("Invalid data format for edges.")
            return
        if not isinstance(nodes, dict):
            logger.error("Invalid data format for nodes.")
            return

        try:
            for node, attrs in nodes.items():
                node_str = str(node)
                if not self._is_token_node(node_str, attrs):
                    self.data_graph.add_node(node_str, **attrs)
                    logger.debug(f"Added node: {node_str} with attributes: {attrs}")

            filtered_data = [
                (str(u), str(v), d)
                for u, v, d in data
                if not self._is_token_node(str(u), nodes.get(u, {}))
                and not self._is_token_node(str(v), nodes.get(v, {}))
            ]

            if not filtered_data:
                logger.warning("No valid edges to add after filtering token nodes.")

            self.data_graph.add_weighted_edges_from(
                [(u, v, d.get("weight", 1.0)) for u, v, d in filtered_data]
            )
            logger.debug(
                f"Data graph loaded with {self.data_graph.number_of_nodes()} nodes and "
                f"{self.data_graph.number_of_edges()} edges."
            )

            components = list(nx.connected_components(self.data_graph))
            logger.debug(f"Identified {len(components)} connected components.")

            significant_components = [
                comp for comp in components if len(comp) >= min_component_size
            ]
            logger.info(
                f"{len(significant_components)} components meet the size threshold of "
                f"{min_component_size}."
            )

            if not significant_components:
                logger.warning(
                    "No connected components meet the minimum size threshold."
                )
                self.data_graph = nx.Graph()
                return

            filtered_graph = nx.Graph()
            for comp in significant_components:
                filtered_graph.add_nodes_from(
                    (node, self.data_graph.nodes[node]) for node in comp
                )
                filtered_graph.add_edges_from(
                    (u, v, self.data_graph.edges[u, v])
                    for u, v in self.data_graph.edges
                    if u in comp and v in comp
                )
                logger.debug(f"Added component with {len(comp)} nodes.")

            self.data_graph = filtered_graph
            logger.debug(
                f"Filtered data graph now has {self.data_graph.number_of_nodes()} "
                f"nodes and {self.data_graph.number_of_edges()} edges."
            )
        except Exception:
            logger.exception("Failed to load and filter data graph")
            raise

    def _is_token_node(self, node: str, attrs: dict[str, Any]) -> bool:
        """Determine if a node is a token node based on both its ID and attributes.

        Parameters
        ----------
        node : str
            The node identifier.
        attrs : Dict[str, Any]
            The attributes associated with the node.

        Returns
        -------
        bool
            True if the node is identified as a token node based on its ID or
            attributes, False otherwise.
        """
        if "token" in node.lower():
            return True

        return attrs.get("type") == "token" if attrs else False

    def _extract_node_id(self, node_text: str) -> str | None:
        """Extract the node ID from the node text.
        Assumes the format: "Node: {node}, Attributes: {data}"

        Parameters
        ----------
        node_text : str
            The text representation of the node.

        Returns
        -------
        Optional[str]
            The extracted node ID, or None if extraction fails.
        """
        try:
            prefix = "Node:"
            comma_index = node_text.find(",")
            if comma_index == -1:
                logger.warning(f"Comma not found in node text: {node_text}")
                return None
            node_part = node_text[:comma_index]
            if not node_part.startswith(prefix):
                logger.warning(f"Node text does not start with '{prefix}': {node_text}")
                return None
            node_id = node_part[len(prefix) :].strip()
        except Exception:
            logger.exception(f"Error extracting node ID from text '{node_text}'")
            return None
        else:
            return node_id

    def _extract_edge_tuple(self, edge_text: str) -> tuple[str, str] | None:
        """Extract the edge tuple (u, v) or (u, v, key) from the edge text.
        Assumes: "Edge: {u} -- {relation} (Weight: {weight}) --> {v} | ID: {edge_id}"

        Parameters
        ----------
        edge_text : str
            The text representation of the edge.

        Returns
        -------
        Optional[Tuple[str, str]]
            The extracted edge tuple, or None if extraction fails.
        """
        try:
            edge_id = edge_text.split("| ID:")[1].strip()
            return tuple(edge_id.split("-"))
        except IndexError:
            logger.warning(f"Unable to extract edge tuple from text: {edge_text}")
            return None
        except Exception:
            logger.exception(f"Error extracting edge tuple from text '{edge_text}'")
            return None

    def prepare_node_index(self) -> None:
        logger.info("Preparing node embeddings for efficient querying.")

        nodes_data = [
            (str(node), data)
            for node, data in self.data_graph.nodes(data=True)
            if not self._is_token_node(node, data)
        ]

        if not nodes_data:
            logger.warning("No nodes to index after filtering token nodes.")
            return

        texts = [
            f"Node: {node_id}, Attributes: {data}, Description: "
            f"{data.get('description', '')}"
            for node_id, data in nodes_data
        ]

        self.node_text_map = texts

        if texts:
            embeddings_np = self.embedding_model.get_text_embeddings(texts)
            embeddings_np = quantize_embeddings(embeddings_np, precision=self.precision)
            if self.similarity_metric == "cosine":
                embeddings_np = embeddings_np / np.linalg.norm(
                    embeddings_np, axis=1, keepdims=True
                )
            self.node_embeddings = embeddings_np

            # add embeddings to the FAISS index
            self.index_nodes.add(self.node_embeddings)
            logger.info(f"Computed and indexed embeddings for {len(texts)} nodes.")
        else:
            logger.warning("No nodes to index after filtering token nodes.")
            return

        # build node_id_map from index to node_id
        self.node_id_map = {idx: node_id for idx, (node_id, _) in enumerate(nodes_data)}
        assert len(self.node_id_map) == len(
            self.node_text_map
        ), "Mismatch in node mappings"
        del embeddings_np, texts, nodes_data
        gc.collect()

    def prepare_edge_index(self) -> None:
        logger.info("Preparing edge embeddings for efficient querying.")

        subgraph = self.data_graph

        edge_data = []
        edge_ids = []

        if isinstance(subgraph, (nx.MultiGraph, nx.MultiDiGraph)):
            for u, v, key, data in subgraph.edges(keys=True, data=True):
                if not self._is_token_node(
                    u, subgraph.nodes[u]
                ) and not self._is_token_node(v, subgraph.nodes[v]):
                    edge_id = f"{u}{EDGE_ID_SEPARATOR}{v}{EDGE_ID_SEPARATOR}{key}"
                    edge_data.append((u, v, key, data, edge_id))
        else:
            for u, v, data in subgraph.edges(data=True):
                if not self._is_token_node(
                    u, subgraph.nodes[u]
                ) and not self._is_token_node(v, subgraph.nodes[v]):
                    edge_id = f"{u}{EDGE_ID_SEPARATOR}{v}"
                    edge_data.append((u, v, data, edge_id))

        texts = []
        for entry in edge_data:
            if isinstance(subgraph, (nx.MultiGraph, nx.MultiDiGraph)):
                u, v, key, data, edge_id = entry
            else:
                u, v, data, edge_id = entry
            text = (
                f"Edge: {u} -- {data.get('relation', 'EDGE')} "
                f"(Weight: {data.get('weight', 'N/A')})"
                f" --> {v} | ID: {edge_id}"
            )
            texts.append(text)
            edge_ids.append(edge_id)

        if not texts:
            logger.warning("No valid edges to index after filtering token edges.")
            return

        self.edge_text_map = texts

        if texts:
            embeddings_np = self.embedding_model.get_text_embeddings(texts)
            embeddings_np = quantize_embeddings(embeddings_np, precision=self.precision)
            if self.similarity_metric == "cosine":
                embeddings_np = embeddings_np / np.linalg.norm(
                    embeddings_np, axis=1, keepdims=True
                )
            self.edge_embeddings = embeddings_np

            # add embeddings to the FAISS index
            self.index_edges.add(self.edge_embeddings)
            logger.info(f"Computed and indexed embeddings for {len(texts)} edges.")
        else:
            logger.warning("No edges to index after filtering token edges.")
            return

        self.edge_id_map = dict(enumerate(edge_ids))
        assert len(self.edge_id_map) == len(
            self.edge_text_map
        ), "Mismatch in edge mappings"
        del embeddings_np, texts, edge_ids
        gc.collect()

    def query_graph(
        self,
        query: str,
        top_k_nodes: int = 500,
        top_k_edges: int = 10000,
    ) -> tuple[list[str], list[tuple[str, ...]]]:
        logger.debug(f"Querying graph with: {query}")

        if getattr(self, "node_embeddings", None) is None:
            logger.error(
                "Node embeddings have not been prepared. Call prepare_node_index first."
            )
            return [], []

        # Convert the query to an embedding
        query_embedding = self.embedding_model.get_query_embedding(query)
        query_embedding_np = np.array(query_embedding).astype("float32")

        # Normalize if using cosine similarity
        if self.similarity_metric == "cosine":
            query_embedding_np = query_embedding_np / np.linalg.norm(
                query_embedding_np, axis=1, keepdims=True
            )

        # Use semantic_search_faiss for nodes
        node_results = semantic_search_faiss(
            query_embeddings=query_embedding_np,
            corpus_embeddings=self.node_embeddings,
            top_k=top_k_nodes,
            corpus_precision=self.precision,
            rescore=False,
            output_index=False,
            exact=False,
        )[0]

        node_ids = []
        relevant_nodes_text = []
        for hit in node_results:
            if not isinstance(hit, dict):
                logger.warning(f"Unexpected hit type: {type(hit)}. Skipping.")
                continue

            corpus_id = hit.get("corpus_id")
            if corpus_id is None or corpus_id == -1:
                continue  # Skip invalid results

            nid = self.node_id_map.get(corpus_id)
            if nid:
                node_ids.append(nid)
                relevant_nodes_text.append(self.node_text_map[corpus_id])

        logger.debug(f"Relevant node IDs retrieved: {node_ids}")
        logger.debug(f"Relevant node texts retrieved: {relevant_nodes_text}")

        if not relevant_nodes_text:
            logger.warning(
                "No relevant nodes found. Extracting the largest connected component."
            )
            lcc_graph = lcc(self.data_graph)
            logger.info(
                f"Largest connected component has {lcc_graph.number_of_nodes()} nodes."
            )

            if lcc_graph.number_of_nodes() == 0:
                logger.warning("No connected components found in the graph.")
                return [], []

            node_ids = [str(node) for node in lcc_graph.nodes()]
            edge_tuples = list(lcc_graph.edges())
            return node_ids, edge_tuples

        node_ids = [
            self._extract_node_id(node_text) for node_text in relevant_nodes_text
        ]
        node_ids = [nid for nid in node_ids if nid and self.data_graph.has_node(nid)]
        logger.debug(f"Filtered node IDs present in data graph: {node_ids}")

        if getattr(self, "edge_embeddings", None) is None:
            logger.error(
                "Edge embeddings have not been prepared. Call prepare_edge_index first."
            )
            return node_ids, []

        # use semantic_search_faiss for edges
        edge_results = semantic_search_faiss(
            query_embeddings=query_embedding_np,
            corpus_embeddings=self.edge_embeddings,
            top_k=top_k_edges,
            corpus_precision=self.precision,
            rescore=False,
            output_index=False,
            exact=False,
        )[0]

        edge_ids = []
        relevant_edges_text = []
        for hit in edge_results:
            if isinstance(hit, dict):
                if hit["corpus_id"] == -1:
                    continue  # Skip invalid results
                idx = hit["corpus_id"]
            elif isinstance(hit, str):
                idx = int(hit)
            else:
                logger.warning(f"Unexpected hit type: {type(hit)}. Skipping.")
                continue

            nid = self.edge_id_map.get(idx)
            if nid:
                edge_ids.append(nid)
                relevant_edges_text.append(self.edge_text_map[idx])

        logger.debug(f"Relevant edge IDs retrieved: {edge_ids}")
        logger.debug(f"Relevant edge texts retrieved: {relevant_edges_text}")

        edge_tuples = [
            self._extract_edge_tuple_from_id(edge_id) for edge_id in edge_ids
        ]

        logger.debug(f"Relevant edge tuples retrieved: {edge_tuples}")

        edge_tuples = [
            et
            for et in edge_tuples
            if et
            and self._validate_edge_tuple(et)
            and (et[0] in node_ids or et[1] in node_ids)
        ]
        logger.debug(f"Extracted and filtered edge tuples: {edge_tuples}")

        return node_ids, edge_tuples

    def _validate_edge_tuple(self, edge_tuple: tuple[str, ...]) -> bool:
        """Validate the edge tuple based on the graph type."""
        if self.data_graph.is_multigraph():
            return len(edge_tuple) == 3 and self.data_graph.has_edge(
                edge_tuple[0], edge_tuple[1], key=edge_tuple[2]
            )
        return len(edge_tuple) == 2 and self.data_graph.has_edge(
            edge_tuple[0], edge_tuple[1]
        )

    def _extract_edge_tuple_from_id(self, edge_id: str) -> tuple[str, ...] | None:
        """Extract the edge tuple (u, v) or (u, v, key) from the edge text."""
        try:
            return tuple(edge_id.split(EDGE_ID_SEPARATOR))
        except Exception:
            logger.exception(f"Error extracting edge tuple from ID '{edge_id}'")
            return None

    @staticmethod
    def slice_subgraph(
        graph_data: nx.Graph,
        node_subset: list[str],
        edge_subset: list[tuple[str, str]] | None = None,
    ) -> nx.Graph:
        """Create a subgraph induced by the specified nodes and edges.

        Parameters
        ----------
        graph_data : nx.Graph
            The original graph.
        node_subset : List[str]
            The list of node IDs to include in the subgraph.
        edge_subset : Optional[List[Tuple[str, str]]], optional
            The list of edge tuples to include in the subgraph, by default None.

        Returns
        -------
        nx.Graph
            The resulting subgraph.
        """
        return create_subgraph(graph_data, node_subset, edge_subset)

    def create_query_subgraph(
        self,
        graph: nx.Graph,
        query: str,
        max_iterations: int = 100,
    ) -> nx.Graph:
        """Create a subgraph based on the relevance to the given query.

        Parameters
        ----------
        graph : nx.Graph
            The complete graph to query from.
        query : str
            The query string to search for relevant nodes and edges.
        max_iterations : int, optional
            Maximum number of iterations to attempt to build a connected subgraph.

        Returns
        -------
        nx.Graph
            The resulting subgraph containing the most relevant nodes and edges.
        """
        try:
            self.load_data_graph(
                data=list(graph.edges(data=True)),
                nodes=dict(graph.nodes(data=True)),
            )
            logger.debug("Data graph loaded into QuerySubgraph.")
            logger.debug(f"Data graph nodes: {list(self.data_graph.nodes())}")
        except Exception:
            logger.exception("Error loading data graph into QuerySubgraph.")
            raise

        # get the LCC
        lcc_graph = lcc(self.data_graph)
        total_nodes = lcc_graph.number_of_nodes()
        total_edges = lcc_graph.number_of_edges()

        logger.debug(
            f"The Largest Connected Component (LCC) has {total_nodes} nodes "
            f"and {total_edges} edges"
        )

        top_k_nodes = max(5, int(0.01 * total_nodes))
        top_k_edges = max(10, int(0.01 * total_edges))
        logger.debug(f"Initial top_k_nodes set to {top_k_nodes} based on LCC size.")
        logger.debug(f"Initial top_k_edges set to {top_k_edges} based on LCC size.")

        # adjust mmr_threshold based on density of LCC
        density = nx.density(lcc_graph)
        self.mmr_threshold = self._adjust_mmr_threshold(density)
        logger.debug(
            f"Adjusted mmr_threshold to {self.mmr_threshold} based on LCC density "
            f"{density:.4f}."
        )

        self.prepare_node_index()
        self.prepare_edge_index()

        for iteration in range(1, max_iterations + 1):
            logger.debug(
                f"Iteration {iteration}: Querying with top_k_nodes={top_k_nodes}, "
                f"top_k_edges={top_k_edges}"
            )

            node_ids, edge_tuples = self.query_graph(
                query=query,
                top_k_nodes=top_k_nodes,
                top_k_edges=top_k_edges,
            )
            logger.debug(f"Node IDs after query and filtering: {node_ids}")

            if not node_ids:
                error_msg = "No relevant nodes found for the query."
                logger.error(error_msg)
                raise ValueError(error_msg)

            subgraph = self._create_multi_ego_subgraph(node_ids, edge_tuples)
            logger.debug(
                f"Subgraph created with {subgraph.number_of_nodes()} nodes and "
                f"{subgraph.number_of_edges()} edges."
            )

            if subgraph.number_of_nodes() == 0:
                logger.debug(
                    "Subgraph is empty. Cannot check connectivity on an empty graph."
                )
                continue

            # add MST edges to ensure connectivity
            subgraph = self._add_mst_edges(subgraph)

            subgraph = lcc(subgraph)

            logger.info(
                f"Connected subgraph created with {subgraph.number_of_nodes()} "
                f"nodes and {subgraph.number_of_edges()} edges."
            )

            sigma = nx.sigma(self._to_undirected(subgraph))
            if sigma > 1:
                logger.info(f"Smallworldness sigma ({sigma}) > 1.0")
                return subgraph
            if iteration == max_iterations:
                return subgraph

            logger.debug("Subgraph is disconnected. Preparing for next iteration.")

            # increment top_k_nodes and top_k_edges
            increment_nodes, increment_edges = self._compute_increment(
                total_nodes=total_nodes,
                total_edges=total_edges,
                current_iteration=iteration,
                current_top_k_nodes=top_k_nodes,
                current_top_k_edges=top_k_edges,
                subgraph_density=nx.density(subgraph),
            )

            top_k_nodes = min(top_k_nodes + increment_nodes, total_nodes)
            top_k_edges = min(top_k_edges + increment_edges, total_edges)

            logger.debug(f"Updated top_k_nodes to {top_k_nodes} based on LCC size.")
            logger.debug(f"Updated top_k_edges to {top_k_edges} based on LCC size.")

            self.mmr_threshold = self._adjust_mmr_threshold(nx.density(subgraph))
            logger.debug(
                f"Adjusted mmr_threshold to {self.mmr_threshold} based on current "
                f"subgraph density."
            )

            if top_k_nodes >= total_nodes and top_k_edges >= total_edges:
                logger.debug(
                    "Reached maximum top_k_nodes and top_k_edges based on LCC size."
                )
                break

        if not self._is_connected(subgraph):
            logger.warning("Subgraph is still disconnected after maximum iterations.")
            subgraph = lcc(subgraph)
            logger.info(
                f"Using largest connected component with {subgraph.number_of_nodes()} "
                f"nodes and {subgraph.number_of_edges()} edges."
            )

        return subgraph

    def _adjust_mmr_threshold(self, density: float, default: float = 0.2) -> float:
        """Adjust mmr_threshold based on graph density.

        Parameters
        ----------
        density : float
            The density of the graph.
        default : float
            The default mmr threshold (0.2).

        Returns
        -------
        float
            The adjusted mmr_threshold.
        """
        if density < 0.05:
            return 0.1  # less diversity needed in sparse graphs
        if density > 0.5:
            return 0.3  # more diversity needed in dense graphs
        return default

    def _add_mst_edges(self, subgraph: nx.Graph) -> nx.Graph:
        """Add edges from the Minimum Spanning Tree (MST) of the induced data graph to
        ensure connectivity.

        Parameters
        ----------
        subgraph : nx.Graph
            The subgraph to which MST edges will be added.

        Returns
        -------
        nx.Graph
            The subgraph augmented with MST edges.
        """
        try:
            if subgraph.number_of_nodes() > 1:
                induced_graph = self.data_graph.subgraph(subgraph.nodes())
                mst = nx.minimum_spanning_tree(induced_graph, weight="weight")
                subgraph.add_edges_from(mst.edges(data=True))
                logger.debug(
                    "Added MST edges from induced graph to ensure connectivity."
                )
        except Exception:
            logger.exception("Failed to compute MST on induced graph")
        return subgraph

    def _create_multi_ego_subgraph(
        self,
        node_ids: list[str],
        edge_tuples: list[tuple[str, str]],
    ) -> nx.Graph:
        """Create a subgraph that includes retrieved nodes, retrieved edges,
        and their common neighbors efficiently.

        Parameters
        ----------
        node_ids : List[str]
            List of node IDs that are most relevant to the query.
        edge_tuples : List[Tuple[str, str]]
            List of edge tuples that are most relevant to the query.

        Returns
        -------
        nx.Graph
            The resulting subgraph.
        """
        logger.debug("Creating multi-ego subgraph.")

        subgraph_nodes = set(node_ids)
        subgraph_edges = set(edge_tuples)

        # 1: identify common neighbors to at least n retrieved nodes
        neighbor_counts = defaultdict(int)
        for node in node_ids:
            for neighbor in self.data_graph.neighbors(node):
                neighbor_counts[neighbor] += 1

        common_neighbors = {n for n, count in neighbor_counts.items() if count >= 2}
        subgraph_nodes.update(common_neighbors)
        logger.debug(f"Identified common neighbors: {common_neighbors}")

        # 2: collect relevant edges
        relevant_nodes = subgraph_nodes

        if self.data_graph.is_multigraph():
            subgraph_edges.update(
                (u, v, key)
                for u in relevant_nodes
                for v, keys in self.data_graph[u].items()
                if v in relevant_nodes
                for key in keys
            )
        else:
            subgraph_edges.update(
                (u, v)
                for u in relevant_nodes
                for v in self.data_graph[u]
                if v in relevant_nodes
            )

        logger.debug(f"Total edges collected for subgraph: {len(subgraph_edges)}")

        # 3: create subgraph using edge_subgraph
        try:
            subgraph = self.data_graph.edge_subgraph(subgraph_edges).copy()
            logger.debug(
                f"Multi-ego subgraph created with {subgraph.number_of_nodes()} nodes "
                f"and {subgraph.number_of_edges()} edges."
            )
        except nx.NetworkXError:
            logger.exception("Failed to create edge_subgraph")
            return self.data_graph.__class__()

        return subgraph

    def _is_connected(self, graph: nx.Graph) -> bool:
        """Check if the graph is connected.

        Parameters
        ----------
        graph : nx.Graph
            The graph to check.

        Returns
        -------
        bool
            True if connected, False otherwise.
        """
        if nx.is_directed(graph):
            return nx.is_weakly_connected(graph)
        return nx.is_connected(graph)

    @staticmethod
    def _to_undirected(graph: nx.Graph) -> nx.Graph:
        """Convert the graph to an undirected version for sigma calculation.

        This does not modify the original graph but creates an undirected copy of it.

        Parameters
        ----------
        graph : nx.Graph
            The directed or undirected graph to convert.

        Returns
        -------
        nx.Graph
            An undirected version of the graph.
        """
        if graph.is_directed():
            undirected_graph = graph.to_undirected()
            logger.debug(
                "Converted directed graph to undirected for sigma calculation."
            )
        else:
            undirected_graph = graph.copy()
            logger.debug("Graph is already undirected. No conversion needed.")

        return undirected_graph

    def _compute_increment(
        self,
        total_nodes: int,
        total_edges: int,
        current_iteration: int,
        current_top_k_nodes: int,
        current_top_k_edges: int,
        subgraph_density: float,
    ) -> tuple[int, int]:
        """Compute the increment for top_k_nodes and top_k_edges based on graph
        characteristics.

        This method dynamically determines how much to increment based on the current
        subgraph's density and the overall graph size.

        Parameters
        ----------
        total_nodes : int
            Total number of nodes in the graph.
        total_edges : int
            Total number of edges in the graph.
        current_iteration : int
            Current iteration number.
        current_top_k_nodes : int
            Current number of top_k_nodes.
        current_top_k_edges : int
            Current number of top_k_edges.
        subgraph_density : float
            Current density of the subgraph.

        Returns
        -------
        Tuple[int, int]
            The computed increments for nodes and edges.
        """
        logger.debug(
            f"Computing increments based on iteration {current_iteration}, "
            f"subgraph_density={subgraph_density:.4f}."
        )

        # base increment as a percentage of total nodes and edges
        base_node_increment = max(5, int(0.05 * total_nodes))  # 5% of total nodes
        base_edge_increment = max(10, int(0.1 * total_edges))  # 10% of total edges

        if subgraph_density < 0.05:
            node_increment = int(base_node_increment * 3.0)
            edge_increment = int(base_edge_increment * 3.0)
        elif subgraph_density < 0.1:
            node_increment = int(base_node_increment * 2.5)
            edge_increment = int(base_edge_increment * 2.5)
        elif subgraph_density < 0.3:
            node_increment = int(base_node_increment * 2.0)
            edge_increment = int(base_edge_increment * 2.0)
        else:
            # Slightly increase for denser subgraphs
            node_increment = int(base_node_increment * 1.5)
            edge_increment = int(base_edge_increment * 1.5)

        # further adjust increments based on current iteration to allow for exponential
        # growth without causing too large steps
        scaling_factor = 1 + (0.05 * current_iteration)  # 5% per iteration
        node_increment = int(node_increment * scaling_factor)
        edge_increment = int(edge_increment * scaling_factor)

        remaining_nodes = total_nodes - current_top_k_nodes
        remaining_edges = total_edges - current_top_k_edges

        node_increment = min(node_increment, remaining_nodes)
        edge_increment = min(edge_increment, remaining_edges)

        logger.debug(
            f"Computed increments - Nodes: {node_increment}, Edges: {edge_increment}"
        )

        return node_increment, edge_increment
