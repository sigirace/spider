import os
from celery import Celery
from django.conf import settings

# Django 설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("spider")

# Celery 설정 가져오기
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery 설정 추가
app.conf.update(broker_connection_retry_on_startup=True)  # 이 설정을 추가하여 경고 해결


# 디버그용 테스트 태스크
@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
