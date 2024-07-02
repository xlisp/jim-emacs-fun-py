#!/opt/anaconda3/bin/python
import ast
import sys

import os
from graphviz import Digraph

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.call_graph = Digraph()
        self.current_function = None
        self.edges = set()

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.call_graph.node(self.current_function, self.current_function)
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            func_name = self._get_call_name(node)
            if func_name:
                edge = (self.current_function, func_name)
                if edge not in self.edges:
                    self.call_graph.edge(*edge)
                    self.edges.add(edge)
        self.generic_visit(node)

    def _get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

def parse_python_files(directory):
    visitor = CallGraphVisitor()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    tree = ast.parse(f.read(), filename=file)
                    visitor.visit(tree)
    return visitor.call_graph

if __name__ == "__main__":
    directory = sys.argv[1]
    call_graph = parse_python_files(directory)
    #call_graph.render("call_graph", format="png", cleanup=True)
    print(call_graph.source)
    print("Call graph generated and saved as call_graph.png")
