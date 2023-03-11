import os
import sys
import chardet
import traceback

def replace_strings_in_file(file_path, old_string, new_string):
    try:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
            detected_encoding = chardet.detect(file_contents)['encoding']
        with open(file_path, 'w', encoding=detected_encoding or 'utf-8') as file:
            file_contents = file_contents.decode(detected_encoding or 'utf-8')
            new_contents = file_contents.replace(old_string, new_string)
            file.write(new_contents)
    except Exception as e:
        print(f"Error replacing strings in file {file_path}: {e}")
        traceback.print_exc()

def replace_strings_in_directory(directory_path, old_string, new_string):
    try:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    replace_strings_in_file(file_path, old_string, new_string)
                    new_file_name = file_name.replace(old_string, new_string)
                    if new_file_name != file_name:
                        new_file_path = os.path.join(root, new_file_name)
                        os.rename(file_path, new_file_path)
                except Exception as e:
                    print(f"Error replacing strings in file {file_path}: {e}")
                    traceback.print_exc()
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    new_dir_name = dir_name.replace(old_string, new_string)
                    new_dir_path = os.path.join(root, new_dir_name)
                    if new_dir_name != dir_name:
                        os.rename(dir_path, new_dir_path)
                        dir_path = new_dir_path  # Fix UnboundLocalError
                    replace_strings_in_directory(dir_path, old_string, new_string)  # Recursive call
                except Exception as e:
                    print(f"Error replacing strings in directory {dir_path}: {e}")
                    traceback.print_exc()
    except Exception as e:
        print(f"Error replacing strings in directory {directory_path}: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python replace_strings.py <directory_path> <old_string> <new_string>')
    else:
        directory_path = sys.argv[1]
        old_string = sys.argv[2]
        new_string = sys.argv[3]
        replace_strings_in_directory(directory_path, old_string, new_string)
