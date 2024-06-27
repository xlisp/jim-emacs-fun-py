
from graphviz import Source

file_path = 'new_class.gv'
with open(file_path, 'r') as file:
    dot_data = file.read()

src = Source(dot_data)

src.view()
