from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'database')
DB_NAME = os.getenv('DB_NAME', 'taskdb')
DB_USER = os.getenv('DB_USER', 'taskuser')
DB_PASS = os.getenv('DB_PASS', 'taskpass')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def init_db():
    """Initialize database with tasks table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title, completed, created_at FROM tasks ORDER BY id DESC')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],
                'title': task[1],
                'completed': task[2],
                'created_at': task[3].isoformat() if task[3] else None
            })
        
        return jsonify(task_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        title = data.get('title')
        
        if not title:
            return jsonify({"error": "Title is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING id', (title,))
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"id": task_id, "title": title, "completed": False}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    try:
        data = request.get_json()
        completed = data.get('completed')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET completed = %s WHERE id = %s', (completed, task_id))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Task updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Task deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
