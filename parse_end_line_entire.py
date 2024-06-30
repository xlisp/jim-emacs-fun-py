#!/opt/anaconda3/bin/python

import ast
import sys
import astunparse

filename = sys.argv[1]
line_number = int(sys.argv[2])

# Step 1: Read the code from abc.py
with open(filename, 'r') as file:
    source_code = file.read()

# Step 2: Parse the source code into an AST
parsed_code = ast.parse(source_code)

# Function to find the node encompassing the given line number
def get_syntax_node(line_number, tree):
    for node in ast.walk(tree):
        if hasattr(node, 'lineno') and node.lineno <= line_number <= getattr(node, 'end_lineno', node.lineno):
            # For simplicity, assume we return the first found node
            return node
    return None

# Function to extract the complete syntax
def extract_complete_syntax(line_number, tree):
    node = get_syntax_node(line_number, tree)
    return astunparse.unparse(node) if node else None

# Example use, say for line number 42
syntax_node = extract_complete_syntax(line_number, parsed_code)
print(syntax_node)
