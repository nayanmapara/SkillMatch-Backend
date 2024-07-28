from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pymongo import MongoClient
import logging

# Import the AI service
from funcs.ai_service import enhance_resume

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# MongoDB setup
mongo_uri = os.environ["MONGODB_URI"]
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

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    user = {
        "email": email,
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        users_collection.insert_one(user)
        logging.info(f"User {email} created successfully.")
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid email"}), 401

    return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200


@app.route('/submit_resume', methods=['POST'])
def submit_resume():
    resume_content = request.json.get('resume_content')
    job_description = request.json.get('job_description')

    if not resume_content or not job_description:
        return jsonify({"error": "Resume content and job description are required"}), 400

    try:
        # Call the AI to enhance the resume
        enhanced_resume_latex = enhance_resume(resume_content, job_description)

        # Store the original resume in the database
        resume = {
            "content": resume_content,
            "created_at": datetime.utcnow().isoformat()
        }
        # resumes_collection.insert_one(resume)  # Uncomment if needed

        logging.info(f"Resume submitted and enhanced successfully.")
        # Return the enhanced resume LaTeX content
        return jsonify({"enhanced_resume_latex": enhanced_resume_latex}), 200
    except Exception as e:
        logging.error(f"Error enhancing resume: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000)
