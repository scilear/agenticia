import json
import os
import subprocess
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("execution.log", mode='w'),
                        logging.StreamHandler()
                    ])

def is_safe_path(base_path, target_path, follow_symlinks=True):
    if follow_symlinks:
        return os.path.realpath(target_path).startswith(base_path)
    else:
        return os.path.abspath(target_path).startswith(base_path)

def write_code(base_path, file_path, code):
    full_path = os.path.join(base_path, file_path)
    try:
        if not is_safe_path(base_path, full_path, follow_symlinks=False):
            raise ValueError("Attempted to write outside of the working directory.")
        
        if os.path.islink(full_path):
            raise ValueError("File path is a symlink. Aborting for security reasons.")
        
        if os.path.exists(full_path):
            user_input = input(f"The file {full_path} already exists. Overwrite? (y/n): ")
            if user_input.lower() != 'y':
                raise FileExistsError("File already exists and overwrite is not allowed.")

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            # Correctly process escape sequences in the code string
            processed_code = bytes(code, "utf-8").decode("unicode_escape")
            file.write(processed_code)
            logging.info(f"Code written to {full_path}")

    except Exception as e:
        logging.error(f"Error writing code to {full_path}: {str(e)}")
        return {"action": "write_code", "file": full_path, "error": str(e)}

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
        logging.info(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        error_detail = {
            "action": "execute_command",
            "command": command,
            "error": str(e),
            "stderr": e.stderr.strip() if e.stderr else "No stderr output."
        }
        logging.error(f"Error executing command '{command}': {error_detail}")
        return error_detail

def main(json_file):
    logging.info("Starting task execution from JSON file.")
    with open(json_file, 'r') as file:
        instructions = json.load(file)
    
    base_path = os.getcwd()
    errors = []

    for task in instructions['response']:
        error = None
        if task['action'] == 'write_code':
            error = write_code(base_path, task['details']['file'], task['details']['code'])
        elif task['action'] == 'command':
            command = task['details']['command']
            error = execute_command(command)
            if error:
                break
        else:
            logging.warning(f"Action {task['action']} is not supported by this executor.")
        
        if error:
            errors.append(error)
            break

    if 'assumptions' in instructions:
        logging.info("Assumptions:")
        if isinstance(instructions['assumptions'], list):
            for assumption in instructions['assumptions']:
                logging.info(f"- {assumption}")
        elif isinstance(instructions['assumptions'], str):
            logging.info(f"- {instructions['assumptions']}")

    if 'questions' in instructions:
        logging.info("Questions:")
        for question in instructions['questions']:
            logging.info(f"- {question}")
    
    if errors:
        error_file = f"{json_file[:-5]}_error.json"
        with open(error_file, 'w') as ef:
            json.dump(errors, ef)
        logging.error(f"Errors encountered. Details saved in '{error_file}'")
        print(errors)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        logging.error("Usage: python json_task_executor.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    if not Path(json_file_path).is_file():
        logging.error(f"The file {json_file_path} does not exist.")
        sys.exit(1)

    if not is_safe_path(os.getcwd(), json_file_path):
        logging.error("The JSON file is not within the working directory. Aborting for security reasons.")
        sys.exit(1)

    main(json_file_path)
