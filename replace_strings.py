import os
import sys
import chardet

def replace_strings_in_file(file_path, old_string, new_string):
    with open(file_path, 'rb') as file:
        file_contents = file.read()
        detected_encoding = chardet.detect(file_contents)['encoding']
    with open(file_path, 'w', encoding=detected_encoding) as file:
        file_contents = file_contents.decode(detected_encoding)
        new_contents = file_contents.replace(old_string, new_string)
        file.write(new_contents)

def replace_strings_in_directory(directory_path, old_string, new_string):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            replace_strings_in_file(file_path, old_string, new_string)
            new_file_name = file_name.replace(old_string, new_string)
            if new_file_name != file_name:
                new_file_path = os.path.join(root, new_file_name)
                os.rename(file_path, new_file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            new_dir_name = dir_name.replace(old_string, new_string)
            new_dir_path = os.path.join(root, new_dir_name)
            if new_dir_name != dir_name:
                os.rename(dir_path, new_dir_path)
            replace_strings_in_directory(new_dir_path, old_string, new_string)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python replace_strings.py <directory_path> <old_string> <new_string>')
    else:
        directory_path = sys.argv[1]
        old_string = sys.argv[2]
        new_string = sys.argv[3]
        replace_strings_in_directory(directory_path, old_string, new_string)
