import os
import sys
from datetime import datetime

# Get the current date and time for the filename
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Define the output file path in the Documents folder
output_file_path = os.path.expanduser(rf"~\Documents\Specific_File_Export_{formatted_time}.txt")

# Function to extract and write the content of specific files
def extract_specific_files(file_paths):
    try:
        # Open the output file for writing
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        # Get the relative path and file name
                        file_name = os.path.basename(file_path)
                        relative_path = os.path.relpath(file_path)

                        # Read the content of the file
                        with open(file_path, 'r', encoding='utf-8') as file:
                            # Write the file name and content to the output file
                            output_file.write(f"## File: {relative_path}\n")
                            output_file.write(file.read())
                            output_file.write("\n" + "="*40 + "\n")
                    except Exception as e:
                        output_file.write(f"Error reading {file_path}: {e}\n")
                else:
                    output_file.write(f"File not found: {file_path}\n")
            print(f"Export completed: {output_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Main function to handle command-line arguments
if __name__ == "__main__":
    # Check if any file paths are provided in the command-line arguments
    if len(sys.argv) > 1:
        # Get the list of files from the command-line arguments
        file_paths = sys.argv[1:]
        extract_specific_files(file_paths)
    else:
        print("Please provide at least one file path as an argument.")
