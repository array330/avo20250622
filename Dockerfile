FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
CMD ["gunicorn", "jobs_project.wsgi:application", "--bind", "0.0.0.0:8000"]
