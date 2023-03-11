import os
import shutil

def replace_in_file(filepath, old_str, new_str):
    """Replace old_str with new_str in the contents of a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()
    file_content = file_content.replace(old_str, new_str)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)

def replace_in_dir(source_dir, destination_dir, old_str, new_str, excluded_files=None):
    """Replace old_str with new_str in all file contents and filenames in a directory."""
    if excluded_files is None:
        excluded_files = ['.git']
        
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for item in os.listdir(source_dir):
        # Check if item is excluded
        if item in excluded_files:
            continue
        
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)

        if os.path.isdir(source_path):
            replace_in_dir(source_path, destination_path, old_str, new_str, excluded_files)
        else:
            replace_in_file(source_path, old_str, new_str)
            shutil.copy2(source_path, destination_path)
            
    print(f"Replacement completed for directory {source_dir}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: python replace_files.py <source> <destination> <old_string> <new_string>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    destination_dir = sys.argv[2]
    old_str = sys.argv[3]
    new_str = sys.argv[4]

    if "--exclude-git" in sys.argv:
        excluded_files = ['.git']
    else:
        excluded_files = None

    replace_in_dir(source_dir, destination_dir, old_str, new_str, excluded_files)
