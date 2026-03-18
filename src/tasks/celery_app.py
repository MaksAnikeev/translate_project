from celery import Celery

from src.config import settings


celery_instance = Celery(
    main="tasks", broker=settings.RADIS_URL, include=["src.tasks.tasks"]
)
