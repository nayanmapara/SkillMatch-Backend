from flask import Flask, jsonify, request, redirect, send_file
import sqlite3
from dotenv import load_dotenv
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# import subprocess
# import tempfile

# Import the AI service
from funcs.ai_service import enhance_resume

load_dotenv()
app = Flask(__name__)

CORS(app)

db_path = "./db/auth.db"

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect("https://skill-match-resume.vercel.app", code=302)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user:
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    cursor.execute('INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)',
                   (email, hashed_password, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user[2], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user[0]}), 200

@app.route('/submit_resume', methods=['POST'])
def submit_resume():
    user_id = request.json.get('user_id')
    resume_content = request.json.get('resume_content')
    job_description = request.json.get('job_description')

    if not user_id or not resume_content or not job_description:
        return jsonify({"error": "User ID, resume content, and job description are required"}), 400

    # Call the AI to enhance the resume
    enhanced_resume_latex = enhance_resume(resume_content, job_description)

    # Store the original resume in the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resumes (user_id, content, created_at) VALUES (?, ?, ?)',
                   (user_id, resume_content, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    # Return the enhanced resume LaTeX content
    return jsonify({"enhanced_resume_latex": enhanced_resume_latex}), 200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
