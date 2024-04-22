import sqlite3

# Function to establish a database connection
def connect_to_database():
    conn = sqlite3.connect('agent_database.db')
    return conn

def get_agents():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Retrieve agent records from the database
    cursor.execute('SELECT agent_id, name, status FROM agents')
    agents = cursor.fetchall()

    conn.close()
    return agents

def add_agent(agent_id, role, capabilities):
    conn = connect_to_database()
    cursor = conn.cursor()
    # cursor.execute('''
    #     INSERT INTO agents (agent_id, role, capabilities, status, current_task)
    #     VALUES (?,?,?,?,?)
    # ''', (agent_id, role, capabilities, 'available', ''))
    # conn.commit()
    conn.close()

def get_agent(agent_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agents WHERE agent_id =?', (agent_id,))
    agent = cursor.fetchone()
    conn.close()
    return agent

def update_agent_status(agent_id, status):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('UPDATE agents SET status =? WHERE agent_id =?', (status, agent_id))
    conn.commit()
    conn.close()

def assign_task(agent_id, task_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('UPDATE agents SET current_task =? WHERE agent_id =?', (task_id, agent_id))
    conn.commit()
    conn.close()

def get_available_agents():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agents WHERE status =?', ('available',))
    agents = cursor.fetchall()
    conn.close()
    return agents

def add_task(task_id, description, action_type, details):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_id, description, action_type, details, status, agent_id)
        VALUES (?,?,?,?,?,?)
    ''', (task_id, description, action_type, details, 'pending', ''))
    conn.commit()
    conn.close()

def get_task(task_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE task_id =?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task_status(task_id, status):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status =? WHERE task_id =?', (status, task_id))
    conn.commit()
    conn.close()

def assign_task_to_agent(task_id, agent_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status =?, agent_id =? WHERE task_id =?', ('assigned', agent_id, task_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Create a connection to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Create the agents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            agent_id TEXT PRIMARY KEY,
            role TEXT,
            capabilities TEXT,
            status TEXT,
            current_task TEXT
        )
    ''')

    # Create the tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            description TEXT,
            action_type TEXT,
            details TEXT,
            status TEXT,
            agent_id TEXT
        )
    ''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Test the functions
    add_agent('Pete', 'Python programmer', 'write_code, execute_command')
    add_agent('PeteSon', 'Python programmer', 'write_code, execute_command')
    add_agent('Petester', 'Tester', 'run_tests')

    print(get_agent('Pete'))  # Should print the agent information
    update_agent_status('Pete', 'busy')
    print(get_agent('Pete'))  # Should print the updated status

    add_task('task_123', 'Write a Python script', 'write_code', 'import numpy as np\nprint("Hello, world!")')
    add_task('task_456', 'Run a command', 'execute_command', 'ls -l')

    print(get_task('task_123'))  # Should print the task information

    assign_task_to_agent('task_123', 'PeteSon')
    print(get_task('task_123'))  # Should print the updated task status and agent ID

    assign_task_to_agent('task_456', 'Pete')
    print(get_task('task_456'))  # Should print the updated task status and agent ID