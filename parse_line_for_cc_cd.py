#!/opt/anaconda3/bin/python

import ast
import sys
# GPT: ast parse abc.py, and get you line number for abc.py , return current line function code string
def get_code_at_line(file_path, line_number):
    """
    This function returns the code at a specific line number in a given Python file
    by parsing the file with the ast module.

    :param file_path: The path to the Python file.
    :param line_number: The line number to retrieve the code from.
    :return: The code at the specified line as a string, or an error message if the line number is out of range.
    """
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
            tree = ast.parse(source_code, filename=file_path)

            for node in ast.walk(tree):
                if hasattr(node, 'lineno') and node.lineno == line_number:
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                    return '\n'.join(source_code.splitlines()[start_line-1:end_line])

            return "Error: No code at the specified line number."

    except FileNotFoundError:
        return "Error: File not found."
    except SyntaxError as e:
        return f"Error: Syntax error in the file - {str(e)}"

# Example usage
file_path = sys.argv[1] #'parse_end_line_entire.py'
line_number = sys.argv[2]
print(get_code_at_line(file_path, line_number))

# 19行：对了 =》 ！！！！可以作为C-c d的替代方案了
#    for node in ast.walk(tree):
#        if hasattr(node, 'lineno') and node.lineno <= line_number <= getattr(node, 'end_lineno', node.lineno):
#            # For simplicity, assume we return the first found node
#            return node

# 20行
#        if hasattr(node, 'lineno') and node.lineno <= line_number <= getattr(node, 'end_lineno', node.lineno):
#            # For simplicity, assume we return the first found node
#            return node
#
