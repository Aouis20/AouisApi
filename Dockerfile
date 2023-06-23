FROM python:3.9.14-buster
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]