from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# DB connection
def get_db():
    return sqlite3.connect("database.db")

# Create table (run once)
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            problem TEXT,
            topic TEXT,
            status TEXT,
            time_spent INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", data=data)

# Add record
@app.route('/add', methods=['POST'])
def add():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO practice (date, problem, topic, status, time_spent)
        VALUES (?, ?, ?, ?, ?)
    """, (data['date'], data['problem'], data['topic'], data['status'], data['time']))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete record
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM practice WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# API (for Postman)
@app.route('/api/data')
def api_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)