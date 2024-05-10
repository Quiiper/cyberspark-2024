FROM python:slim AS app

RUN pip install pycryptodome

FROM pwn.red/jail

COPY --from=app / /srv

ENV JAIL_MEM=20M JAIL_POW=0 JAIL_PORT=1337 JAIL_TIME=20 JAIL_PIDS=10

COPY app.py /srv/app/run

COPY SECRET.py /srv/app

WORKDIR /srv/app

RUN chmod +x run