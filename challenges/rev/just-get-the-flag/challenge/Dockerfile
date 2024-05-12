FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app

COPY . .

RUN chmod +x main

RUN chmod +x entrypoint.sh

ENV flag=Spark{64e9310f03c092c01134ea409c68bfa323ae5f43}

ENTRYPOINT ["./entrypoint.sh"]