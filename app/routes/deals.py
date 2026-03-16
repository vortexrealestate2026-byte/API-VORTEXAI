
from celery import Celery

celery = Celery(
    "rocket",
    broker="redis://redis:6379/0"
)
