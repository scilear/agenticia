# web_interface.py
import datetime
from flask import Flask, render_template, request, jsonify
import json_task_executor

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    if request.method == 'POST':
        json_text = request.form['json_text']
        if json_text.strip() != '':
            with open('temp.json', 'w') as temp_file:
                temp_file.write(json_text)
            json_task_executor.main('temp.json')
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({'message': f"Last executed at {current_time}"})
    return jsonify({'message': 'No JSON instructions provided.'})

# Adding a global variable to track overwrite prompts
# overwrite_prompt_status = None

# @app.route('/overwrite-choice', methods=['POST', 'GET'])
# def overwrite_choice():
#     global overwrite_prompt_status
#     if request.method == 'POST':
#         overwrite_prompt_status = "The file already exists. Do you want to overwrite it?"
#         return jsonify({'prompt': overwrite_prompt_status})
#     elif request.method == 'GET':
#         if overwrite_prompt_status:
#             prompt = overwrite_prompt_status
#             overwrite_prompt_status = None  # Reset after sending
#             return jsonify({'prompt': prompt})
#         else:
#             return jsonify({'prompt': None})

if __name__ == '__main__':
    app.run(debug=True)
