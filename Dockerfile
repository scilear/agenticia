FROM python:3.9-slim

WORKDIR /app

# Copy the Python script into the working directory /app
COPY json_task_executor.py .

# Make the Python script executable
RUN chmod +x json_task_executor.py

# Define the volume for external data
VOLUME /app/data

# Set the command to execute the Python script
CMD ["python", "json_task_executor.py", "/app/data/instructions.json"]