from celery import Celery

app = Celery("tasks", broker="redis://redis:6379/0")

app.conf.update(
    broker_connection_retry_on_startup=True
                )

app.autodiscover_tasks(['src.infrastructure.celery.tasks'])
