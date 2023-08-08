import os
import random
import shutil

def copy_random_files(source_directory, target_directory):
    # Check if target directory exists, if not, create it
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # List all .toml files in the source directory
    files = [f for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f)) and f.endswith('.toml')]
    
    # Determine the number of files to copy: 10 or all of them if fewer than 10
    num_to_copy = min(10, len(files))
    
    # Randomly select files to copy
    files_to_copy = random.sample(files, num_to_copy)

    # Copy the files
    for f in files_to_copy:
        source_path = os.path.join(source_directory, f)
        destination_path = os.path.join(target_directory, f)
        shutil.copy(source_path, destination_path)

    print("Operation completed.")

# Input paths
source_directory_path = input("Enter the path of the directory to COPY .toml files FROM: ")
target_directory_path = input("Enter the path of the directory to COPY .toml files TO: ")

copy_random_files(source_directory_path, target_directory_path)
