import itertools
from unittest.mock import MagicMock, Mock, patch

import faiss
import networkx as nx
import numpy as np
import pytest
import torch
from torch import nn
from transformers import AutoModel

from nxlu.processing.embed import (
    CustomModel,
    QuerySubgraph,
    SentenceTransformerEmbedding,
)


def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return (np.array(embedding) / norm).tolist()


@pytest.fixture
def custom_model_config():
    return {
        "base_model": "bert-base-uncased",
        "fc_dropout": 0.3,
        "id2label": {0: "ClassA", 1: "ClassB"},
    }


class TestCustomModel:
    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_initialization(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768  # Ensure config is properly mocked
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.model == mock_model
        assert isinstance(model.dropout, nn.Dropout)
        assert isinstance(model.fc, nn.Linear)
        assert model.fc.out_features == len(custom_model_config["id2label"])

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_forward(self, mock_from_pretrained, custom_model_config):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        mock_model.return_value.last_hidden_state = torch.randn(2, 10, 768)
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)
        input_ids = torch.randint(0, 1000, (2, 10))
        attention_mask = torch.ones((2, 10))

        with patch.object(
            model.fc,
            "forward",
            return_value=torch.randn(2, 10, len(custom_model_config["id2label"])),
        ):
            output = model(input_ids, attention_mask)

        assert isinstance(output, torch.Tensor)
        assert output.shape == (2, len(custom_model_config["id2label"]))
        assert torch.allclose(
            output.sum(dim=1), torch.ones(2), atol=1e-5
        )  # Softmax sums to 1

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_invalid_config(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768  # Ensure config is properly mocked
        mock_from_pretrained.return_value = mock_model

        invalid_config = custom_model_config.copy()
        invalid_config["id2label"] = {}  # Empty id2label

        model = CustomModel(config=invalid_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.model == mock_model
        assert isinstance(model.dropout, nn.Dropout)
        assert isinstance(model.fc, nn.Linear)
        assert model.fc.out_features == 0


class TestCustomModelEdgeCases:
    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_zero_classes(self, mock_from_pretrained, custom_model_config):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        mock_from_pretrained.return_value = mock_model

        invalid_config = custom_model_config.copy()
        invalid_config["id2label"] = {}

        model = CustomModel(config=invalid_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.fc.out_features == 0  # Updated assertion

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_forward_incorrect_input_shape(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        # Mock the model to return a last_hidden_state with variable sequence length
        mock_model.return_value.last_hidden_state = torch.randn(
            2, 8, 768
        )  # Changed sequence length
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)
        # Different input dimensions
        input_ids = torch.randint(0, 1000, (2, 8))
        attention_mask = torch.ones((2, 8))

        with patch.object(
            model.fc,
            "forward",
            return_value=torch.randn(2, 8, len(custom_model_config["id2label"])),
        ):
            output = model(input_ids, attention_mask)

        assert isinstance(output, torch.Tensor)
        assert output.shape == (2, len(custom_model_config["id2label"]))
        assert torch.allclose(output.sum(dim=1), torch.ones(2), atol=1e-5)


@pytest.fixture
def fully_connected_graph():
    G = nx.complete_graph(5)
    G = nx.relabel_nodes(G, lambda x: f"node{x}")  # Renaming nodes to strings
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "relationship_type" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture
def partially_connected_graph():
    G = nx.Graph()
    edges = [("node0", "node1"), ("node1", "node2"), ("node3", "node4")]
    G.add_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "relationship_type" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture
def disconnected_graph():
    G = nx.Graph()
    G.add_nodes_from(["node0", "node1", "node2", "node3", "node4"])
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    return G


@pytest.fixture
def weighted_graph():
    G = nx.Graph()
    edges = [
        ("node0", "node1", 0.5),
        ("node1", "node2", 0.7),
        ("node2", "node3", 0.2),
    ]
    G.add_weighted_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G,
        {edge[:2]: "weighted_relationship" for edge in G.edges(data=True)},
        "relationship",
    )
    return G


@pytest.fixture
def binary_graph():
    G = nx.Graph()
    edges = [
        ("node0", "node1"),
        ("node1", "node2"),
        ("node2", "node3"),
        ("node3", "node4"),
    ]
    G.add_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "binary_relationship" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture(
    params=[
        "fully_connected_graph",
        "partially_connected_graph",
        "disconnected_graph",
        "weighted_graph",
        "binary_graph",
    ]
)
def varied_graph(
    request,
    fully_connected_graph,
    partially_connected_graph,
    disconnected_graph,
    weighted_graph,
    binary_graph,
):
    graph = request.getfixturevalue(request.param)
    graph.graph["name"] = request.param
    return graph


# Fixtures for QuerySubgraph
@pytest.fixture
def sample_data():
    data = [
        ("node1", "node2", {"weight": 1.0, "relationship": "connected"}),
        ("node2", "node3", {"weight": 2.0, "relationship": "connected"}),
        ("node3", "node4", {"weight": 3.0, "relationship": "connected"}),
        ("node4", "node5", {"weight": 4.0, "relationship": "connected"}),
    ]
    nodes = {
        "node1": {"label": "Label_1"},
        "node2": {"label": "Label_2"},
        "node3": {"label": "Label_3"},
        "node4": {"label": "Label_4"},
        "node5": {"label": "Label_5"},
    }
    return data, nodes


# Module-level fixture for QuerySubgraph instance
@pytest.fixture
def query_subgraph_instance():
    return QuerySubgraph()


class TestQuerySubgraph:
    def test_query_subgraph_initialization(self, query_subgraph_instance):
        assert isinstance(query_subgraph_instance.data_graph, nx.Graph)
        assert isinstance(
            query_subgraph_instance.embedding_model, SentenceTransformerEmbedding
        )
        assert isinstance(query_subgraph_instance.index_nodes, faiss.Index)
        assert isinstance(query_subgraph_instance.index_edges, faiss.Index)
        assert query_subgraph_instance.node_text_map == []
        assert query_subgraph_instance.edge_text_map == []
        assert query_subgraph_instance.node_id_map == {}
        assert query_subgraph_instance.edge_id_map == {}

    def test_load_data_graph(self, query_subgraph_instance, sample_data):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Ensure token nodes are excluded
        # Since none are token nodes in sample_data, all should be added
        assert query_subgraph_instance.data_graph.number_of_nodes() == 5
        assert query_subgraph_instance.data_graph.number_of_edges() == 4
        for node, attrs in nodes.items():
            assert (
                query_subgraph_instance.data_graph.nodes[node]["label"]
                == attrs["label"]
            )

    def test_load_data_graph_with_token_nodes(
        self, query_subgraph_instance, sample_data
    ):
        data, nodes = sample_data
        # Add token nodes
        nodes["token1"] = {"type": "token", "label": "Token_1"}
        nodes["node6"] = {"label": "Label_6"}

        data += [("node1", "token1", {"weight": 0.5, "relationship": "token_relation"})]
        data += [("node6", "token1", {"weight": 0.5, "relationship": "token_relation"})]
        # Set min_component_size=1 to include isolated nodes
        query_subgraph_instance.load_data_graph(
            data=data, nodes=nodes, min_component_size=1
        )

        # Token nodes should be excluded
        assert (
            query_subgraph_instance.data_graph.number_of_nodes() == 6
        )  # node1 to node6
        assert query_subgraph_instance.data_graph.has_node("token1") is False
        assert query_subgraph_instance.data_graph.has_edge("node1", "token1") is False

    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings")
    def test_prepare_node_index(
        self,
        mock_get_text_embeddings,
        mock_index_flat_ip,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock get_text_embeddings to return fixed embeddings
        mock_get_text_embeddings.return_value = [[0.1, 0.2, 0.3] for _ in range(5)]

        # Mock faiss index
        mock_index = Mock()
        mock_index_flat_ip.return_value = mock_index

        query_subgraph_instance.prepare_node_index()

        # Check that embeddings were called
        # assert mock_get_text_embeddings.called
        # Check that index was created and added embeddings
        mock_index.add.assert_called_once()
        assert query_subgraph_instance.index_nodes == mock_index

    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings")
    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    def test_prepare_edge_index(
        self,
        mock_index_flat_ip,
        mock_get_text_embeddings,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock get_text_embeddings to return fixed embeddings
        mock_get_text_embeddings.return_value = [
            [0.1, 0.2, 0.3] for _ in range(4)
        ]  # 4 edges

        # Mock faiss index
        mock_index = Mock()
        mock_index_flat_ip.return_value = mock_index

        query_subgraph_instance.prepare_edge_index()

        # Check that embeddings were called
        assert mock_get_text_embeddings.called
        # Check that index was created and added embeddings
        mock_index.add.assert_called_once()
        assert query_subgraph_instance.index_edges == mock_index

    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_query_embedding")
    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    def test_query_graph(
        self,
        mock_index_flat_ip,
        mock_get_query_embedding,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Prepare node index
        with patch(
            "nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings"
        ) as mock_get_text_embeddings:
            mock_get_text_embeddings.return_value = [[0.1, 0.2, 0.3] for _ in range(5)]
            mock_index_nodes = Mock()
            mock_index_flat_ip.return_value = mock_index_nodes
            query_subgraph_instance.prepare_node_index()

        # Mock get_query_embedding to return fixed embedding
        mock_get_query_embedding.return_value = [0.1, 0.2, 0.3]

        # Mock index_nodes.search to return fixed distances and indices
        mock_index_nodes.search.return_value = (np.array([[0.9]]), np.array([[0]]))

        # Map index 0 to 'node1' in node_id_map
        query_subgraph_instance.node_id_map = {0: "node1"}
        query_subgraph_instance.node_text_map = [
            "Node: node1, Attributes: {'label': 'Label_1'}"
        ]

        # Mock _extract_node_id to return 'node1' correctly
        with patch.object(
            query_subgraph_instance,
            "_extract_node_id",
            return_value="node1",
            autospec=True,
        ):
            # Mock prepare_edge_index to do nothing
            with patch.object(
                query_subgraph_instance, "prepare_edge_index", autospec=True
            ) as mock_prepare_edge_index:
                node_ids, edge_tuples = query_subgraph_instance.query_graph(
                    query="test query"
                )

        # Check that the node_ids are as expected
        assert node_ids == ["node1"]
        # Since no edges are prepared yet, edge_tuples should be empty
        assert edge_tuples == []


class TestQuerySubgraphEdgeCases:
    @pytest.fixture
    def complex_graph(self):
        G = nx.Graph()
        # Add nodes
        for i in range(10):
            G.add_node(f"node{i}", label=f"Label_{i}")
        # Add edges with weights and relationships
        edges = [
            ("node0", "node1", {"weight": 1.0, "relationship": "connected"}),
            ("node1", "node2", {"weight": 2.0, "relationship": "connected"}),
            ("node2", "node3", {"weight": 3.0, "relationship": "connected"}),
            ("node3", "node4", {"weight": 4.0, "relationship": "connected"}),
            ("node4", "node5", {"weight": 5.0, "relationship": "connected"}),
            ("node5", "node6", {"weight": 6.0, "relationship": "connected"}),
            ("node6", "node7", {"weight": 7.0, "relationship": "connected"}),
            ("node7", "node8", {"weight": 8.0, "relationship": "connected"}),
            ("node8", "node9", {"weight": 9.0, "relationship": "connected"}),
            ("node9", "node0", {"weight": 10.0, "relationship": "connected"}),
            # Token nodes
            ("node0", "token1", {"weight": 0.1, "relationship": "token_relation"}),
            ("token1", "token2", {"weight": 0.2, "relationship": "token_relation"}),
        ]
        G.add_edges_from(edges)
        return G

    @pytest.fixture
    def empty_graph(self):
        G = nx.Graph()
        return G

    def test_query_graph_with_empty_graph(
        self,
        query_subgraph_instance,
        empty_graph,
    ):
        query_subgraph_instance.load_data_graph(data=[], nodes={})
        node_ids, edge_tuples = query_subgraph_instance.query_graph(query="test query")

        assert node_ids == []
        assert edge_tuples == []

    def test_query_graph_with_all_token_nodes(
        self,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        # All nodes are token nodes
        nodes = {node: {"type": "token"} for node in nodes}
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Replace FAISS index_nodes and index_edges with Mocks
        mock_index_nodes = Mock(spec=faiss.Index)
        mock_index_nodes.d = 3  # Set the expected dimension
        mock_index_edges = Mock(spec=faiss.Index)
        mock_index_edges.d = 3  # Set the expected dimension
        query_subgraph_instance.index_nodes = mock_index_nodes
        query_subgraph_instance.index_edges = mock_index_edges

        # Mock get_query_embedding to return a fixed embedding
        with patch.object(
            query_subgraph_instance.embedding_model,
            "get_query_embedding",
            return_value=[0.1, 0.2, 0.3],
            autospec=True,
        ):
            # Mock index_nodes.search to return no valid indices
            query_subgraph_instance.index_nodes.search.return_value = (
                np.array([[0.0]]),
                np.array([[-1]]),
            )

            node_ids, edge_tuples = query_subgraph_instance.query_graph(
                query="test query"
            )
        assert node_ids == []
        assert edge_tuples == []

    def test_create_subgraph_with_no_edges(self, varied_graph):
        node_subset = ["node1", "node2"]
        edge_subset = []
        subgraph = QuerySubgraph.slice_subgraph(varied_graph, node_subset, edge_subset)

        assert isinstance(subgraph, nx.Graph)
        assert subgraph.number_of_nodes() == len(node_subset)

        # Edges only included if in edge_subset
        assert subgraph.number_of_edges() == 0

    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_query_embedding")
    def test_query_graph_with_no_matching_nodes(
        self,
        mock_get_query_embedding,
        mock_index_flat_ip,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        mock_get_query_embedding.return_value = [0.1, 0.2, 0.3]

        with patch.object(
            query_subgraph_instance, "prepare_node_index", return_value=None
        ):
            mock_index_nodes = MagicMock(spec=faiss.Index)
            mock_index_nodes.d = 3
            mock_index_nodes.search = MagicMock()
            mock_index_nodes.ntotal = 5
            query_subgraph_instance.index_nodes = mock_index_nodes

            mock_index_nodes.search.return_value = (
                np.array([[0.0, 0.0, 0.0, 0.0, 0.0]]),
                np.array([[-1, -1, -1, -1, -1]]),
            )

            with patch.object(
                query_subgraph_instance,
                "_extract_node_id",
                side_effect=[None, None, None, None, None],
                autospec=True,
            ):
                node_ids, edge_tuples = query_subgraph_instance.query_graph(
                    query="no match"
                )

        assert set(node_ids) == set(
            query_subgraph_instance.data_graph.nodes()
        ), "Expected all nodes from the largest connected component."
        assert edge_tuples == list(
            query_subgraph_instance.data_graph.edges()
        ), "Expected all edges from the largest connected component."

    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings")
    def test_query_graph_with_large_k_values(
        self,
        mock_get_text_embeddings,
        mock_index_flat_ip,  # This is now a MagicMock replacing faiss.IndexFlatIP
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data

        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Instead of specifying spec=faiss.IndexFlatIP (which is now a MagicMock),
        # specify spec=faiss.Index or remove the spec.
        mock_index_nodes = MagicMock(spec=faiss.Index)
        mock_index_nodes.d = 3  # Set the expected dimension
        mock_index_nodes.ntotal = 5
        mock_index_nodes.add = MagicMock()
        mock_index_nodes.search = MagicMock()

        mock_index_edges = MagicMock(spec=faiss.Index)
        mock_index_edges.d = 3  # Set the expected dimension
        mock_index_edges.ntotal = 5
        mock_index_edges.add = MagicMock()
        mock_index_edges.search = MagicMock()

        mock_index_flat_ip.side_effect = [mock_index_nodes, mock_index_edges]

        # Mock get_text_embeddings to return fixed embeddings
        mock_get_text_embeddings.return_value = [[0.1, 0.2, 0.3] for _ in range(5)]

        # Prepare node index
        query_subgraph_instance.prepare_node_index()

        # Prepare edge index
        query_subgraph_instance.prepare_edge_index()

        # Mock get_query_embedding to return fixed embedding as a list
        mocked_query_embedding = [0.1, 0.2, 0.3]

        with patch.object(
            query_subgraph_instance.embedding_model,
            "get_query_embedding",
            return_value=mocked_query_embedding,
            autospec=True,
        ):
            # Mock index_nodes.search to return fixed distances and indices
            mock_index_nodes.search.return_value = (
                np.array([[0.9, 0.8, 0.7, 0.6, 0.5]], dtype="float32"),
                np.array([[0, 1, 2, 3, 4]]),
            )

            # Map index 0 to 'node1', etc., in node_id_map
            query_subgraph_instance.node_id_map = {
                0: "node1",
                1: "node2",
                2: "node3",
                3: "node4",
                4: "node5",
            }
            query_subgraph_instance.node_text_map = [
                "Node: node1, Attributes: {'label': 'Label_1'}",
                "Node: node2, Attributes: {'label': 'Label_2'}",
                "Node: node3, Attributes: {'label': 'Label_3'}",
                "Node: node4, Attributes: {'label': 'Label_4'}",
                "Node: node5, Attributes: {'label': 'Label_5'}",
            ]

            # Mock _extract_node_id to return node IDs correctly
            with patch.object(
                query_subgraph_instance,
                "_extract_node_id",
                side_effect=["node1", "node2", "node3", "node4", "node5"],
                autospec=True,
            ):
                # Mock prepare_edge_index to do nothing
                with patch.object(
                    query_subgraph_instance, "prepare_edge_index", autospec=True
                ) as mock_prepare_edge_index:
                    node_ids, edge_tuples = query_subgraph_instance.query_graph(
                        query="test query", top_k_nodes=10, top_k_edges=10
                    )

        assert node_ids == [
            "node1",
            "node2",
            "node3",
            "node4",
            "node5",
        ], "Node IDs do not match expected."
        # Since prepare_edge_index is mocked to do nothing, edge_tuples should be empty
        assert (
            edge_tuples == []
        ), "Edge tuples should be empty as prepare_edge_index was mocked."

    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings")
    def test_create_query_subgraph_complex(
        self,
        mock_get_text_embeddings,
        mock_index_flat_ip,
        complex_graph,
    ):
        # Create mock indices
        mock_index_nodes = MagicMock(spec=faiss.Index)
        mock_index_nodes.d = 3
        mock_index_nodes.ntotal = 0
        mock_index_nodes.add = MagicMock()
        mock_index_nodes.search = MagicMock(
            return_value=(
                np.array([[0.9, 0.8, 0.7, 0.6, 0.5]], dtype="float32"),
                np.array([[0, 1, 2, 3, 4]]),
            )
        )

        mock_index_edges = MagicMock(spec=faiss.Index)
        mock_index_edges.d = 3
        mock_index_edges.ntotal = 0
        mock_index_edges.add = MagicMock()

        # Use itertools.cycle to avoid StopIteration
        index_cycle = itertools.cycle([mock_index_nodes, mock_index_edges])

        with patch.object(
            QuerySubgraph,
            "_initialize_faiss_index",
            side_effect=index_cycle,
        ):
            query_subgraph_instance = QuerySubgraph()

            # Assign the mock indices manually
            query_subgraph_instance.index_nodes = mock_index_nodes
            query_subgraph_instance.index_edges = mock_index_edges

            query_subgraph_instance.load_data_graph(
                data=list(complex_graph.edges(data=True)),
                nodes=dict(complex_graph.nodes(data=True)),
            )

            # Prepare embeddings
            def mock_get_text_embeddings_local(texts, *args, **kwargs):
                # Ensure that texts are non-empty
                assert len(texts) > 0, "Texts should not be empty"
                return [[0.1, 0.2, 0.3] for _ in texts]

            mock_get_text_embeddings.side_effect = mock_get_text_embeddings_local

            # Prepare node index
            query_subgraph_instance.prepare_node_index()

            # Manually update ntotal to reflect the number of embeddings added
            mock_index_nodes.ntotal = len(query_subgraph_instance.node_text_map)

            # Correctly map all indices to node IDs
            node_ids_in_index = [
                f"node{i}" for i in range(len(query_subgraph_instance.node_text_map))
            ]
            query_subgraph_instance.node_id_map = dict(enumerate(node_ids_in_index))
            query_subgraph_instance.node_text_map = [
                f"Node: node{i}, Attributes: {complex_graph.nodes[f'node{i}']}, "
                f"Description: "
                for i in range(len(query_subgraph_instance.node_text_map))
            ]

            # Mock the search method to return specific indices and distances
            query_subgraph_instance.index_nodes.search = MagicMock(
                return_value=(
                    np.array([[0.9, 0.8, 0.7, 0.6, 0.5]], dtype="float32"),
                    np.array([[0, 1, 2, 3, 4]]),
                )
            )

            # Mock _extract_node_id to return specific node IDs
            with patch.object(
                query_subgraph_instance,
                "_extract_node_id",
                side_effect=[
                    "node0",
                    "node1",
                    "node2",
                    "node3",
                    "node4",
                ],
                autospec=True,
            ):
                # Create the query subgraph
                subgraph_result = query_subgraph_instance.create_query_subgraph(
                    graph=complex_graph,
                    query="connectivity",
                    max_iterations=1,
                )

        # Assertions to verify the results
        assert isinstance(
            subgraph_result, nx.Graph
        ), "Resulting subgraph should be a NetworkX Graph."
        assert (
            subgraph_result.number_of_nodes() >= 5
        ), "Subgraph should have at least 5 nodes."
        assert (
            subgraph_result.number_of_edges() >= 4
        ), "Subgraph should have at least 4 edges."
        assert subgraph_result.has_edge(
            "node0", "node1"
        ), "Edge (node0, node1) should exist."
        assert subgraph_result.has_edge(
            "node1", "node2"
        ), "Edge (node1, node2) should exist."

    @patch("nxlu.processing.embed.faiss.IndexFlatIP")
    @patch("nxlu.processing.embed.SentenceTransformerEmbedding.get_text_embeddings")
    def test_create_query_subgraph_disconnected_subgraph(
        self,
        mock_get_text_embeddings,
        mock_index_flat_ip,
        sample_data,
    ):
        data, nodes = sample_data

        # Create mock indices
        mock_index_nodes = MagicMock(spec=faiss.Index)
        mock_index_nodes.d = 3
        mock_index_nodes.ntotal = 0
        mock_index_nodes.add = MagicMock()
        mock_index_nodes.search = MagicMock(
            return_value=(
                np.array([[0.0, 0.0, 0.0, 0.0, 0.0]], dtype="float32"),
                np.array([[-1, -1, -1, -1, -1]]),
            )
        )

        mock_index_edges = MagicMock(spec=faiss.Index)
        mock_index_edges.d = 3
        mock_index_edges.ntotal = 0
        mock_index_edges.add = MagicMock()

        # Use itertools.cycle to avoid StopIteration
        index_cycle = itertools.cycle([mock_index_nodes, mock_index_edges])

        with patch.object(
            QuerySubgraph,
            "_initialize_faiss_index",
            side_effect=index_cycle,
        ):
            query_subgraph_instance = QuerySubgraph()
            query_subgraph_instance.index_nodes = mock_index_nodes
            query_subgraph_instance.index_edges = mock_index_edges
            query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

            def side_effect_get_text_embeddings(texts, *args, **kwargs):
                # Ensure that texts are non-empty
                assert len(texts) > 0, "Texts should not be empty"
                return [[0.1, 0.2, 0.3] for _ in texts]

            mock_get_text_embeddings.side_effect = side_effect_get_text_embeddings

            # Prepare embeddings
            query_subgraph_instance.prepare_node_index()

            # Manually update ntotal to reflect the number of embeddings added
            mock_index_nodes.ntotal = len(query_subgraph_instance.node_text_map)

            # Correctly map all indices to node IDs based on actual nodes
            node_ids_in_index = list(
                nodes.keys()
            )  # ['node1', 'node2', 'node3', 'node4', 'node5']
            query_subgraph_instance.node_id_map = dict(enumerate(node_ids_in_index))
            query_subgraph_instance.node_text_map = [
                f"Node: {node_id}, Attributes: {nodes[node_id]}, Description: "
                for node_id in node_ids_in_index
            ]

            # Mock the search method to return specific indices and distances
            query_subgraph_instance.index_nodes.search = MagicMock(
                return_value=(
                    np.array([[0.0, 0.0, 0.0, 0.0, 0.0]], dtype="float32"),
                    np.array([[-1, -1, -1, -1, -1]]),
                )
            )

            # Mock _extract_node_id to return None for all attempts
            with patch.object(
                query_subgraph_instance,
                "_extract_node_id",
                side_effect=[None, None, None, None, None],
                autospec=True,
            ):
                node_ids, edge_tuples = query_subgraph_instance.query_graph(
                    query="no match"
                )

        assert set(node_ids) == set(
            query_subgraph_instance.data_graph.nodes()
        ), "Expected all nodes from the largest connected component."
        assert edge_tuples == list(
            query_subgraph_instance.data_graph.edges()
        ), "Expected all edges from the largest connected component."
