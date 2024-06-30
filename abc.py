class D(B, C):
     pass

def class_relations(cls):
     for base in cls.__bases__:
          yield cls.__name__, base.__name__
          yield from class_relations(base)  # Recursion divine

def create_class_diagram(classes):
     dot = graphviz.Digraph()

     for cls in classes:
          dot.node(cls.__name__)
          for child, parent in class_relations(cls):
               dot.edge(parent, child)

def test_abc():
     if 1:
          print(1)

# 坚持去λ化(中-易) jim-emacs-fun-py  master @ ./parse_end_line_forward.py abc.py 10
# dot = graphviz.Digraph()
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ ./parse_end_line_forward.py abc.py 12
# classes
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ ./parse_end_line_forward.py abc.py 12
# classes
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ ./parse_end_line_forward.py abc.py 13
# dot.node(cls.__name__)
# 坚持去λ化(中-易) jim-emacs-fun-py  master @ ./parse_end_line_forward.py abc.py 14
# class_relations(cls)
# ./parse_end_line_forward.py abc.py 18 & ./parse_end_line_forward.py  abc.py 18 & ./parse_end_line3.py  abc.py 18
# => 1  都是输出1
