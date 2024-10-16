import os
import argparse

def generate_tree_and_files(root, prefix='', level=0, max_level=3, to_ignore=[], relative_root='.'):
    if level >= max_level:
        return '', []
    tree_str = ''
    files_list = []
    try:
        contents = os.listdir(root)
    except PermissionError:
        contents = []
    contents = [item for item in contents if item not in to_ignore]
    contents.sort()
    if contents:
        pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    else:
        pointers = []
    for pointer, item in zip(pointers, contents):
        path = os.path.join(root, item)
        if os.path.isdir(path):
            tree_str += prefix + pointer + item + '/\n'
            extension = '│   ' if pointer == '├── ' else '    '
            subtree_str, subtree_files = generate_tree_and_files(
                path, prefix + extension, level + 1, max_level, to_ignore, relative_root)
            tree_str += subtree_str
            files_list.extend(subtree_files)
        else:
            tree_str += prefix + pointer + item + '\n'
            relative_path = os.path.relpath(path, relative_root)
            files_list.append(relative_path)
    return tree_str, files_list

def main():
    parser = argparse.ArgumentParser(description='Generate fs tree and content of files and print it to one file')
    parser.add_argument('-l', '--level', type=int, default=3, help='Depth of the tree to consider')
    parser.add_argument('-ignore', '--folders_to_ignore', type=str, default='', help='List of folders to ignore, separated by commas')
    parser.add_argument('-o', '--output_filename', type=str, default='onefile.txt', help='Output filename')
    args = parser.parse_args()

    # Args parsing
    if args.folders_to_ignore:
        to_ignore = [folder.strip() for folder in args.folders_to_ignore.split(',')]
    else:
        to_ignore = []

    level = args.level
    output_filename = args.output_filename

    # Generate fs tree
    tree_str = './\n'
    files_list = []
    start_dir = '.'
    subtree_str, subtree_files = generate_tree_and_files(
        start_dir, prefix='', level=0, max_level=level, to_ignore=to_ignore, relative_root=start_dir)
    tree_str += subtree_str
    files_list.extend(subtree_files)

    # Output file creation
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(tree_str)
        f.write('\n')  # Newline after tree
        for file_path in files_list:
            f.write('\n\n')
            f.write('```\n')
            f.write(f'# {file_path}\n\n')
            try:
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    content = file_content.read()
            except Exception as e:
                content = f'Could not read file content: {e}'
            f.write(content)
            f.write('\n```\n')
    print(f'File "{output_filename}" has been successfully created.')

if __name__ == '__main__':
    main()
