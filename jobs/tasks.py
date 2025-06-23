# SPDX-License-Identifier: MIT OR Apache-2.0

from celery import shared_task
from redis import Redis

redis_client = Redis(host='redis', port=6379, db=0)

@shared_task(bind=True)
def gpt_job(self, event_id, guideline_text):
    status_key = f"status:{event_id}"
    checklist_key = f"checklist:{event_id}"

    redis_client.set(status_key, "IN_PROGRESS")

    summary = f"Summary of: {guideline_text[:50]}..."
    checklist = [
        summary,
        "Checklist Item 1 based on guideline",
        "Checklist Item 2 based on guideline",
        "Checklist Item 3 based on guideline"
    ]

    for item in checklist:
        redis_client.rpush(checklist_key, item)

    redis_client.set(status_key, "COMPLETED")
    return f"Checklist for {event_id} created."
