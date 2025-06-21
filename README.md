# Jobs Project

## Overview
This Django-based microservice accepts a `guideline_text` via POST `/jobs/`, enqueues a GPT-powered task to summarize and build a checklist, and exposes a GET `/jobs/{event_id}/` endpoint to retrieve the job status and results.

(See full README in repository for details)
