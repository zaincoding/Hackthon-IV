from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from src.config.settings import settings
from src.services.monitoring_service import monitoring_service
from src.utils.errors import handle_exception
from src.models.database import create_tables


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    # Create database tables on startup
    create_tables()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    from src.api.routes.todos import router as todos_router
    from src.api.routes.sessions import router as sessions_router
    from src.api.routes.ai import router as ai_router
    from src.api.routes.auth import router as auth_router

    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(sessions_router, prefix="/api/v1/sessions", tags=["sessions"])
    app.include_router(todos_router, prefix="/api/v1/todos", tags=["todos"])
    app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])

    # Middleware for request logging and monitoring
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            # Log the exception and return an appropriate response
            response = handle_exception(e)
            response = JSONResponse(
                status_code=response.status_code,
                content=response.detail
            )
        process_time = time.time() - start_time

        # Record performance metrics
        monitoring_service.record_request_time(process_time)

        # Add process time to response header
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.get("/health")
    def health_check():
        metrics = monitoring_service.get_metrics()
        return {
            "status": "healthy",
            "service": "todo-chatbot-backend",
            "metrics": {
                "response_time": metrics.get("avg_response_time", 0),
                "error_rate": metrics.get("error_rate", 0),
                "health_status": metrics.get("health_status", "unknown")
            }
        }

    @app.get("/metrics")
    def get_metrics():
        return monitoring_service.get_metrics()

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )