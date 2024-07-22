from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.start()

    # Пример задачи
    scheduler.add_job(test_job, 'interval', seconds=10)

def test_job():
    print(f"Test job executed at {datetime.now()}")
