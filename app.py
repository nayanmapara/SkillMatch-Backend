from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pymongo import MongoClient

# Import the AI service
from funcs.ai_service import enhance_resume

load_dotenv()
app = Flask(__name__)

CORS(app)

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB")
db_collection = os.getenv("COLLECTION")
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db[db_collection]
# resumes_collection = db.resumes

@app.route('/')
def index():
    return "Welcome to the SkillMatch-Resume API!"

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    user = {
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    print(users_collection.insert_one(user))

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = users_collection.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200

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
    resume = {
        "user_id": user_id,
        "content": resume_content,
        "created_at": datetime.utcnow().isoformat()
    }
    # resumes_collection.insert_one(resume)

    # Return the enhanced resume LaTeX content
    return jsonify({"enhanced_resume_latex": enhanced_resume_latex}), 200

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000)
