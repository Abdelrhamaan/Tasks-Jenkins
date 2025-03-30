# urls.py
from django.urls import path
from .views import trigger_jenkins_build

urlpatterns = [
    path('trigger-build/<int:task_id>/', trigger_jenkins_build, name='trigger_jenkins_build'),
]
