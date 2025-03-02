from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os
from src.services.csv_validator import CSVValidator
from src.tasks.async_tasks import process_csv_task
from src.models.database import SessionLocal
from src.models.models import ProcessingRequest

router = APIRouter(prefix="/api/v1")


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Save and validate CSV
        content = await file.read()
        temp_path = f"storage/temp/uploads/{request_id}_{file.filename}"
        
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Validate CSV
        validation_result = CSVValidator.validate_csv(temp_path)
        if not validation_result["valid"]:
            return JSONResponse(
                status_code=400,
                content={"error": validation_result["error"]}
            )
        
        # Trigger async processing
        process_csv_task.delay(request_id, temp_path)
        
        return JSONResponse(
            status_code=202,
            content={
                "request_id": request_id,
                "message": "Processing started"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )