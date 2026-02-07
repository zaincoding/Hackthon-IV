# Running the Application Locally Without Docker

This guide explains how to run the application directly on your machine without Docker, which allows you to test functionality like login, registration, authentication, and task creation with Neon database.

## Prerequisites

- Python 3.11 installed
- Node.js 18+ installed
- npm or yarn package manager
- Access to a PostgreSQL database (Neon or local)
- An OpenAI API key

## Backend Setup (Python/FastAPI)

### 1. Navigate to the backend directory
```bash
cd backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Then edit the `.env` file to add your OpenAI API key and database connection:
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
DATABASE_URL=postgresql://username:password@neon_project_endpoint.neon.tech/db_name
```

### 5. Run the backend server
```bash
python -m uvicorn src.api.main:app --reload
```

The backend will be available at http://localhost:8000

## Frontend Setup (Next.js/React)

### 1. Navigate to the frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Set up environment variables
Create a `.env.local` file based on `.env.local.example`:
```bash
cp .env.local.example .env.local
```

Edit the `.env.local` file to point to your backend:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Run the frontend development server
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Neon Database Setup

### 1. Create a Neon account
- Go to https://neon.tech/
- Sign up for a free account

### 2. Create a new project
- Click "New Project"
- Choose your region and PostgreSQL version
- Note down the connection details

### 3. Update your backend .env file
Replace the DATABASE_URL in your backend `.env` file with the connection string from Neon:
```bash
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Testing Application Features

Once both the backend and frontend are running:

1. **Access the frontend**: Open http://localhost:3000 in your browser
2. **API Documentation**: Check the backend API at http://localhost:8000/docs
3. **Health Check**: Verify the backend is running at http://localhost:8000/health

### Available API Endpoints:
- `GET /health` - Health check
- `POST /api/v1/sessions/` - Create new session
- `GET /api/v1/sessions/{session_id}` - Get session info
- `DELETE /api/v1/sessions/{session_id}` - Delete session
- `GET/POST /api/v1/todos/` - Todo operations
- `POST /api/v1/ai/` - AI processing

## Troubleshooting

- If you get database connection errors, verify your Neon database settings and connection string
- If the frontend can't connect to the backend, check that both services are running and the NEXT_PUBLIC_API_URL is set correctly
- For OpenAI errors, verify your API key is correct and has sufficient credits
- Check the console logs in both terminals for specific error messages

## Development Workflow

- The backend supports hot reloading when you make changes (if RELOAD=True in .env)
- The frontend also supports hot reloading during development
- You can access the FastAPI documentation at http://localhost:8000/docs to test API endpoints directly