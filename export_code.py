import os

def export_folder_contents(directory, ignore_folders):
    output = f"Directory:\n"
    for root, dirs, files in os.walk(directory):
        # Skip the ignored folders
        if any(folder in root.split(os.path.sep) for folder in ignore_folders):
            continue
        for file in files:
            if file.endswith(".py") or file.endswith(".html") or file.endswith(".css"):
                output += f"{os.path.join(root, file)}\n"
    output += "\n"
    
    for root, dirs, files in os.walk(directory):
        # Skip the ignored folders
        if any(folder in root.split(os.path.sep) for folder in ignore_folders):
            continue
        for file in files:
            if file.endswith(".py") or file.endswith(".html") or file.endswith(".css"):
                file_path = os.path.join(root, file)
                output += f"- File {file_path}:\n\n"
                with open(file_path, "r") as f:
                    output += f.read()
                output += "\n\n"
    
    return output

# Example usage
directory = "."
ignore_folders = ["archive", "temp", "flask_env", "bin", "lib", "lib64", "include"]
result = export_folder_contents(directory, ignore_folders)
print(result)