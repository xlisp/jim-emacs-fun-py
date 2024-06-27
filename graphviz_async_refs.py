#!/opt/anaconda3/bin/python

import sys
import os
import ast
import graphviz

# Directory where the Python files lie
directory_path = sys.argv[1]

async_calls = {}

def find_async_functions(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    async_functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef):
            async_functions.append(node.name)

    return async_functions

def find_await_calls(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    await_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Await):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    await_calls.append(node.value.func.attr)
                elif isinstance(node.value.func, ast.Name):
                    await_calls.append(node.value.func.id)

    return await_calls

for root, _, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            async_funcs = find_async_functions(file_path)
            await_funcs = find_await_calls(file_path)
            async_calls[file_path] = (async_funcs, await_funcs)

dot = graphviz.Digraph()

for file_path, (async_funcs, await_funcs) in async_calls.items():
    for func in async_funcs:
        dot.node(f'{file_path}:{func}', f'{func}', shape='box', color='lightblue2')

    for await_func in await_funcs:
        for func in async_funcs:
            dot.edge(f'{file_path}:{func}', f'{file_path}:{await_func}')

# Save and visualize the graph
dot.render('async_functions_graph', format='png')

print("The graph is created and saved as 'async_functions_graph.png'.")

