from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'convertly.settings')

app = Celery('convertly', broker_connection_retry_on_startup=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'clean-up every 5 min all files':{
#         'task': 'convertor.tasks.cleanup_files',
#         'schedule': 300.0
#     }
# }

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)