# Task Manager API

A modern, production-ready RESTful API for managing tasks and user authentication built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

### Authentication
- ✅ User registration with email verification via OTP
- ✅ Email/password login with JWT tokens
- ✅ Google OAuth 2.0 Sign-in/Sign-up integration
- ✅ Password reset with one-time OTP flow
- ✅ Refresh token support
- ✅ JWT Bearer token authentication

### Task Management
- ✅ Full CRUD operations for tasks
- ✅ Task filtering by status (completed/pending)
- ✅ Task statistics and analytics
- ✅ Pagination support
- ✅ Toggle task completion status
- ✅ User-specific task isolation

### Security
- ✅ Password hashing with bcrypt
- ✅ JWT token validation
- ✅ OAuth2 with Swagger UI integration
- ✅ Email verification OTP
- ✅ Secure one-time OTP codes
- ✅ CORS support

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL/SQLite
- **ORM**: SQLAlchemy
- **Authentication**: JWT, OAuth2, Bcrypt
- **Email**: SMTP
- **API Documentation**: Swagger UI, ReDoc

## Project Structure

```
task/
├── api/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py                 # Database configuration
│   ├── model/
│   │   ├── __init__.py
│   │   ├── user_model.py            # User and VerificationToken models
│   │   └── tasks.py                 # Tasks model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth_schemas.py          # Authentication schemas
│   │   └── task_schemas.py          # Task schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py          # Authentication  logic
│   │   └── task_service.py          # Task CRUD operations
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_route.py            # Authentication endpoints
│   │   └── task_routes.py           # Task endpoints
│   ├── security.py                   # JWT and OAuth2 configuration
│   ├── utils.py                      # Utility functions (email sending)
│
├── migrations/                        # Alembic database migrations
├── main.py                           # FastAPI application entry point
├── requirements.txt                  # Python dependencies
├── alembic.ini                       # Alembic configuration
└── .env                              # Environment variables
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- pip or conda

### Setup

1. **Clone the repository**
   ```bash
   cd task
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # Windows
   # or
   source env/bin/activate      # Unix/MacOS
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/task_manager
   # or for SQLite (development)
   DATABASE_URL=sqlite:///./test.db

   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_MINUTES=60

   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password

   # Google OAuth
   GOOGLE_CLIENT_ID=your-google-client-id

   # Frontend URL
   FRONTEND_URL=http://localhost:3000
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "confirm_password": "SecurePassword123"
}
```

#### Verify Email
```http
POST /api/v1/auth/verify-email
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": 1234
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Google Sign-In
```http
POST /api/v1/auth/google
Content-Type: application/json

{
  "id_token": "google-oauth-token"
}
```

#### Request Password Reset
```http
POST /api/v1/auth/password-reset/request
Content-Type: application/json

{
  "email": "user@example.com"
}
```

You will receive an OTP via email if the account exists.

#### Reset Password with OTP
```http
POST /api/v1/auth/password-reset/verify
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "1234",
  "new_password": "NewPassword123",
  "confirm_password": "NewPassword123"
}
```

#### Check OTP Validity
```http
GET /api/v1/auth/password-reset/check?email=user@example.com&otp=1234
```

### Tasks (Protected - Requires Authorization)

All task endpoints require JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

#### Create Task
```http
POST /api/v1/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

#### Get All Tasks
```http
GET /api/v1/tasks?skip=0&limit=10
Authorization: Bearer <token>
```

#### Get Task by ID
```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer <token>
```

#### Get Completed Tasks
```http
GET /api/v1/tasks/status/completed
Authorization: Bearer <token>
```

#### Get Pending Tasks
```http
GET /api/v1/tasks/status/pending
Authorization: Bearer <token>
```

#### Get Task Statistics
```http
GET /api/v1/tasks/stats/count
Authorization: Bearer <token>

Response:
{
  "status": "success",
  "message": "Task statistics retrieved successfully",
  "data": {
    "total": 10,
    "completed": 7,
    "pending": 3
  }
}
```

#### Update Task
```http
PUT /api/v1/tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "New title",
  "description": "New description",
  "completed": true
}
```

#### Toggle Task Completion
```http
PATCH /api/v1/tasks/{task_id}/toggle
Authorization: Bearer <token>
```

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
Authorization: Bearer <token>
```

#### Delete All Tasks
```http
DELETE /api/v1/tasks
Authorization: Bearer <token>
```

## Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click the "Authorize" button in the top-right
3. Enter your JWT access token in the "Value" field
4. Click "Authorize"
5. All subsequent requests will include your token automatically

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email STRING UNIQUE NOT NULL,
  password STRING,
  google_id STRING UNIQUE,
  is_google_user BOOLEAN DEFAULT FALSE,
  is_verified BOOLEAN DEFAULT FALSE
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY,
  title STRING NOT NULL,
  description STRING,
  completed BOOLEAN DEFAULT FALSE,
  owner_id INTEGER FOREIGN KEY REFERENCES users(id)
);
```

### Verification Tokens Table
```sql
CREATE TABLE verification_tokens (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY REFERENCES users(id),
  otp INTEGER NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME DEFAULT NOW()
);
```

### Password Resets Table
```sql
CREATE TABLE password_resets (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY REFERENCES users(id),
  otp STRING NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME DEFAULT NOW(),
  is_used BOOLEAN DEFAULT FALSE
);
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input or validation error
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `500 Internal Server Error` - Server error

Example error response:
```json
{
  "status": "failure",
  "status_code": 401,
  "message": "Invalid credentials",
  "data": {}
}
```

