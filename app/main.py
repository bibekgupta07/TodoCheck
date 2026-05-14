# Import FastAPI
from fastapi import FastAPI

# Import CORS middleware to allow frontend access
from fastapi.middleware.cors import CORSMiddleware

# Import our modules
# Use relative imports to avoid module path issues
from .config import settings
from .database import connect_to_mongo, close_mongo_connection
from .core.middleware import LoggingMiddleware, add_custom_headers
from .api import todos


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple Todo API with FastAPI and MongoDB",
    version="1.0.1"
)


# Add CORS middleware
# CORS allows frontend apps from other domains to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (for development)
    allow_credentials=True,    # Allow cookies
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers
)


# Add logging middleware
# This will log every request and response
app.add_middleware(LoggingMiddleware)


# Add custom headers middleware
@app.middleware("http")
async def headers_middleware(request, call_next):
    """Add custom headers to all responses."""
    return await add_custom_headers(request, call_next)


# Startup event - runs when app starts
@app.on_event("startup")
async def startup():
    """
    Connect to MongoDB when application starts.
    """
    print("🚀 Starting Todo API...")
    await connect_to_mongo()
    print(f"✨ API running at http://localhost:{settings.PORT}")
    print(f"📚 Docs available at http://localhost:{settings.PORT}/docs")


# Shutdown event - runs when app stops
@app.on_event("shutdown")
async def shutdown():
    """
    Close MongoDB connection when application stops.
    """
    print("🛑 Shutting down Todo API...")
    await close_mongo_connection()
    print("👋 Goodbye!")


# Root endpoint - health check
@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint.
    Returns basic API information.
    """
    return {
        "message": "Welcome to Todo API",
        "status": "running",
        "docs": "/docs"
    }


# Include todo routes
# All todo endpoints will be under /api/v1/todos
app.include_router(
    todos.router,
    prefix=settings.API_V1_PREFIX
)


# Run the application
# This only runs when you execute: python run.py (from project root)
if __name__ == "__main__":
    import uvicorn
    
    # Note: It's better to use the run.py file in the root directory
    # Or run: uvicorn app.main:app --reload
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )