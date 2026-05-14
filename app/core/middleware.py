# Import FastAPI Request type
from fastapi import Request

# Import time module to measure request duration
import time

# Import BaseHTTPMiddleware to create custom middleware
from starlette.middleware.base import BaseHTTPMiddleware


# What is Middleware?
# Middleware is code that runs BEFORE and AFTER each request
# Think of it like a security checkpoint or logger that sees every request


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests and responses.
    Logs method, path, status code, and duration.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        This function runs for EVERY request to the API.
        
        Args:
            request: The incoming HTTP request
            call_next: Function to call the actual endpoint handler
            
        Returns:
            Response from the endpoint
        """
        
        # Record start time to calculate request duration
        start_time = time.time()
        
        # Get request information
        method = request.method           # GET, POST, PUT, DELETE, etc.
        path = request.url.path          # /api/v1/todos/
        client_ip = request.client.host if request.client else "unknown"
        
        # Log incoming request
        print(f"🔵 {method} {path} from {client_ip}")
        
        # Call the actual endpoint handler and get response
        # This is where your API endpoint code runs
        response = await call_next(request)
        
        # Calculate how long the request took
        duration = time.time() - start_time
        
        # Log response with status code and duration
        print(f"✅ {method} {path} - {response.status_code} - {duration:.4f}s")
        
        # Return the response to the client
        return response


async def add_custom_headers(request: Request, call_next):
    """
    Middleware function to add custom headers to all responses.
    Alternative way to create middleware without a class.
    
    Args:
        request: Incoming HTTP request
        call_next: Function to call next handler
        
    Returns:
        Response with custom headers added
    """
    
    # Process the request
    response = await call_next(request)
    
    # Add custom headers to response
    response.headers["X-API-Version"] = "1.0.0"
    response.headers["X-Custom-Header"] = "Todo-API"
    
    return response