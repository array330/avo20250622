# Django-Celery-Redis-PostgreSQL GPT Job API

## Overview

This project implements a simple API service built with Django and Celery that accepts guideline texts, processes them asynchronously using a simulated GPT job, and returns a unique event ID for tracking. The GPT job summarizes the guideline text and creates a checklist stored in Redis. Clients can query job status and results via a dedicated endpoint.

---

## Design Choices

### 1. Frameworks & Tools

- **Django**: Chosen for its robust web framework features and ease of building REST APIs.
- **Celery**: Used to handle asynchronous background tasks so the summarization (GPT job) does not block the request-response cycle.
- **Redis**: Acts as both the Celery broker and as a fast storage medium for checklist and job status data.
- **PostgreSQL**: Used as the primary database to store job metadata and event IDs.
- **UUID for event_id**: Provides a globally unique identifier to track jobs without exposing internal database IDs.
- **DRF Spectacular**: To auto-generate OpenAPI schema and enable interactive Swagger UI.

### 2. API Design

- **POST `/jobs/`**: Accepts the `guideline_text` and returns an `event_id`. The Celery GPT job is triggered asynchronously.
- **GET `/jobs/{event_id}/`**: Returns the status of the GPT job (`PENDING`, `IN_PROGRESS`, `COMPLETED`) and the checklist result if completed.
- **No GET on `/jobs/`**: Strictly a POST-only endpoint for job creation to avoid data leakage or unintended access.

### 3. Redis Data Structures

- Job **status** stored under key `status:{event_id}`, a simple string indicating current state.
- Checklist stored under key `checklist:{event_id}`, a Redis list preserving FIFO order.

### 4. Testing and Coverage

- Tests cover creation, task execution, Redis state, and API responses.
- Coverage target ≥ 70% to ensure reliability and maintainability.

---

## AI Assistance

This entire implementation was developed with the assistance of AI tools to:

- Generate example code snippets for Django, Celery, and Redis integration.
- Provide best practices for asynchronous task management.
- Help design the Redis key/value schema and FIFO checklist storage.
- Create test cases to cover critical API and task behavior.
- Automatically generate OpenAPI specs annotations for API documentation.
- Compose Docker Compose configurations for service orchestration.
- Draft this README and documentation clearly explaining design rationales.

The AI support streamlined the development process, ensuring adherence to modern patterns and clean architecture while reducing manual effort.

---

## How to Run

1. Install dependencies from `requirements.txt`.
2. Use Docker Compose to start PostgreSQL, Redis, Django, and Celery worker services.
3. Run database migrations: `python manage.py migrate`.
4. Start the Django development server.
5. Use Swagger UI at `/swagger-ui/` to explore the API.
6. POST to `/jobs/` with a guideline text to create jobs.
7. GET `/jobs/{event_id}/` to check job status and retrieve results.

---

## License

Dual-licensed under MIT and Apache-2.0 licenses. See LICENSE-MIT and LICENSE-APACHE files for details.

---

Thank you for exploring this project!
