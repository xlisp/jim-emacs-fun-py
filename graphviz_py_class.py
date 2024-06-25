## GPT: python how to show all class relationship  with graphviz
import inspect
import graphviz
from typing import List

def get_class_relationships(module) -> List[str]:
    classes = [cls for _, cls in inspect.getmembers(module, inspect.isclass)]
    edges = []

    for cls in classes:
        bases = cls.__bases__
        for base in bases:
            if base.__module__ == module.__name__:  # only consider relationships within the same module
                edges.append((base.__name__, cls.__name__))
    
    return edges

def create_class_diagram(module, output_file="class_diagram"):
    edges = get_class_relationships(module)
    dot = graphviz.Digraph(comment='Class Diagram')
    
    for base, derived in edges:
        dot.edge(base, derived)
    
    dot.render(output_file, view=True)

## => ! Must Ipython Eval it:
# Example usage with a hypothetical module `mymodule`
## import mymodule  # replace with your module
## create_class_diagram(mymodule)
