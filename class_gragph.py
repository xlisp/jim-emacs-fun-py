import graphviz
import inspect
# GPT: python project show class graphviz relations
class A:
     pass

class B(A):
     pass

class C(A):
     pass

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

     return dot

classes = [A, B, C, D]

diagram = create_class_diagram(classes)

diagram.view()
