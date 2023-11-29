FROM python:3.11-buster
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
