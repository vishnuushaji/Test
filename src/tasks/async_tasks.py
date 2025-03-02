# src/tasks/async_tasks.py
from src.tasks.celery_config import celery_app
from src.services.csv_validator import CSVValidator
from src.services.image_processor import ImageProcessor
from src.models.database import SessionLocal
from src.models.models import ProcessingRequest
import pandas as pd
import requests
import os
import uuid

@celery_app.task(bind=True)
def process_csv_task(self, request_id: str, input_csv_path: str):
    db = SessionLocal()
    try:
        # Update status to processing
        processing_request = db.query(ProcessingRequest).filter(
            ProcessingRequest.id == uuid.UUID(request_id)
        ).first()
        processing_request.status = 'PROCESSING'
        db.commit()

        # Read CSV
        df = pd.read_csv(input_csv_path)
        output_rows = []

        # Process each row
        for index, row in df.iterrows():
            product_name = row['Product Name']
            image_urls = row['Input Image Urls'].split(',')
            
            processed_urls = []
            for url_index, url in enumerate(image_urls):
                try:
                    # Download and process image
                    image = ImageProcessor.download_image(url.strip())
                    compressed_image = ImageProcessor.compress_image(image)
                    
                    # Save processed image
                    saved_path = ImageProcessor.save_image(
                        compressed_image, 
                        product_name, 
                        url_index
                    )
                    processed_urls.append(saved_path)
                except Exception as e:
                    print(f"Error processing image {url}: {str(e)}")
                    processed_urls.append(None)
            
            # Prepare output row
            output_row = row.to_dict()
            output_row['Output Image Urls'] = ','.join(processed_urls)
            output_rows.append(output_row)
        
        # Create output CSV
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_csv_path = os.path.join(output_dir, f"{request_id}_output.csv")
        
        output_df = pd.DataFrame(output_rows)
        output_df.to_csv(output_csv_path, index=False)

        # Update database
        processing_request.status = 'COMPLETED'
        processing_request.output_csv_path = output_csv_path
        db.commit()

        # Trigger webhook
        trigger_webhook(request_id, 'COMPLETED')

        return {
            "request_id": request_id,
            "status": "COMPLETED",
            "output_csv_path": output_csv_path
        }

    except Exception as e:
        # Update status to failed
        processing_request.status = 'FAILED'
        db.commit()
        
        # Trigger webhook
        trigger_webhook(request_id, 'FAILED')
        
        # Re-raise to let Celery handle the error
        raise self.retry(exc=e, max_retries=3)
    finally:
        db.close()

def trigger_webhook(request_id: str, status: str):
    webhook_url = os.getenv('WEBHOOK_ENDPOINT')
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={
                "request_id": request_id,
                "status": status
            })
            response.raise_for_status()
        except Exception as e:
            print(f"Webhook trigger failed: {str(e)}")