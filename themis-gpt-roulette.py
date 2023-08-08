import os
import random

def delete_random_files(directory):
    # List all .toml files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.toml')]
    
    # Ensure there are at least 5 files
    if len(files) < 10:
        print("There are fewer than 10 .toml files in the directory. No files will be deleted.")
        return

    # Determine the number of files to delete
    num_to_delete = int(len(files) * 0.9)
    
    # Randomly select files to delete
    files_to_delete = random.sample(files, num_to_delete)
    
    # Confirm with the user
    confirm = input(f"Are you sure you want to delete {num_to_delete} .toml files from {directory}? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return

    # Delete the files
    for f in files_to_delete:
        file_path = os.path.join(directory, f)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

    print("Operation completed.")

# Replace 'YOUR_DIRECTORY_PATH' with the path to your directory
directory_path = input("Enter the path of the directory: ")
delete_random_files(directory_path)
