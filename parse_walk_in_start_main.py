#!/opt/anaconda3/bin/python
import ast
import sys

import graphviz

class FunctionCallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}  # Dictionary to store function names and their calls

    def visit_FunctionDef(self, node):
        function_name = node.name
        self.functions[function_name] = []
        self.current_function = function_name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            called_function_name = node.func.id
            if self.current_function:
                self.functions[self.current_function].append(called_function_name)
        self.generic_visit(node)

def parse_python_file(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read())
    visitor = FunctionCallGraphVisitor()
    visitor.visit(tree)
    return visitor.functions

def find_one_path(functions, start_function):
    path = []
    visited = set()

    def dfs(function):
        if function not in visited:
            visited.add(function)
            path.append(function)
            if function in functions:
                for called_function in functions[function]:
                    dfs(called_function)

    dfs(start_function)
    return path

def generate_graphviz_string(path):
    dot = graphviz.Digraph(comment='Function Call Path')
    for i in range(len(path) - 1):
        dot.node(path[i], path[i])
        dot.node(path[i + 1], path[i + 1])
        dot.edge(path[i], path[i + 1])
    if path:
        dot.node(path[-1], path[-1])  # Add the last node
    return dot.source

# Parse the Python file and generate the function call graph
filename = sys.argv[1] #'abc.py'  # Replace with your file name

functions = parse_python_file(filename)
start_function = sys.argv[2] #'main'  # Replace with your starting function
path = find_one_path(functions, start_function)
graphviz_string = generate_graphviz_string(path)

print(graphviz_string)
