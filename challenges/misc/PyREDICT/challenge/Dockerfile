FROM python:slim AS app
RUN pip install --no-cache-dir randcrack

FROM pwn.red/jail
COPY --from=app / /srv

ENV JAIL_POW=0 JAIL_PORT=1337 JAIL_TIME=20

COPY app.py /srv/app/run

WORKDIR /srv/app

RUN chmod +x run