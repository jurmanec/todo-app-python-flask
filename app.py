from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize SQLite database
DB_FILE = "tasks.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      description TEXT NOT NULL,
                      status BOOLEAN NOT NULL DEFAULT 0)''')
        conn.commit()
        conn.close()

# Database connection helper
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API: List all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

# API: Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    description = data.get('description')
    if not description:
        return jsonify({"error": "Description is required"}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, status) VALUES (?, 0)", (description,))
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    return jsonify({"id": task_id, "description": description, "status": False}), 201

# API: Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    description = data.get('description')
    status = data.get('status')
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE tasks SET description = ?, status = ? WHERE id = ?", (description, status, id))
    conn.commit()
    conn.close()
    return jsonify({"id": id, "description": description, "status": status})

# API: Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(host='0.0.0.0', port=port, debug=False)
    #app.run(debug=True)