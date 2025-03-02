# main.py
from fastapi import FastAPI
from src.api import upload_api, status_api
from src.models import database

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Image Processing System")

# Include routers
app.include_router(upload_api.router)
app.include_router(status_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.exceptions import CustomAPIException
from src.utils.logger import logger

app = FastAPI()

@app.exception_handler(CustomAPIException)
async def custom_exception_handler(request: Request, exc: CustomAPIException):
    logger.error(f"Custom API Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "details": str(exc)
        }
    )


# main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Image Processing System",
        version="1.0.0",
        description="API for processing images from CSV files",
        routes=app.routes,
    )
    
    # Add custom documentation
    openapi_schema["info"]["x-logo"] = {
        "url": "https://your-logo-url.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi