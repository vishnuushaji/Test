# src/middleware/rate_limiter.py
from fastapi import Request, HTTPException
from functools import wraps
import time

class RateLimiter:
    _instances = {}
    
    @classmethod
    def limit(cls, max_requests=100, window=60):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                client_ip = request.client.host
                current_time = time.time()
                
                if client_ip not in cls._instances:
                    cls._instances[client_ip] = []
                
                # Remove old requests
                cls._instances[client_ip] = [
                    req for req in cls._instances[client_ip] 
                    if current_time - req < window
                ]
                
                # Check rate limit
                if len(cls._instances[client_ip]) >= max_requests:
                    raise HTTPException(
                        status_code=429, 
                        detail="Too many requests. Please try again later."
                    )
                
                cls._instances[client_ip].append(current_time)
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator