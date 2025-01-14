from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .middleware import logger
import httpx
from fastapi.exceptions import RequestValidationError


# Custom handler for validation errors
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    for error in exc.errors():
        field_name = error.get("loc")[-1]
        error_message = error.get("msg")
        error_details.append(f"Field '{field_name}' is invalid: {error_message}")
    logger.error(f"Validation Error occurred: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"message": "Request validation failed. Please check your input data.", "details": error_details}
    )

# Custom handler for httpx connection timeouts
async def httpx_timeout_handler(request, exc: httpx.ConnectTimeout):
    logger.error(f"Connection timed out: {str(exc)}")
    return JSONResponse(
        status_code=408,
        content={"detail": "Request timed out. Could not connect to the server. Please try again later."}
    )

# ValueError handler with typo fix
async def value_error_handler(request, exc: ValueError):
    logger.error(f"ValueError: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}  # Corrected the typo here
    )

# Handler for HTTP exceptions
async def httpexceptions_handler(request, exc: HTTPException):
    logger.error(f"HTTPException Error: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail if exc.detail else str(exc)}
    )

# Generic exception handler
async def exception_handler(request, exc: Exception):
    logger.error(f"An unexpected error occurred {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
