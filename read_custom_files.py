import os
from datetime import datetime

# Define the file extensions you're interested in
FILE_EXTENSIONS = [".py", ".json", ".yaml", ".yml", ".js", ".html", ".sh"]

# Get the current date and time for the filename
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Define the output file path in the Documents folder
output_file_path = os.path.expanduser(rf"~\Documents\Content_Export_Stark_energy_monitor_{formatted_time}.txt")

# Function to generate a tree-like structure of the directory
def generate_file_tree(directory):
    file_tree = []
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d != '.git']  # Exclude .git
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        subdir = os.path.basename(root)
        file_tree.append(f"{indent}{subdir}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                file_tree.append(f"{sub_indent}{file}")
    return "\n".join(file_tree)

# Function to read files and export the content in a structured format
def read_files_in_directory(directory):
    try:
        # Open the output file for writing
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Write the file tree structure at the top
            output_file.write("# Directory Structure:\n")
            output_file.write(generate_file_tree(directory))
            output_file.write("\n" + "="*40 + "\n\n")

            # Iterate through the directory and write file contents
            for root, dirs, files in os.walk(directory):
                # Skip .git directory
                dirs[:] = [d for d in dirs if d != '.git']  # Exclude .git
                for file in files:
                    if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                        filepath = os.path.join(root, file)
                        try:
                            # Extract the relative file path
                            relative_path = os.path.relpath(filepath, directory)
                            with open(filepath, 'r', encoding='utf-8') as f:
                                # Write the file name and contents
                                output_file.write(f"## File: {relative_path}\n")
                                output_file.write(f.read())
                                output_file.write("\n" + "="*40 + "\n")
                        except Exception as e:
                            output_file.write(f"Error reading {relative_path}: {e}\n")
            print(f"Export completed: {output_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Get the current directory the script is in
current_directory = os.getcwd()

# Call the function with the current working directory
read_files_in_directory(current_directory)
