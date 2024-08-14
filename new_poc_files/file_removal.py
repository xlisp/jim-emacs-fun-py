import os

def remove_extra_files(directory, max_files=30):
    files = sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    if len(files) > max_files:
        files_to_remove = files[:-max_files]
        for file in files_to_remove:
            os.remove(os.path.join(directory, file))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Remove extra files from a directory.')
    parser.add_argument('directory', type=str, help='The directory to clean up.')
    parser.add_argument('--max_files', type=int, default=30, help='The maximum number of files to keep.')
    args = parser.parse_args()
    remove_extra_files(args.directory, args.max_files)
