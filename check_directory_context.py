import os
files = ['json_task_executor.py', 'Dockerfile']
current_directory = os.getcwd()
print(f'Current directory: {current_directory}')
for file in files:
    if os.path.exists(file):
        print(f'File found: {file}')
    else:
        print(f'File not found: {file}')