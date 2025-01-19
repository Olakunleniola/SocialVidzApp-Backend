import asyncio
from functools import wraps
import httpx

def timeout_wrapper(timeout: float):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                raise httpx.ConnectTimeout(f"Function '{func.__name__}' timed out after {timeout} seconds.")
        return wrapper
    return decorator
