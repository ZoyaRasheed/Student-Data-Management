# Student Management System

## Description
The Student Management System allows teachers and students to interact through a web-based platform. Teachers can log in to add marks, and students can log in to view their marks.

## Features
- Teacher login
- Student login
- Teachers can add marks
- Students can view marks


## Installation and Setup

### Prerequisites
- Python 3.x installed
- Pip installed

### Steps to Start
1. **Navigate to the server directory:**
```bash
cd server
```

2. **Create a virtual environment:**
```bash
python3 -m venv env
# or
python -m venv env
```

3. **Activate the virtual environment:**
```bash
source env/bin/activate
# or (for Windows)
.env\\Scripts\\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Apply database migrations:**
```bash
python manage.py migrate
```
6. **Create a `.env` file in the root directory:**
```plaintext
MONGO_DB_URL = ""
```

7. **Seed the database:**
```bash
python seeder.py
```
(This will create initial classes, subjects, and roles)

8. **Start the development server:**
```bash
python manage.py runserver
```

Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Using API for Testing

1. Open the `api.http` file in a REST client (such as the VS Code REST Client extension).
2. Use the provided API endpoints to test various functionalities like login, adding marks, and viewing marks.

---

## Technology Stack
- Backend: Django
- API: Django REST Framework
- Database: Mongodb

