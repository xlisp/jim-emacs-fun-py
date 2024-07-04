def get_file_paths(file_tree):
    file_paths = []

    def traverse(node):
        if node['type'] == 'FILE':
            file_paths.append(node['path'])
        elif node['type'] == 'DIRECTORY':
            for child in node['children']:
                traverse(child)

    traverse(file_tree)
    return file_paths

file_tree = {
    'path': '.', 'name': '.', 'type': 'DIRECTORY', 'children': [
        {'type': 'FILE', 'name': 'hello.c', 'path': 'hello.c', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'FILE', 'name': 'hello.go', 'path': 'hello.go', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'FILE', 'name': 'hello.rb', 'path': 'hello.rb', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'FILE', 'name': 'index.html', 'path': 'index.html', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'FILE', 'name': 'index.js', 'path': 'index.js', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'DIRECTORY', 'name': 'root', 'path': 'root', 'children': [
            {'type': 'FILE', 'name': '1.txt', 'path': 'root/1.txt', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False}
        ], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False},
        {'type': 'DIRECTORY', 'name': 'tests', 'path': 'tests', 'children': [
            {'type': 'FILE', 'name': 'test_model.rb', 'path': 'tests/test_model.rb', 'children': [], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False}
        ], 'hide': False, 'lock': False, 'unittest': False, 'isRetainedFile': False}
    ]
}

file_paths = get_file_paths(file_tree)
print(file_paths)
