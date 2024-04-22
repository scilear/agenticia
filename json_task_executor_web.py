import os
import sys
import json
import subprocess
from pathlib import Path
import logging


class CustomHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        append_to_logs(log_message)

# Create a logger
logger = logging.getLogger('JTE')
logger.setLevel(logging.INFO)

# Create console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
    
# Add console handler to logger
logger.addHandler(console_handler)

# Create and add custom handler to logger
custom_handler = CustomHandler()
custom_handler.setFormatter(console_formatter)
logger.addHandler(custom_handler)

import datetime
from flask import Flask, render_template, request, jsonify
import json_task_executor_web

app = Flask(__name__)

logs = []
last_executed_time = None

@app.route('/')
def home():
    return render_template('index.html', last_executed=last_executed_time)

@app.route('/execute', methods=['POST'])
def execute():
    global last_executed_time
    if request.method == 'POST':
        json_text = request.form['json_text']
        if json_text.strip() != '':
            with open('temp.json', 'w') as temp_file:
                temp_file.write(json_text)
            # append_to_logs(json_text)
            process_instructions_file('temp.json')
            last_executed_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            append_to_logs(last_executed_time)
            return jsonify({'message': f"Last executed at {last_executed_time}", 'logs': logs})
    return jsonify({'message': 'No JSON instructions provided.'})

@app.route('/logs')
def get_logs():
    return jsonify(logs)

def append_to_logs(log_entry):
    global logs
    logs.append(log_entry)


def is_safe_path(base_path, target_path, follow_symlinks=True):
    if follow_symlinks:
        return os.path.realpath(target_path).startswith(base_path)
    else:
        return os.path.abspath(target_path).startswith(base_path)

def write_code(base_path, file_path, code):
    full_path = os.path.join(base_path, file_path)
    try:
        if not is_safe_path(base_path, full_path, follow_symlinks=False):
            raise ValueError('Attempted to write outside of the working directory.')

        if os.path.islink(full_path):
            raise ValueError('File path is a symlink. Aborting for security reasons.')

        if os.path.exists(full_path):
            logger.info('File already exists and committing before changing.')
            execute_command(f"git add .")
            execute_command(f"git commit -am 'automated overwrite'")

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            processed_code = bytes(code, 'utf-8').decode('unicode_escape')
            file.write(processed_code)
            logger.info(f'Code written to {full_path}')

    except Exception as e:
        logger.error(f'Error writing code to {full_path}: {str(e)}')
        return {'action': 'write_code', 'file': full_path, 'error': str(e)}

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
        logger.info(f'Executed: {command}')
    except subprocess.CalledProcessError as e:
        error_detail = {
            'action': 'execute_command',
            'command': command,
            'error': str(e),
            'stderr': e.stderr.strip() if e.stderr else 'No stderr output.'
        }
        logger.error(f"Error executing command '{command}': {error_detail}")
        return error_detail

def process_instructions_file(json_file):
    logger.info('Starting task execution from JSON file.')
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
            logger.warning(f"Action {task['action']} is not supported by this executor.")

        if error:
            errors.append(error)
            break

    if 'assumptions' in instructions:
        logger.info('Assumptions:')
        if isinstance(instructions['assumptions'], list):
            for assumption in instructions['assumptions']:
                logger.info(f'- {assumption}')
        elif isinstance(instructions['assumptions'], str):
            logger.info(f"- {instructions['assumptions']}")

    if 'questions' in instructions:
        logger.info('Questions:')
        for question in instructions['questions']:
            logger.info(f'- {question}')

    if errors:
        error_file = f'{json_file[:-5]}_error.json'
        with open(error_file, 'w') as ef:
            json.dump(errors, ef)
        logger.error(f"Errors encountered. Details saved in '{error_file}'")
        print(errors)


if __name__ == '__main__':
    app.run(debug=True)
