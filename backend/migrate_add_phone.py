import sqlite3

# Path to your SQLite database
DB_PATH = 'learnex.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

try:
    c.execute('ALTER TABLE students ADD COLUMN phone TEXT;')
    print('Column phone added.')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Column phone already exists.')
    else:
        print('Error:', e)

conn.commit()
conn.close()
