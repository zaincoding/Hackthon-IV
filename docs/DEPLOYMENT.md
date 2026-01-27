# Deployment Guide for AI-Powered Todo Chatbot

## Overview
This document provides instructions for deploying the AI-Powered Todo Chatbot application.

## Prerequisites
- Docker and Docker Compose
- Access to OpenAI API (API key)
- At least 2GB RAM available
- Port 3000 and 8000 available

## Environment Variables
Create a `.env` file in the root directory with the following variables:

```bash
# Backend Configuration
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key_here
HOST=0.0.0.0
PORT=8000

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key_here
```

## Deployment Methods

### Method 1: Docker Compose (Recommended)
1. Ensure you have Docker and Docker Compose installed
2. Place your `.env` file in the root directory
3. Run the following command:
   ```bash
   docker-compose up -d
   ```
4. The application will be available at `http://localhost:3000`

### Method 2: Manual Deployment
1. **Backend Setup:**
   - Navigate to the `backend` directory
   - Create a virtual environment: `python -m venv venv`
   - Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
   - Install dependencies: `pip install -r requirements.txt`
   - Set environment variables
   - Start the server: `python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000`

2. **Frontend Setup:**
   - Navigate to the `frontend` directory
   - Install dependencies: `npm install`
   - Set environment variables
   - Build the application: `npm run build`
   - Start the server: `npm start`

## Configuration Options

### Backend Settings
- `HOST`: Host address for the backend server (default: 0.0.0.0)
- `PORT`: Port for the backend server (default: 8000)
- `DEBUG`: Enable debug mode (default: False)
- `SESSION_TIMEOUT_HOURS`: Session timeout in hours (default: 24)
- `MAX_TODOS_PER_SESSION`: Maximum todos per session (default: 1000)

### Frontend Settings
- `NEXT_PUBLIC_BACKEND_URL`: URL of the backend server
- `NEXT_PUBLIC_OPENAI_API_KEY`: OpenAI API key (if needed on frontend)

## Health Checks
- Backend health: `GET /health` (returns service status and metrics)
- Backend metrics: `GET /metrics` (returns detailed system metrics)

## Security Considerations
- Store API keys securely and never commit them to version control
- Use HTTPS in production environments
- Regularly rotate API keys
- Monitor application logs for suspicious activity
- Validate all user inputs

## Scaling Recommendations
- For higher loads, consider using a dedicated Redis instance
- Use a proper database instead of in-memory storage for production
- Implement CDN for static assets
- Use load balancers for multiple instances

## Troubleshooting
- If the application fails to start, check that all environment variables are set
- Check logs with `docker-compose logs` if using Docker
- Ensure ports 3000 and 8000 are not in use by other applications
- Verify your OpenAI API key is valid and has sufficient quota