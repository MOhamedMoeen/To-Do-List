# Todo List App

A simple Todo List web application built with **Flask** and **SQLite**.

## Features
- Add, update, and delete tasks.
- Mark tasks as **pending** or **done**.
- Sort tasks by **time** or **priority**.
- Filter tasks based on their status.
- User authentication (register, login, logout).

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/To-Do-List.git
   ```
2. Navigate to the project directory:
   ```
   cd To-Do-List
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open your browser and go to http://127.0.0.1:5000/

## Usage
- Register a new user and login.
- Add tasks using the input form.
- Use the dropdown to sort or filter tasks.
- Click on a task to mark it as done or delete it.

## API Endpoints

### POST /register  
Register a new user.  

**Request body example:**  
```
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response example:**  
```
{
  "message": "User registered successfully"
}
```

---

### GET /tasks  
Fetch all tasks for the logged-in user.  

**Response example:**  
```
[
  {
    "id": 1,
    "task": "Buy groceries",
    "status": "pending",
    "priority": "high",
    "time": "2025-09-10T16:00:00"
  },
  {
    "id": 2,
    "task": "Clean room",
    "status": "done",
    "priority": "medium",
    "time": "2025-09-10T12:30:00"
  }
]
```

## License
This project is open-source and free to use.
