from django.test import TestCase, Client
from .models import Job
from .tasks import gpt_job, redis_client
import json
import uuid

class JobTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_job_view(self):
        response = self.client.post('/jobs/', data=json.dumps({
            'guideline_text': 'Test guideline for GPT job'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('event_id', data)

    def test_get_job_status_with_result(self):
        event_id = str(uuid.uuid4())
        status_key = f"status:{event_id}"
        checklist_key = f"checklist:{event_id}"

        redis_client.set(status_key, "COMPLETED")
        checklist = ["Summary", "Item 1", "Item 2"]
        for item in checklist:
            redis_client.rpush(checklist_key, item)

        response = self.client.get(f'/jobs/{event_id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['GPT_job_status'], "COMPLETED")
        self.assertEqual(data['GPT_job_result'], checklist)
