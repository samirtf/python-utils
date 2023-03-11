import os
import sys

def replace_strings_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        file_contents = file.read()
        new_contents = file_contents.replace(old_string, new_string)
    with open(file_path, 'w') as file:
        file.write(new_contents)

def replace_strings_in_directory(directory_path, old_string, new_string):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            replace_strings_in_file(file_path, old_string, new_string)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            new_dir_path = dir_path.replace(old_string, new_string)
            os.rename(dir_path, new_dir_path)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python replace_strings.py <directory_path> <old_string> <new_string>')
    else:
        directory_path = sys.argv[1]
        old_string = sys.argv[2]
        new_string = sys.argv[3]
        replace_strings_in_directory(directory_path, old_string, new_string)
