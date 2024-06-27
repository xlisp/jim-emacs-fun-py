import graphviz
import inspect
# GPT: python project show class graphviz relations
# TODO: 如何嵌入代码当中，实时查看类列表之间的关系呢？
# 1. import进来所有相关的类，然后调用函数create_class_diagram就好了。
# 2. 用ag 搜索相关的类，比如一个函数在所有文件中使用，找到它的类的列表，传递给这个create_class_diagram就好了
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
