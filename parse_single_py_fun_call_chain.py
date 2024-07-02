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

def generate_graphviz_output(functions):
    dot = graphviz.Digraph(comment='Function Call Graph')
    for function, calls in functions.items():
        dot.node(function, function)
        for call in calls:
            dot.node(call, call)
            dot.edge(function, call)
    #dot.render(output_filename, format='png', view=True)
    return dot.source

# Parse the Python file and generate the function call graph
filename = sys.argv[1]
#output_filename = 'function_call_graph'

functions = parse_python_file(filename)
print(generate_graphviz_output(functions))
