# FastAPI Authentication System

A full-stack authentication application built with FastAPI and React.

## Project Structure

```
fastapi_auth/
├── app/                  # Backend FastAPI application
│   ├── main.py           # Main application entry point
│   ├── routes/            # API routes
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   ├── middlewares/       # Custom middlewares
│   └── ...
├── frontend/              # React frontend application
│   ├── public/            # Static files
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── styles/        # CSS styles
│   │   └── ...
│   └── package.json       # Frontend dependencies
├── package.json           # Root package.json for running both frontend and backend
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi_auth
   ```

2. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   npm run install:frontend
   ```

4. Install root project dependencies:
   ```
   npm install
   ```

## Running the Application

### Development Mode

To run both frontend and backend concurrently:

```
npm start
```

This will start:
- Backend server at http://localhost:8000
- Frontend development server at http://localhost:3000

### Running Separately

To run the backend only:
```
npm run start:backend
```

To run the frontend only:
```
npm run start:frontend
```

## Building for Production

To build the frontend for production:
```
npm run build:frontend
```

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

## Features

- User registration and login
- JWT token authentication
- Email verification
- Password reset functionality
- Protected routes
- Responsive dashboard

## License

ISC

# 🚀 PostgreSQL with Docker – Quick Setup

This project sets up a PostgreSQL database using Docker. It creates a new database, user, and password — perfect for local development.

---

## 📦 Requirements

- [Docker](https://www.docker.com/)
- (Optional) [psql CLI](https://www.postgresql.org/docs/current/app-psql.html) or any SQL GUI like DBeaver / pgAdmin

---

## 🔧 Setup Instructions

### 1. 🐳 Start PostgreSQL in Docker

```bash
docker run --name my-postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -d postgres:14
```

### 2. ✅ Verify It's Running

```bash
docker ps
```

### 3. 🔌 Connect to the Database

Using psql CLI:
```bash
psql -h localhost -U myuser -d mydb
```

Or using a GUI tool like DBeaver or pgAdmin with these connection details:
- Host: localhost
- Port: 5432
- Database: mydb
- Username: myuser
- Password: mypassword

### 4. 🛑 Stop the Container

When you're done:
```bash
docker stop my-postgres
```

### 5. 🗑️ Remove the Container (Optional)

To completely remove the container:
```bash
docker rm my-postgres
```
