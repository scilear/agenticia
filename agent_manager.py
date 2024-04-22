import sqlite3

# Create a connection to the database
conn = sqlite3.connect('agent_database.db')
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

# Commit the changes
conn.commit()

# Close the connection
conn.close()