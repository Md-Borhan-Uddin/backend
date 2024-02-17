import os
import dotenv
from celery import Celery


dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RMS.settings')

app = Celery('RMS')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def debug_task(self):
    print(f'Request: {self}')