#!/opt/anaconda3/bin/python
## USE: ./graphviz_show_file.py '~/Desktop/xxx_class_ref.gv'
import sys
from graphviz import Source

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    dot_data = file.read()

src = Source(dot_data)

src.view()
