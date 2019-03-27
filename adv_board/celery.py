from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adv_platform.settings')

app = Celery('adv_platform')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update({'beat_schedule': {
    'check_expiration_time': {
        'task': 'adv_board.tasks.flag_expired',
        'schedule': crontab(hour='*/12'),  # minute='2, 35' << only 2nd and 35th minute of an hour
        'args': ('', )
        },
    }
})   # accepts a dict with configurations

app.conf.timezone = 'UTC'
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
