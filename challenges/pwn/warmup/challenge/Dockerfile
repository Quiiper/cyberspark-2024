FROM ubuntu:latest AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY warmup /srv/app/run
COPY flag.txt /srv/app/flag.txt
ENV JAIL_MEM=20M JAIL_POW=0 JAIL_PORT=1000

WORKDIR /srv/app

RUN chmod +x run
