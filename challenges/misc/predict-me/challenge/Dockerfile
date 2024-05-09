FROM node:20-slim AS node

RUN npm install -g nodemon

FROM pwn.red/jail

COPY --from=node / /srv

ENV JAIL_POW=0 JAIL_PORT=1337 JAIL_TIME=60 JAIL_PIDS=10 JAIL_MEM=50M

COPY app.js /srv/app/run

WORKDIR /srv/app

RUN chmod +x run