import uuid
from django.db import models

class Job(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    guideline_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
