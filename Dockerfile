FROM python:3.9.14-buster
WORKDIR /api

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
