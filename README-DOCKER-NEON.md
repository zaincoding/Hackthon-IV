# Running the Application with Docker Desktop - Enhanced Configuration

This guide explains how to run the full-stack application using Docker Desktop with flexible database configuration options.

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of RAM allocated to Docker

## Quick Start with Local PostgreSQL (Default)

1. Make sure Docker Desktop is running on your machine.

2. From the project root directory, run:

```bash
docker-compose up --build
```

This will:
- Build the backend and frontend containers
- Start PostgreSQL and Redis databases locally
- Link all services together
- Make the frontend available at http://localhost:3000
- Make the backend API available at http://localhost:8000

## Quick Start with Neon Database

1. Make sure Docker Desktop is running on your machine.

2. Set up your Neon database connection in the .env file (see "Environment Configuration" below)

3. From the project root directory, run:

```bash
docker-compose -f docker-compose.neon.yml up --build
```

This will:
- Build the backend and frontend containers
- Connect to the Neon PostgreSQL database (external)
- Start Redis locally for caching/session storage
- Link all services together
- Make the frontend available at http://localhost:3000
- Make the backend API available at http://localhost:8000

## Environment Configuration

### Option 1: Using the .env file (Recommended)
Copy the provided .env file and modify the DATABASE_URL as needed:

```bash
cp .env.example .env
# Edit .env to set your desired DATABASE_URL
```

The default .env uses local PostgreSQL. To use Neon, uncomment and modify the Neon DATABASE_URL line.

### Option 2: Using environment variables
You can also set the DATABASE_URL directly when running Docker Compose:

```bash
DATABASE_URL="your_neon_connection_string_here" docker-compose up --build
```

## Alternative: Run Individual Services

If you prefer to run just one service at a time:

### Backend Only
```bash
docker-compose up --build backend
```

### Frontend Only (after starting backend separately)
```bash
docker-compose up --build frontend
```

## Database Options Explained

### Local PostgreSQL (Default)
- Runs PostgreSQL in a Docker container
- Data persists in Docker volumes
- Good for development and testing
- Connection: `postgresql://user:password@db:5432/todo_db`

### Neon Database
- Cloud-hosted PostgreSQL service
- Production-ready, scalable
- Good for production or cloud-based development
- Connection: `postgresql://username:password@endpoint/project?sslmode=require`

## Troubleshooting

- If you encounter issues with the build, try clearing Docker's cache:
  ```bash
  docker system prune -a
  ```

- If the frontend can't connect to the backend, make sure the `NEXT_PUBLIC_API_URL` in the docker-compose.yml points to the correct backend service name.

- For database migration issues when switching between local and Neon DB, you may need to run initialization commands in the backend container:
  ```bash
  docker-compose exec backend python init_db.py
  ```

- When switching from local to Neon database, ensure your Neon database has the correct schema. You may need to run initialization scripts to create the required tables.

- If you get SSL connection errors with Neon database, ensure your connection string includes `sslmode=require`.