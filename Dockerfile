FROM python:3.7-slim

COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY ./app/ /app
WORKDIR /app/

EXPOSE 8080

CMD ["gunicorn", "-c", "/app/gunicorn.conf.ini", "app:app"]
