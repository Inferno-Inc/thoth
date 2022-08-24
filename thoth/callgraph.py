#!/usr/bin/env python3

from graphviz import Digraph
from .utils import (
    CALLGRAPH_CONFIG,
    CALLGRAPH_NODE_ATTR,
    CALLGRAPH_GRAPH_ATTR,
    CALLGRAPH_EDGE_ATTR,
)


class CallFlowGraph:
    def __init__(self, functions, format, filename, config=CALLGRAPH_CONFIG):
        """Create the Call Flow Graph object

        Args:
            functions (List): List of all functions
            format (String): Format of the dot
            filename (String): Name of the output file
            config (optional): Defaults to CALLGRAPH_CONFIG.
        """
        self.dot = None
        self.config = config
        self.format = format
        self.filename = filename
        self._generate_call_flow_graph(functions)

    def _call_flow_graph_generate_nodes(self, functions):
        """Create all the function nodes

        Args:
            functions (List): List of all functions
        """
        supported_decorators = [
            "constructor",
            "l1_handler",
            "external",
            "view",
            "raw_input",
            "raw_output",
            "known_ap_change",
        ]
        for function in functions:

            # Default values
            shape = self.config["default"]["shape"]
            color = self.config["default"]["color"]
            style = self.config["default"]["style"]
            fillcolor = self.config["default"]["fillcolor"]

            label = function.name

            # This function is an entrypoint
            if function.entry_point:
                shape = self.config["entrypoint"]["shape"]
                style = self.config["entrypoint"]["style"]

            # Node color selection by priority
            # This function is an import
            if function.is_import:
                style = self.config["import"]["style"]
                fillcolor = self.config["import"]["fillcolor"]

            for decorator in function.decorators:
                if decorator in supported_decorators:
                    style = self.config[decorator]["style"]
                    fillcolor = self.config[decorator]["fillcolor"]

            # Search if this function is doing indirect_calls
            if any(inst.is_call_indirect() for inst in function.instructions):
                label += " **"

            # Add decorator below the function name
            if function.decorators != []:
                label += f"\\l{str(function.decorators)}"

            # Create the function node
            self.dot.node(
                function.offset_start,
                label=label,
                shape=shape,
                style=style,
                color=color,
                fillcolor=fillcolor,
            )

    def _generate_call_flow_graph(self, functions):
        """Create the complete CallFlowGraph's dot

        Args:
            functions (List): List of all functions
        """
        # Create the directed graph
        self.dot = Digraph(
            self.filename,
            comment="Call flow graph",
            node_attr=CALLGRAPH_NODE_ATTR,
            graph_attr=CALLGRAPH_GRAPH_ATTR,
            edge_attr=CALLGRAPH_EDGE_ATTR,
        )
        self.dot.format = self.format
        # First, we create the nodes
        self._call_flow_graph_generate_nodes(functions)

        edges = []
        # Build the edges btw functions (nodes)
        for function in functions:
            for inst in function.instructions:
                if inst.is_call_direct():
                    # direct CALL to a fonction
                    if inst.call_xref_func_name is not None:
                        edges.append((function.offset_start, inst.call_offset))
                    else:
                        # relative CALL
                        pass
                elif inst.is_call_indirect():
                    # indirect call
                    # we can't create any edges without evaluating the stack
                    pass

        # Create the edges inside the dot
        while len(edges) > 0:
            # Multiple edges are the same
            if edges.count(edges[0]) > 1:
                self.dot.edge(
                    str(edges[0][0]),
                    str(edges[0][1]),
                    label=str(edges.count(edges[0])),
                )
            # Unique edge
            else:
                self.dot.edge(str(edges[0][0]), str(edges[0][1]))
            edges = list(filter(lambda x: x != edges[0], edges))

    def print(self, view=True):
        """Print the dot

        Args:
            view (bool, optional): Set if the disassembler should open the output file or not. Defaults to True.

        Returns:
            Dot: the output Dot
        """
        self.dot.render(directory="output-callgraph", view=view)
        return self.dot
