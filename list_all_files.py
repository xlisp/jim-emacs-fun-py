import os
# show the project all file full path list  as array
def list_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# Example usage
directory_path = '/Users/emacspy/JSPro/ai-chatbot'
all_files = list_all_files(directory_path)
print(all_files)
