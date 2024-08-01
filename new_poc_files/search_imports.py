import re
import sys


def search_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    imports = re.findall(r'^\s*(import\s+\S+|from\s+\S+\s+import\s+\S+)', content, re.MULTILINE)
    for imp in imports:
        print(imp)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python search_imports.py <file_path>')
    else:
        search_imports(sys.argv[1])