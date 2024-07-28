## API Documentation

### 1. Signup Route

**Endpoint:** `/signup`  
**Method:** `POST`  
**Content-Type:** `application/json`  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**

- **Success (201 Created)**
    ```json
    {
      "message": "User created successfully"
    }
    ```

- **Error (400 Bad Request)**
    ```json
    {
      "error": "Email and password are required"
    }
    ```
    or
    ```json
    {
      "error": "User already exists"
    }
    ```

- **Error (500 Internal Server Error)**
    ```json
    {
      "error": "Internal server error"
    }
    ```

**Description:**
- Validates the presence of email and password.
- Checks if the user already exists in the database.
- Hashes the password using PBKDF2 with SHA256 and stores the user details in the database.
- Returns appropriate success or error messages based on the outcome.

---

### 2. Login Route

**Endpoint:** `/login`  
**Method:** `POST`  
**Content-Type:** `application/json`  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**

- **Success (200 OK)**
    ```json
    {
      "message": "Login successful",
      "user_id": "user_id_here"
    }
    ```

- **Error (400 Bad Request)**
    ```json
    {
      "error": "Email and password are required"
    }
    ```

- **Error (401 Unauthorized)**
    ```json
    {
      "error": "Invalid email or password"
    }
    ```

**Description:**
- Validates the presence of email and password.
- Checks if the user exists and if the password matches the hashed password stored in the database.
- Returns a success message with the user ID or appropriate error messages if the credentials are invalid.

Here's the documentation for the `/submit_resume` route:


### 3. Submit Resume Route

**Endpoint:** `/submit_resume`  
**Method:** `POST`  
**Content-Type:** `application/json`  

**Request Body:**
```json
{
  "user_id": "user_id_here",
  "resume_content": "Your resume content in plain text",
  "job_description": "The job description for the targeted job"
}
```

**Response:**

- **Success (200 OK)**
    ```json
    {
      "enhanced_resume_latex": "Enhanced resume content in LaTeX format"
    }
    ```

- **Error (400 Bad Request)**
    ```json
    {
      "error": "User ID, resume content, and job description are required"
    }
    ```

- **Error (500 Internal Server Error)**
    ```json
    {
      "error": "Internal server error"
    }
    ```

**Description:**
- Validates that `user_id`, `resume_content`, and `job_description` are provided in the request.
- Calls an AI function to enhance the resume based on the provided content and job description.
- Stores the original resume content in the database (the database insertion is commented out in this snippet).
- Returns the enhanced resume content in LaTeX format or an appropriate error message if there is an issue.

**Notes:**
- Make sure the `enhance_resume` function is properly implemented to handle resume enhancement.
- Uncomment the `resumes_collection.insert_one(resume)` line if you need to store the resume in the database.
