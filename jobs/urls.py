from django.urls import path
from .views import create_job, get_job_status

urlpatterns = [
    path('', create_job),
    path('<uuid:event_id>/', get_job_status),
]
