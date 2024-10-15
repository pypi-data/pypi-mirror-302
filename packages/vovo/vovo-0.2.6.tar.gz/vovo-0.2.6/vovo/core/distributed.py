from celery import Celery
from vovo.settings import global_settings


celery_app = Celery(global_settings.CELERY_TASK_NAME)


def configure_celery():

    celery_app.conf.update(broker_url=global_settings.CELERY_BROKER_URL,
                           backend=global_settings.CELERY_RESULT_BACKEND,
                           task_serializer=global_settings.CELERY_TASK_SERIALIZER,
                           timezone='UTC', enable_utc=True)