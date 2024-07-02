#!/opt/anaconda3/bin/python

## USE: ./parse_log_print_fun.py ~/Desktop/DEBUG-NEXT-701001.log

import os
import re
import sys

log_path = sys.argv[1]

log_content = open(log_path, 'r').read()

def parse_log(log):
    """
    Parse the log to extract filenames and line numbers.

    :param log: The log content as a string.
    :return: A list of tuples containing (filename, line_number).
    """
    pattern = re.compile(r'(?P<filename>[\w_]+\.py):(?P<line_number>\d+)')
    matches = pattern.findall(log)
    return [(match[0], int(match[1])) for match in matches]

def find_code_in_project(project_path, filename, line_number):
    """
    Find the specified line in the given file within the project directory.

    :param project_path: The path to the project directory.
    :param filename: The name of the file to search.
    :param line_number: The line number to find.
    :return: The path to the file and the line content, or an error message.
    """
    for root, _, files in os.walk(project_path):
        if filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if 1 <= line_number <= len(lines):
                    return file_path, line_number, lines[line_number - 1].strip()
    return "Error: File or line not found in the project."

def main():
    project_path = '/Users/emacspy/ClackyAIPro/staging-clacky-ai-agent' ##'pa/to/your/project'  # Replace with the actual project path
    log_entries = parse_log(log_content)

    results = []
    for filename, line_number in log_entries:
        result = find_code_in_project(project_path, filename, line_number)
        results.append(result)

    for result in results:
        if isinstance(result, tuple):
            print(f"#======= File: {result[0]}, Line: {result[1]} Code: {result[2]}\n")
            # print(f"#======= File: {result[0]}, Line: {result[1]}\n") # 需要当前行的代码不然一个函数多个日志就不知道执行到了哪一行了！
            os.system(f'/Users/emacspy/EmacsPyPro/jim-emacs-fun-py/parse_line_to_fundefine2.py {result[0]} {result[1]}')
        else:
            print(result)

if __name__ == "__main__":
    main()
