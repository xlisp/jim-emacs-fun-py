import os
import sys

def find_imports_in_file(file_path, base_dir):
    """Search for import statements in a single file and return them."""
    imports = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('import') or line.startswith('from'):
                # Split the line into components
                parts = line.split()
                if parts[0] == 'from':
                    # Handle "from ... import ..."
                    module = parts[1]
                    if not module.startswith('.'):
                        imports.append(line)
                    else:
                        full_path = resolve_relative_import(file_path, module, base_dir)
                        if full_path:
                            imports.append(f"from {full_path} {' '.join(parts[2:])}")
                elif parts[0] == 'import':
                    # Handle "import ..."
                    modules = parts[1].split(',')
                    for module in modules:
                        module = module.strip()
                        if not module.startswith('.'):
                            imports.append(f"import {module}")
                        else:
                            full_path = resolve_relative_import(file_path, module, base_dir)
                            if full_path:
                                imports.append(f"import {full_path}")
    return imports

def resolve_relative_import(file_path, module, base_dir):
    """Resolve relative import to its full path."""
    file_dir = os.path.dirname(file_path)
    depth = module.count('.')
    relative_path = module.lstrip('.')
    
    parent_dir = file_dir
    for _ in range(depth - 1):
        parent_dir = os.path.dirname(parent_dir)
    
    full_path = os.path.relpath(os.path.join(parent_dir, relative_path), base_dir).replace(os.sep, '.')
    return full_path

def search_imports_in_directory(directory):
    """Search for import statements in all Python files within a directory."""
    all_imports = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = find_imports_in_file(file_path, directory)
                if imports:
                    all_imports.append((file_path, imports))
    return all_imports

def print_imports(imports):
    """Print the import statements."""
    for file_path, import_lines in imports:
        print(f"\n## In file: {file_path}")
        for line in import_lines:
            print(f"{line}")

if __name__ == "__main__":
    directory = sys.argv[1] #input("Enter the directory path to search for import statements: ")
    imports = search_imports_in_directory(directory)
    print_imports(imports)

