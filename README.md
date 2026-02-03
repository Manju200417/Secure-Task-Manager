# Task Manager – Backend Developer Internship Project

This project is a simple task management system built to demonstrate backend development fundamentals such as authentication, role-based access control, RESTful API design, and frontend–backend integration.

The project runs in **two parts**:

1. Backend (Flask REST API)
2. Frontend (HTML, CSS, JavaScript)

Both parts are included in this repository and are explained in this README.

---

## Tech Stack

### Backend

- Python 3
- Flask
- SQLite
- JWT Authentication
- bcrypt / Werkzeug for password hashing

### Frontend

- HTML
- CSS
- JavaScript (Vanilla)

---

## Features

- User registration and login
- Secure password hashing
- JWT-based authentication
- Role-based access control (User and Admin)
- CRUD operations for tasks
- Users can manage only their own tasks
- Admin can view and delete all users and tasks
- API versioning using `/api/v1`
- Proper HTTP status codes and error handling
- Basic request and error logging
- Simple frontend to test APIs

---

## Project Structure

```
intern-project/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── utils/
│   │   └── auth_helper.py
│   ├── logs/
│   │   └── app.log
│   ├── users.db
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

## API Endpoints

### Authentication

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/v1/register`      | Register a new user              |
| POST   | `/api/v1/login`         | Login and receive a JWT token    |

### Tasks *(JWT required)*

| Method | Endpoint                | Description                                          |
|--------|-------------------------|------------------------------------------------------|
| POST   | `/api/v1/tasks`         | Create a task                                        |
| GET    | `/api/v1/tasks`         | Get tasks (user gets own, admin gets all)            |
| DELETE | `/api/v1/tasks/<id>`    | Delete a task                                        |

### Users *(Admin only)*

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| GET    | `/api/v1/users`         | View all users                   |
| DELETE | `/api/v1/users/<id>`    | Delete a user                    |

All protected endpoints require a JWT token in the request header:

```
Authorization: Bearer <token>
```

---

## Running the Project

This project runs in **two parts** — backend and frontend. Follow the steps below to run both.

---

### Step 1: Run the Backend

1. Navigate to the backend directory:

```bash
cd intern-project/backend
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install backend dependencies:

```bash
pip install -r requirements.txt
```

4. Start the backend server:

```bash
python app.py
```

The backend server will run at:

```
http://127.0.0.1:5000
```

> Keep this terminal running.

---

### Step 2: Run the Frontend

1. Open a new terminal window.
2. Navigate to the frontend directory:

```bash
cd intern-project/frontend
```

3. Open the frontend in a browser:

```bash
open index.html
```

You can also open `index.html` directly by double-clicking it.

---

## Usage Flow

1. Start the backend server.
2. Open the frontend in a browser.
3. Register a new user.
4. Login to access the dashboard.
5. Create, view, and delete tasks.
6. Admin users can manage all users and tasks.

---

## Security Notes

- Passwords are hashed before storing.
- JWT authentication is required for protected routes.
- Role-based access is enforced at the API level.
- Input validation and error handling are implemented.

---

## Scalability Notes

- SQLite can be replaced with PostgreSQL or MySQL.
- Redis can be added for caching.
- Docker can be used for containerization.
- Services can be separated into authentication and task modules.
- Load balancing can be added for horizontal scaling.