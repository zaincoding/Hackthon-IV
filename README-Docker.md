# Running the Application with Docker Desktop

This guide explains how to run the full-stack application using Docker Desktop.

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of RAM allocated to Docker

## Quick Start

1. Make sure Docker Desktop is running on your machine.

2. From the project root directory, run:

```bash
docker-compose up --build
```

This will:
- Build the backend and frontend containers
- Start PostgreSQL and Redis databases
- Link all services together
- Make the frontend available at http://localhost:3000
- Make the backend API available at http://localhost:8000

3. To stop the application, press `Ctrl+C` in the terminal.

4. To stop and remove containers, networks, and volumes:

```bash
docker-compose down -v
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

## Troubleshooting

- If you encounter issues with the build, try clearing Docker's cache:
  ```bash
  docker system prune -a
  ```

- If the frontend can't connect to the backend, make sure the `NEXT_PUBLIC_API_URL` in the docker-compose.yml points to the correct backend service name.

- For database migrations or initialization, you may need to run additional commands in the backend container:
  ```bash
  docker-compose exec backend python manage.py migrate  # Example command
  ```