from celery import Celery
import os
broker = os.environ.get("RABBITMQ_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
backend = os.environ.get("REDIS_URL", "redis://redis:6379/0")
celery = Celery("insightx", broker=broker, backend=backend)
