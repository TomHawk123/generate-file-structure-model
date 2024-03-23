import os
import fnmatch


def read_ignore_patterns(path):
    """
    Reads ignore patterns from a .structureignore file, if it exists.
    :param path: The path where the .structureignore file is located.
    :return: A list of patterns to ignore.
    """
    ignore_file = os.path.join(path, '.structureignore')
    patterns = []
    if os.path.isfile(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as file:
            patterns = [line.strip()
                        for line in file.readlines() if line.strip() != '']
    return patterns


def should_ignore(entry, ignore_patterns):
    """
    Checks if the entry should be ignored based on the provided patterns.
    :param entry: The directory or file to check.
    :param ignore_patterns: A list of patterns to ignore.
    :return: True if the entry matches any ignore pattern, False otherwise.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(entry, pattern):
            return True
    return False


def print_dir_contents(path, output_file, ignore_patterns, prefix=''):
    dir_entries = sorted(os.listdir(path), key=lambda x: x.lower())
    entries = [e for e in dir_entries if not should_ignore(e, ignore_patterns)]
    full_paths = [os.path.join(path, e) for e in entries]
    files = [f for f in full_paths if os.path.isfile(f)]
    dirs = [d for d in full_paths if os.path.isdir(d)]

    for i, d in enumerate(dirs):
        dir_name = os.path.basename(d)
        if i == len(dirs) - 1 and not files:
            output_file.write(f"{prefix}└── {dir_name}/\n")
            new_prefix = prefix + "    "
        else:
            output_file.write(f"{prefix}├── {dir_name}/\n")
            new_prefix = prefix + "│   "
        print_dir_contents(d, output_file, ignore_patterns, new_prefix)

    for i, f in enumerate(files):
        file_name = os.path.basename(f)
        if i == len(files) - 1:
            output_file.write(f"{prefix}└── {file_name}\n")
        else:
            output_file.write(f"{prefix}├── {file_name}\n")


# Start of the script execution
if __name__ == "__main__":
    root_directory = '.'
    ignore_patterns = read_ignore_patterns(root_directory)

    with open('project_structure.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(root_directory + '\n')
        print_dir_contents(root_directory, output_file, ignore_patterns)
