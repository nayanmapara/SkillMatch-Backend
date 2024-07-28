from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import logging

# Import the AI service
from funcs.ai_service import enhance_resume

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# SQLite setup
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return "Welcome to the SkillMatch-Resume API!"

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        db.execute('INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)',
                   (email, hashed_password, datetime.utcnow().isoformat()))
        db.commit()
        logging.info(f"User {email} created successfully.")
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user['id']}), 200

@app.route('/submit_resume', methods=['POST'])
def submit_resume():
    user_id = request.json.get('user_id')
    resume_content = request.json.get('resume_content')
    job_description = request.json.get('job_description')

    if not user_id or not resume_content or not job_description:
        return jsonify({"error": "User ID, resume content, and job description are required"}), 400

    try:
        # Call the AI to enhance the resume
        enhanced_resume_latex = enhance_resume(resume_content, job_description)

        # Store the original resume in the database
        db = get_db()
        db.execute('INSERT INTO resumes (user_id, content, created_at) VALUES (?, ?, ?)',
                   (user_id, resume_content, datetime.utcnow().isoformat()))
        db.commit()

        logging.info(f"Resume for user {user_id} submitted and enhanced successfully.")
        # Return the enhanced resume LaTeX content
        return jsonify({"enhanced_resume_latex": enhanced_resume_latex}), 200
    except Exception as e:
        logging.error(f"Error enhancing resume: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    init_db()
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
