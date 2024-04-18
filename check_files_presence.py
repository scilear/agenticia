import os

files_to_check = ['json_task_executor.py', 'Dockerfile']
for file_name in files_to_check:
    if os.path.exists(file_name):
        print(f'{file_name} is present.')
    else:
        print(f'{file_name} is missing.')