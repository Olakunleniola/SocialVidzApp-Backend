import asyncio
from functools import wraps

def timeout_wrapper(timeout: float):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"Function '{func.__name__}' timed out after {timeout} seconds.")
        return wrapper
    return decorator
