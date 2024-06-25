# GPT: python how to show all function relationship  with graphviz => TODO: save relationship to datalog
import ast
import graphviz

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.calls.append((self.current_function, node.func.id))
            elif isinstance(node.func, ast.Attribute):
                self.calls.append((self.current_function, node.func.attr))
        self.generic_visit(node)

def get_function_calls(module_path):
    with open(module_path, 'r') as file:
        tree = ast.parse(file.read(), filename=module_path)
    
    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    return visitor.calls

def create_function_diagram(calls, output_file="function_diagram"):
    dot = graphviz.Digraph(comment='Function Call Diagram')
    
    for caller, callee in calls:
        dot.edge(caller, callee)
    
    dot.render(output_file, view=True)

# Example usage with a hypothetical module file path `mymodule.py`
module_path = 'mymodule_fun.py'  # replace with the path to your module
calls = get_function_calls(module_path)
create_function_diagram(calls)
