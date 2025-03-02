from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery('image_processing', 
                    broker=os.getenv('REDIS_URL'),
                    backend=os.getenv('REDIS_URL'))

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=600,  # 10 minutes
    task_soft_time_limit=500  # Soft timeout
)
