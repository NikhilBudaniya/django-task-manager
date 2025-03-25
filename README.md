# Django Tasks API

A REST API for task management built with Django and Django REST Framework. This project allows creating users, managing tasks, assigning tasks to users, and viewing task statistics.

## Features

- User management (CRUD operations)
- Task management (CRUD operations)
- Task assignments
- Task filtering and search
- Task statistics

## Setup Instructions

### Prerequisites

- Python 3.12+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NikhilBudaniya/django-task-manager.git
   cd djangoTasks
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On macOS/Linux
   source .venv/bin/activate
   # On Windows
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. Apply migrations:
   ```bash
   python manage.py makemigrations tasks
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   # Use these credentials:
   # Name: admin
   # Email: admin@example.com
   # Mobile: 1234567890
   # Password: Admin@123
   ```

3. Create a regular user:
   ```bash
   python manage.py shell
   ```
   ```python
   from tasks.models import User
   User.objects.create_user(name='user', email='user@example.com', mobile='9876543210', password='User@123')
   exit()
   ```

## Running the Application

```bash
python manage.py runserver
```

The API will be accessible at http://127.0.0.1:8000/

## Django Admin Interface

After creating a superuser, you can access the Django admin interface to manage users and tasks:

1. Access the admin interface at: http://127.0.0.1:8000/admin
2. Login with your superuser credentials
3. From here, you can:
   - Create, view, update, and delete users
   - Create, view, update, and delete tasks
   - Assign tasks to users

### Task Types
All valid task types:
- `feature` - New feature implementation
- `bug` - Bug fix
- `enhancement` - Improvement to existing feature
- `maintenance` - Code cleanup, refactoring, etc.

### Task Statuses
All valid task statuses:
- `pending` - Task not started yet
- `in_progress` - Task is being worked on
- `completed` - Task is finished
- `cancelled` - Task has been cancelled

## API Documentation

### User APIs

#### Create User
- **Endpoint**: `POST /users/create/`
- **Request**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "mobile": "9876543210",
    "password": "password123"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 3,
    "name": "John Doe",
    "email": "john@example.com",
    "mobile": "9876543210"
  }
  ```

#### Get All Users
- **Endpoint**: `GET /users/get/all/`
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "Test User 1",
      "email": "testuser1@gmail.com",
      "mobile": "1234567890"
    },
    {
      "id": 2,
      "name": "Test User 2",
      "email": "testuser2@gmail.com",
      "mobile": "1234567890"
    }
  ]
  ```

#### Get User by ID
- **Endpoint**: `GET /users/get/{user_id}/`
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "name": "Test User 1",
    "email": "testuser1@gmail.com",
    "mobile": "1234567890"
  }
  ```

#### Update User
- **Endpoint**: `PUT /users/update/{user_id}/`
- **Request**:
  ```json
  {
    "name": "Updated",
    "mobile": "1023456789"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "name": "Updated",
    "email": "testuser1@gmail.com",
    "mobile": "1023456789"
  }
  ```

#### Delete User
- **Endpoint**: `DELETE /users/delete/{user_id}/`
- **Response** (204 No Content)

### Task APIs

#### Create Task
- **Endpoint**: `POST /tasks/create/`
- **Request**:
  ```json
  {
    "title": "New Test Task",
    "description": "New test task description",
    "status": "pending",
    "task_type": "feature"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 3,
    "title": "New Test Task",
    "description": "New test task description",
    "status": "pending",
    "task_type": "feature",
    "created_at": "2023-05-10T15:30:00Z",
    "completed_at": null
  }
  ```

#### Get All Tasks
- **Endpoint**: `GET /tasks/get/all/`
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "title": "Test Task 1",
      "description": "Description for test task 1",
      "status": "pending",
      "task_type": "feature",
      "created_at": "2023-05-10T14:30:00Z",
      "completed_at": null
    },
    {
      "id": 2,
      "title": "Test Task 2",
      "description": "Description for test task 2",
      "status": "in_progress",
      "task_type": "bug",
      "created_at": "2023-05-10T14:35:00Z",
      "completed_at": null
    }
  ]
  ```

#### Get Task by ID
- **Endpoint**: `GET /tasks/get/{task_id}/`
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "title": "Test Task 1",
    "description": "Description for test task 1",
    "status": "pending",
    "task_type": "feature",
    "created_at": "2023-05-10T14:30:00Z",
    "completed_at": null
  }
  ```

#### Update Task Status
- **Endpoint**: `PATCH /tasks/update/{task_id}/`
- **Request**:
  ```json
  {
    "status": "completed"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "title": "Test Task 1",
    "description": "Description for test task 1",
    "status": "completed",
    "task_type": "feature",
    "created_at": "2023-05-10T14:30:00Z",
    "completed_at": "2023-05-10T16:45:20Z"
  }
  ```

#### Delete Task
- **Endpoint**: `DELETE /tasks/delete/{task_id}/`
- **Response** (204 No Content)

#### Filter Tasks
- **Endpoint**: `GET /tasks/filter/?status=pending&task_type=feature&search=login`
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "title": "Test Task 1",
      "description": "Description for test task 1",
      "status": "pending",
      "task_type": "feature",
      "created_at": "2023-05-10T14:30:00Z",
      "completed_at": null
    }
  ]
  ```

### Task Assignment APIs

#### Assign Task to Users
- **Endpoint**: `POST /tasks/assign/`
- **Request**:
  ```json
  {
    "task_id": 1,
    "user_ids": [2]
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Users assigned to task successfully"
  }
  ```

#### Get Users Assigned to a Task
- **Endpoint**: `GET /tasks/users/{task_id}/`
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "Test User 1",
      "email": "testuser1@gmail.com",
      "mobile": "1234567890"
    },
    {
      "id": 2,
      "name": "Test User 2",
      "email": "testuser2@gmail.com", 
      "mobile": "1234567890"
    }
  ]
  ```

#### Get Tasks Assigned to a User
- **Endpoint**: `GET /users/tasks/{user_id}/`
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "title": "Test Task 1",
      "description": "Description for test task 1",
      "status": "pending",
      "task_type": "feature",
      "created_at": "2023-05-10T14:30:00Z",
      "completed_at": null
    },
    {
      "id": 2,
      "title": "Test Task 2",
      "description": "Description for test task 2",
      "status": "in_progress",
      "task_type": "bug",
      "created_at": "2023-05-10T14:35:00Z",
      "completed_at": null
    }
  ]
  ```

### Task Statistics

- **Endpoint**: `GET /tasks/stats/`
- **Response** (200 OK):
  ```json
  {
    "total_tasks": 2,
    "by_status": {
      "pending": 1,
      "in_progress": 1,
      "completed": 0,
      "cancelled": 0
    },
    "by_type": {
      "feature": 1,
      "bug": 1,
      "enhancement": 0,
      "maintenance": 0
    }
  }
  ```

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run specific test case:
```bash
python manage.py test tasks.tests.TaskAPITestCase
```

Run specific test method:
```bash
python manage.py test tasks.tests.TaskAPITestCase.test_task_create
```

Keep database between test runs (useful for debugging):
```bash
python manage.py test --keepdb
```

## Test Credentials

- **Admin User**:
  - Email: admin@example.com
  - Password: Admin@123
  - Name: Admin
  - Mobile: 1234567890

- **Regular User**:
  - Email: user@example.com
  - Password: User@123
  - Name: user
  - Mobile: 9876543210
