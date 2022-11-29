FROM tiangolo/uwsgi-nginx-flask:latest

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./worker-app /app
