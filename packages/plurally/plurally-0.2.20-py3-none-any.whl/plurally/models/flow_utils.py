from collections import defaultdict
from copy import deepcopy

import networkx as nx
from loguru import logger

from plurally.models import factory
from plurally.models.meta import InstagramNewDm, InstagramSendDm
from plurally.models.node import Node
from plurally.models.subflow import Subflow
from plurally.models.utils import is_list_type


def get_annots_or_raise(node, handle, schema):
    if handle not in schema.model_fields:
        raise ValueError(
            f"Handle {handle} not found in node {node}, options are {list(schema.model_fields)}"
        )
    return schema.model_fields[handle]


def connect_nodes(
    graph, src_node: Node, src_handle: str, tgt_node: Node, tgt_handle: str
):
    if src_node is tgt_node:
        raise ValueError(f"Cannot connect node with itself: {src_node}")

    for node in (src_node, tgt_node):
        if node not in graph:
            raise ValueError(
                f"{node} was not added to {graph} before connecting"
                f" {src_handle} to {tgt_handle}"
            )

    get_annots_or_raise(src_node, src_handle, src_node.OutputSchema)
    inputs_annots = get_annots_or_raise(tgt_node, tgt_handle, tgt_node.InputSchema)

    # if tgt_handle is not a list and there already is a connection it is False
    if not is_list_type(inputs_annots):
        for src, tgt, key in graph.in_edges(tgt_node, data=True):
            if key["tgt_handle"] == tgt_handle:
                raise ValueError(
                    f"Node {tgt_node.name} already has a connection for {tgt_handle}"
                )

    if not tgt_node.validate_connection(src_node, src_handle, tgt_handle):
        raise ValueError(
            f"Connection between {src_node} ({src_handle=}) and {tgt_node} ({tgt_handle=}) is invalid"
        )

    key = f"{src_handle}###{tgt_handle}"
    if (src_node, tgt_node, key) in graph.edges:
        raise ValueError(
            f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} already exists"
        )

    graph.add_edge(
        src_node,
        tgt_node,
        src_handle=src_handle,
        tgt_handle=tgt_handle,
        key=key,
    )


def disconnect_all_nodes_connected_to(
    graph, node_id: str, handle: str = None, mode: str = "all"
):
    assert mode in ("all", "source", "target")
    to_remove = []

    for src_node, tgt_node, key in graph.edges:
        src_handle, tgt_handle = key.split("###")

        is_src = (src_node.node_id == node_id or node_id in src_handle) and (
            not handle or src_handle == handle or src_handle.endswith(f".{handle}")
        )
        is_tgt = (tgt_node.node_id == node_id or node_id in tgt_handle) and (
            not handle or tgt_handle == handle or tgt_handle.endswith(f".{handle}")
        )

        if mode == "all":
            if is_src or is_tgt:
                to_remove.append((src_node, tgt_node, key))
        elif mode == "target" and is_tgt:
            to_remove.append((src_node, tgt_node, key))
        elif mode == "source" and is_src:
            to_remove.append((src_node, tgt_node, key))

    for node in graph.nodes:
        if isinstance(node, Subflow):
            disconnect_all_nodes_connected_to(node.graph, node_id, handle, mode)

    for src_node, tgt_node, key in to_remove:
        graph.remove_edge(src_node, tgt_node, key=key)


def _automate_insta_escalation_connection(out_graph):
    needed_connections = [
        ("was_escalated_previously_", "was_escalated_previously_"),
    ]
    new_dm_nodes = []
    send_dm_nodes = []
    for node in out_graph.nodes:
        if isinstance(node, InstagramNewDm):
            new_dm_nodes.append(node)
        elif isinstance(node, InstagramSendDm):
            send_dm_nodes.append(node)
    if send_dm_nodes:
        assert (
            len(send_dm_nodes) == 1
        ), f"Only one InstagramSendDm block is allowed, found {len(send_dm_nodes)}"
        if len(new_dm_nodes) == 1:
            # check if there are required connections
            for needed_src, needed_tgt in needed_connections:
                for src, _, data in out_graph.in_edges(send_dm_nodes[0], data=True):
                    if (
                        src == new_dm_nodes[0]
                        and data["src_handle"] == needed_src
                        and data["tgt_handle"] == needed_tgt
                    ):
                        break
                else:
                    connect_nodes(
                        out_graph,
                        new_dm_nodes[0],
                        needed_src,
                        send_dm_nodes[0],
                        needed_tgt,
                    )


def get_flatten_graph(in_graph):
    out_graph = nx.MultiDiGraph()

    edges = set()
    for node in in_graph.nodes:
        if isinstance(node, Subflow):
            out_graph = nx.compose(out_graph, node.graph)
        else:
            out_graph.add_node(node)

    for src, tgt, data in in_graph.edges(data=True):
        tgt_handle = data["tgt_handle"]
        src_handle = data["src_handle"]

        if isinstance(src, Subflow):
            src_id, src_handle = src_handle.split(".")
            src = src.get_node(src_id)

        if isinstance(tgt, Subflow):
            if "." in tgt_handle:
                tgt_id, tgt_handle = tgt_handle.split(".")
                tgt = tgt.get_node(tgt_id)
            else:
                assert tgt_handle == "run"
                # add virtual edges to each subnode.run handle
                for subnode in tgt.graph.nodes:
                    edges.add((src, src_handle, subnode, "run"))
                # do not add the one to the run handle of subflow
                # because subflow won't be in flatten graph
                continue
        edges.add((src, src_handle, tgt, tgt_handle))

    # we could skip checks here and make things faster if necessary
    for src, src_handle, tgt, tgt_handle in edges:
        connect_nodes(
            out_graph,
            src,
            src_handle,
            tgt,
            tgt_handle,
        )

    _automate_insta_escalation_connection(out_graph)
    return out_graph


def ungroup_subflow_data(flow_serialized, node_id):
    connected_to_run_handle = []
    nodes_to_add = []
    edges_to_add = []
    for ix, node in enumerate(flow_serialized["nodes"]):
        node = node["id"]
        if node["_node_id"] == node_id:
            assert node["kls"] == "Subflow"
            nodes_to_add.extend(
                [{"id": subflow_n} for subflow_n in node["subflow_nodes"]]
            )
            edges_to_add.extend(node["subflow_links"])
            break
    else:
        raise ValueError(
            f"Node with id {node_id} not found in {flow_serialized['nodes']}"
        )

    del flow_serialized["nodes"][ix]

    for edge in flow_serialized["links"]:
        if edge["target"] == node_id:
            if edge["tgt_handle"] == "run":
                connected_to_run_handle.append(edge)
            else:
                new_target, new_tgt_handle = edge["tgt_handle"].split(".")
                edge["target"] = new_target
                edge["tgt_handle"] = new_tgt_handle
                logger.debug(
                    f"Changed from {node_id[:5]} target to {new_target[:5]} and tgt_handle to {new_tgt_handle}"
                )

        if edge["source"] == node_id:
            new_source, new_src_handle = edge["src_handle"].split(".")
            edge["source"] = new_source
            edge["src_handle"] = new_src_handle
            logger.debug(
                f"Changed from {node_id[:5]} source to {new_source[:5]} and src_handle to {new_src_handle}"
            )

    for node in nodes_to_add:
        flow_serialized["nodes"].append(node)

    for edge in edges_to_add:
        flow_serialized["links"].append(edge)

    return connected_to_run_handle


def adapt_flow_data(data):
    data = deepcopy(data)

    # check node compat
    nodes_to_adapt = defaultdict(list)
    for n in data["nodes"]:
        n = n["id"]
        kls, *_ = factory.MAP[n["kls"]]
        version_from = n.get("PLURALLY_VERSION", 0)
        if kls.PLURALLY_VERSION != version_from and kls.PLURALLY_VERSION != 0:
            nodes_to_adapt[kls].append(n["_node_id"])
        elif kls is Subflow:
            ungroup = False
            for child in n["subflow_nodes"]:
                kls, *_ = factory.MAP[child["kls"]]
                version_from = child.get("PLURALLY_VERSION", 0)
                if kls.PLURALLY_VERSION != version_from and kls.PLURALLY_VERSION != 0:
                    nodes_to_adapt[kls].append(child["_node_id"])
                    ungroup = True
            if ungroup:
                logger.debug(
                    f"Ungrouping subflow {n['name']} ({n['_node_id'][:5]}) to adapt versions"
                )
                connected_to_run_handle = ungroup_subflow_data(data, n["_node_id"])
                if connected_to_run_handle:
                    # in case there was a subflow holding deprecated node, and the subflow's run handle was
                    # connected, then we need to regroup the subflow otherwise logic will differ
                    # if not, then it's okayish, subflow stays ungrouped but the flow will be fine
                    raise NotImplementedError("Need to implement regrouping")

    for kls, node_ids in nodes_to_adapt.items():
        kls.adapt_version(node_ids, data)

    # FIXME: should regroup here...
    # for subflow_id, (node_ids, connected_to_run) in ungrouped.items():
    # flow_utils.regroup_subflow_data(data, subflow_id, node_ids, connected_to_run)
    return data
