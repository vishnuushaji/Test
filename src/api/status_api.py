from fastapi import APIRouter, HTTPException
from src.models.database import SessionLocal
from src.models.models import ProcessingRequest
import uuid

router = APIRouter(prefix="/api/v1")

@router.get("/status/{request_id}")
def get_processing_status(request_id: str):
    # Validate UUID
    try:
        uuid_obj = uuid.UUID(request_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request ID format")
    
    # Fetch status from database
    db = SessionLocal()
    try:
        request = db.query(ProcessingRequest).filter(
            ProcessingRequest.id == uuid_obj
        ).first()
        
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return {
            "request_id": str(request.id),
            "status": request.status,
            "created_at": request.created_at.isoformat() if request.created_at else None,
            "output_csv_path": request.output_csv_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching status: {str(e)}")
    finally:
        db.close()