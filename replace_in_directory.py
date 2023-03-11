import os

def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as f:
        content = f.read()
    
    content = content.replace(old_string, new_string)
    
    with open(file_path, 'w') as f:
        f.write(content)

def replace_file_name(file_path, old_string, new_string):
    dir_path = os.path.dirname(file_path)
    old_name = os.path.basename(file_path)
    new_name = old_name.replace(old_string, new_string)
    new_path = os.path.join(dir_path, new_name)
    os.rename(file_path, new_path)

def replace_in_directory(dir_path, old_string, new_string):
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            file_path = os.path.join(root, name)
            replace_string_in_file(file_path, old_string, new_string)
            replace_file_name(file_path, old_string, new_string)
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            replace_in_directory(dir_path, old_string, new_string)
            replace_file_name(dir_path, old_string, new_string)

# Example usage:
replace_in_directory('/path/to/directory', 'old_string', 'new_string')
