import ast
import difflib
from typing import Dict, List, Optional, Tuple

class FunctionComparator:
    def __init__(self):
        self.functions1: Dict[str, ast.FunctionDef] = {}
        self.functions2: Dict[str, ast.FunctionDef] = {}

    def parse_code(self, code: str) -> ast.Module:
        """Parse Python code string into an AST."""
        return ast.parse(code)

    def extract_functions(self, tree: ast.Module) -> Dict[str, ast.FunctionDef]:
        """Extract all function definitions from an AST."""
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        return functions

    def compare_function_structure(self, func1: ast.FunctionDef, func2: ast.FunctionDef) -> Tuple[bool, List[str]]:
        """Compare the structure of two functions."""
        differences = []
        
        # Compare arguments
        args1 = [arg.arg for arg in func1.args.args]
        args2 = [arg.arg for arg in func2.args.args]
        if args1 != args2:
            differences.append(f"Different arguments: {args1} vs {args2}")

        # Compare number of statements
        body1 = len(func1.body)
        body2 = len(func2.body)
        if body1 != body2:
            differences.append(f"Different number of statements: {body1} vs {body2}")

        # Compare types of operations
        ops1 = self._get_operation_types(func1)
        ops2 = self._get_operation_types(func2)
        if ops1 != ops2:
            differences.append(f"Different operation types: {ops1} vs {ops2}")

        return len(differences) == 0, differences

    def _get_operation_types(self, func: ast.FunctionDef) -> List[str]:
        """Get a list of operation types used in the function."""
        ops = []
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    ops.append(f"call:{node.func.id}")
            elif isinstance(node, ast.BinOp):
                ops.append(f"binop:{type(node.op).__name__}")
            elif isinstance(node, ast.Compare):
                ops.append(f"compare:{type(node.ops[0]).__name__}")
        return sorted(ops)

    def compare_codes(self, code1: str, code2: str) -> Dict[str, dict]:
        """Compare two code strings and return differences in their functions."""
        # Parse both code strings
        tree1 = self.parse_code(code1)
        tree2 = self.parse_code(code2)

        # Extract functions from both trees
        self.functions1 = self.extract_functions(tree1)
        self.functions2 = self.extract_functions(tree2)

        # Compare functions
        results = {}
        all_function_names = set(self.functions1.keys()) | set(self.functions2.keys())

        for func_name in all_function_names:
            if func_name not in self.functions1:
                results[func_name] = {
                    'status': 'missing_in_code1',
                    'differences': []
                }
            elif func_name not in self.functions2:
                results[func_name] = {
                    'status': 'missing_in_code2',
                    'differences': []
                }
            else:
                are_same, differences = self.compare_function_structure(
                    self.functions1[func_name],
                    self.functions2[func_name]
                )
                results[func_name] = {
                    'status': 'identical' if are_same else 'different',
                    'differences': differences
                }

        return results

# Example usage
if __name__ == "__main__":
    code1 = """
def add_numbers(a, b):
    return a + b

def multiply(x, y):
    return x * y
"""

    code2 = """
def add_numbers(a, b, c):
    return a + b + c

def multiply(x, y):
    result = x * y
    return result
"""

    comparator = FunctionComparator()
    results = comparator.compare_codes(code1, code2)
    
    for func_name, result in results.items():
        print(f"\nFunction: {func_name}")
        print(f"Status: {result['status']}")
        if result['differences']:
            print("Differences:")
            for diff in result['differences']:
                print(f"  - {diff}")

