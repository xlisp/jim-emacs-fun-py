#!/opt/anaconda3/bin/python


import ast
import sys
# GPT: ast parse abc.py, and get you line number for abc.py , return current line function define code string

def get_function_code_at_line(file_path, line_number):
    """
    This function returns the full function definition code at a specific line number in a given Python file
    by parsing the file with the ast module. It supports both async and regular functions.

    :param file_path: The path to the Python file.
    :param line_number: The line number to retrieve the function definition from.
    :return: The full function definition code as a string, or an error message if the line number is out of range.
    """
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
            tree = ast.parse(source_code, filename=file_path)

            for node in ast.walk(tree):
                if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) and node.lineno <= line_number <= node.end_lineno:
                    # Collect all lines of the function definition including decorators
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line

                    # Extract the function code from the source code
                    function_code_lines = source_code.splitlines()[start_line-1:end_line]
                    function_code = '\n'.join(function_code_lines)

                    # Add decorators if any ## GPT: get_function_code_at_line MUST support async function & function define only two line
                    for decorator in node.decorator_list:
                        decorator_line = source_code.splitlines()[decorator.lineno-1]
                        function_code = f"{decorator_line}\n{function_code}"

                    return function_code

            return "Error: No function definition at the specified line number."

    except FileNotFoundError:
        return "Error: File not found."
    except SyntaxError as e:
        return f"Error: Syntax error in the file - {str(e)}"

# Example usage
file_path = sys.argv[1] #'parse_end_line_entire.py'
line_number = int(sys.argv[2])
print(get_function_code_at_line(file_path, line_number))
