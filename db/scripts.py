import sqlite3

def do(query, *args):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    data = cursor.execute(query, *args).fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data