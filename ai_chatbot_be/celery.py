from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_chatbot_be.settings")

app = Celery("ai_chatbot_be")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()