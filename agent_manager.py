def add_agent(agent_id, role, capabilities):
    conn = sqlite3.connect('agent_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agents (agent_id, role, capabilities, status, current_task)
        VALUES (?, ?, ?, ?, ?)
    ''', (agent_id, role, capabilities, 'available', ''))
    conn.commit()
    conn.close()

# Define other agent management functions...