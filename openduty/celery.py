from __future__ import absolute_import
import os
import djcelery
from celery import Celery, shared_task
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openduty.settings')
djcelery.setup_loader()

app = Celery('openduty', include=['openduty.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_IMPORTS=['notification.tasks',]
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task
def add(x, y):
    return x + y