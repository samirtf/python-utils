import os
import argparse
import chardet
import shutil

DEFAULT_IGNORE_LIST = ['.git', '.github']

def replace_strings_in_file(file_path, old_str, new_str):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        if detected_encoding is None:
            raise Exception(f"Could not detect encoding for file {file_path}")
        decoded_data = raw_data.decode(detected_encoding, errors='replace')
    replaced_data = decoded_data.replace(old_str, new_str)
    encoded_data = replaced_data.encode(detected_encoding, errors='replace')
    with open(file_path, 'wb') as f:
        f.write(encoded_data)

def replace_strings_in_dir(dir_path, old_str, new_str, output_dir, ignore_list):
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        files[:] = [f for f in files if not f.lower().endswith(tuple(ignore_list))]
        for file_name in files:
            if file_name not in ignore_list:
                file_path = os.path.join(root, file_name)
                try:
                    replace_strings_in_file(file_path, old_str, new_str)
                    new_file_path = os.path.join(root.replace(dir_path, output_dir), file_name)
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.copy2(file_path, new_file_path)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Replace strings in files recursively.')
    parser.add_argument('dir_path', type=str, help='The directory path to start replacing strings.')
    parser.add_argument('old_str', type=str, help='The string to be replaced.')
    parser.add_argument('new_str', type=str, help='The new string to replace the old one.')
    parser.add_argument('output_dir', type=str, help='The directory path to copy files and apply changes.')
    parser.add_argument('--ignore_list', type=str, nargs='+', default=DEFAULT_IGNORE_LIST,
                        help='A list of file names to ignore during string replacement.')
    args = parser.parse_args()

    replace_strings_in_dir(args.dir_path, args.old_str, args.new_str, args.output_dir, args.ignore_list)

if __name__ == '__main__':
    main()


# python3 replace_strings.py /path/to/dir foo bar /path/to/output --ignore_list .git .github
