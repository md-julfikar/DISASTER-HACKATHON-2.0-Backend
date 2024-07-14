from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import get_data
import logging
logger = logging.getLogger(__name__)
def start():
    logger.info("Starting scheduler...")
    scheduler=BackgroundScheduler()
    scheduler.add_job(get_data,'interval', hours=1)
    scheduler.start()