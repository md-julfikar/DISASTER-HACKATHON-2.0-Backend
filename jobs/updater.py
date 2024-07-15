from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from .jobs import get_data
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

def job_listener(event):
    if event.exception:
        logger.error(f"Job {event.job_id} failed: {event.exception}")
    else:
        logger.info(f"Job {event.job_id} executed successfully at {datetime.now()}")

def start():
    try:
        print("......Job started succesfully.....")
        logger.info("Starting scheduler...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(get_data, 'interval', minutes=60)
        
        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        
        scheduler.start()
        logger.info("Scheduler started successfully.")
        
        # from django.core.signals import request_finished
        # from django.db import connection

        # def close_scheduler(**kwargs):
        #     logger.info("Stopping scheduler...")
        #     scheduler.shutdown()
        #     logger.info("Scheduler stopped.")

        # request_finished.connect(close_scheduler)
    except Exception as e:
        logger.error(f"Failed to start the scheduler: {e}")
