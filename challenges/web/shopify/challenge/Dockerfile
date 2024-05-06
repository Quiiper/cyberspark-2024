FROM python:3.9-slim-buster

WORKDIR /chr

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget supervisor
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

RUN pip install gunicorn

WORKDIR /home/app

COPY ./app .

COPY ./logs /home/app/logs

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python /home/app/setup.py

COPY ./supervisord.conf /etc/supervisord.conf

EXPOSE 5000