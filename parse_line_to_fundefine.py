#!/opt/anaconda3/bin/python


import ast
import sys
# GPT: ast parse abc.py, and get you line number for abc.py , return current line function define code string 
def get_function_code_at_line(file_path, line_number):
    """
    This function returns the full function definition code at a specific line number in a given Python file
    by parsing the file with the ast module.
    
    :param file_path: The path to the Python file.
    :param line_number: The line number to retrieve the function definition from.
    :return: The full function definition code as a string, or an error message if the line number is out of range.
    """
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
            tree = ast.parse(source_code, filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.lineno <= line_number <= node.end_lineno:
                    function_code = source_code.splitlines()[node.lineno-1:node.end_lineno]
                    return '\n'.join(function_code)
                    
            return "Error: No function definition at the specified line number."
    
    except FileNotFoundError:
        return "Error: File not found."
    except SyntaxError as e:
        return f"Error: Syntax error in the file - {str(e)}"

# Example usage
file_path = sys.argv[1] #'parse_end_line_entire.py'
line_number = int(sys.argv[2])
print(get_function_code_at_line(file_path, line_number))

