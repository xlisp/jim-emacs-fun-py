#!/opt/anaconda3/bin/python

import ast
import os

def find_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        node = ast.parse(file.read())
    
    imports = []
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for name in n.names:
                imports.append(name.name)
        elif isinstance(n, ast.ImportFrom):
            imports.append(n.module)
    return imports

def crawl_directory(directory):
    file_imports = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = find_imports(file_path)
                file_imports[file_path] = imports
    return file_imports

def generate_graphviz_data(file_imports):
    lines = ["digraph G {"]
    for file, imports in file_imports.items():
        file_node = file.replace('\\', '/')
        for imp in imports:
            lines.append(f'  "{file_node}" -> "{imp}";')
    lines.append("}")
    return "\n".join(lines)

if __name__ == "__main__":
    directory = input("Enter the directory to analyze: ")
    file_imports = crawl_directory(directory)
    graphviz_data = generate_graphviz_data(file_imports)

    with open("dependencies.dot", "w") as f:
        f.write(graphviz_data)
    print("Graphviz data written to dependencies.dot")

