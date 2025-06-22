from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import sys # <-- Import sys

# Add the project's base directory (where manage.py resides) to the Python path.
# This ensures that 'photocart.settings' can be found correctly.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photocart.settings')

app = Celery('photocart')

# Use a string here to avoid issues with workers serializing the configuration object.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()