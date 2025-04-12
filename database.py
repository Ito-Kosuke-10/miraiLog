import sqlite3

def init_db():
    conn = sqlite3.connect("mirailog.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birthdate TEXT,
            gender TEXT,
            estimated_lifespan INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            goal TEXT,
            deadline TEXT,
            tag TEXT,
            estimated_time TEXT,
            estimated_cost TEXT,
            next_action TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, birthdate, gender, estimated_lifespan):
    conn = sqlite3.connect("mirailog.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, birthdate, gender, estimated_lifespan) VALUES (?, ?, ?, ?)",
              (name, birthdate, gender, estimated_lifespan))
    conn.commit()
    conn.close()

def get_user_id_by_name(name):
    conn = sqlite3.connect("mirailog.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE name = ?", (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_goal(user_id, goal, deadline, tag, time, cost, action):
    conn = sqlite3.connect("mirailog.db")
    c = conn.cursor()
    c.execute('''INSERT INTO goals (user_id, goal, deadline, tag, estimated_time, estimated_cost, next_action)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, goal, deadline, tag, time, cost, action))
    conn.commit()
    conn.close()

def get_goals_by_user(user_id):
    conn = sqlite3.connect("mirailog.db")
    c = conn.cursor()
    c.execute("SELECT goal, deadline, tag, estimated_time, estimated_cost, next_action FROM goals WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows
