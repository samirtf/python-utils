import os


def replace_in_files(src_dir: str, old: str, new: str, skip_git=True) -> None:
    """
    Recursively replaces all occurrences of the string 'old' with the string 'new'
    in all files and directories contained within the source directory 'src_dir'.
    """
    for root, dirs, files in os.walk(src_dir):
        if skip_git and ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            if not file.endswith(".git"):
                replace_in_file(os.path.join(root, file), old, new)
        for dir in dirs:
            if not dir.endswith(".git"):
                replace_in_directory(os.path.join(root, dir), old, new)


def replace_in_file(file_path: str, old: str, new: str) -> None:
    """
    Replaces all occurrences of the string 'old' with the string 'new' in the
    contents of the file specified by 'file_path'. If any replacements are made,
    the modified contents are written back to the file.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
    except (UnicodeDecodeError, PermissionError):
        return
    new_content = content.replace(old, new)
    if new_content != content:
        new_file_path = file_path.replace(old, new)
        with open(new_file_path, 'wb') as f:
            f.write(new_content.encode('utf-8'))
        os.remove(file_path)


def replace_in_directory(dir_path: str, old: str, new: str) -> None:
    """
    Recursively replaces all occurrences of the string 'old' with the string 'new'
    in all files and directories contained within the directory specified by 'dir_path'.
    If any directories are renamed, the renamed directories are processed recursively.
    """
    old_dir_name = os.path.basename(dir_path)
    new_dir_name = old_dir_name.replace(old, new)
    if new_dir_name != old_dir_name:
        try:
            os.rename(dir_path, os.path.join(os.path.dirname(dir_path), new_dir_name))
        except OSError:
            return
    replace_in_files(os.path.join(os.path.dirname(dir_path), new_dir_name), old, new)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Recursively replace string in directory files and directories.")
    parser.add_argument("src_dir", help="source directory")
    parser.add_argument("old", help="string to replace")
    parser.add_argument("new", help="new string")
    parser.add_argument("--skip_git", action="store_true", help="skip .git directories")

    args = parser.parse_args()

    try:
        replace_in_files(args.src_dir, args.old, args.new, args.skip_git)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")
