from celery import Celery

celery_app = Celery("worker", backend="amqp", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
