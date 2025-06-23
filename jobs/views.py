# SPDX-License-Identifier: MIT OR Apache-2.0

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Job
from .tasks import gpt_job, redis_client
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    request={"type": "object", "properties": {"guideline_text": {"type": "string"}}},
    responses={"200": {"type": "object", "properties": {"event_id": {"type": "string"}}}}
)
@csrf_exempt
def create_job(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        guideline_text = data.get('guideline_text', '')
        job = Job.objects.create(guideline_text=guideline_text)
        gpt_job.delay(str(job.event_id), guideline_text)
        return JsonResponse({'event_id': str(job.event_id)})
    else:
        return JsonResponse({'error': 'Method not allowed. Use POST.'}, status=405)

@extend_schema(
    parameters=[OpenApiParameter("event_id", type=str)],
    responses={"200": {"type": "object", "properties": {
        "GPT_job_status": {"type": "string"},
        "GPT_job_result": {"type": "array", "items": {"type": "string"}, "nullable": True}
    }}}
)
def get_job_status(request, event_id):
    if request.method == 'GET':
        status_key = f"status:{event_id}"
        checklist_key = f"checklist:{event_id}"

        status = redis_client.get(status_key)
        if status is None:
            status = 'PENDING'
            result = None
        else:
            status = status.decode('utf-8')
            if status == 'COMPLETED':
                checklist = redis_client.lrange(checklist_key, 0, -1)
                result = [item.decode('utf-8') for item in checklist]
            else:
                result = None

        return JsonResponse({
            'GPT_job_status': status,
            'GPT_job_result': result
        })
    else:
        return JsonResponse({'error': 'Method not allowed. Use GET.'}, status=405)
