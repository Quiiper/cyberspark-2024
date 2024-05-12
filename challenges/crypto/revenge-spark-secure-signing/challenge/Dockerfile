FROM python:3.8-slim
RUN useradd -m -s /bin/sh app
RUN pip install pycryptodome
EXPOSE 9500
RUN apt-get update -y && apt-get upgrade -y 
WORKDIR /home/app
COPY ./* ./
RUN chmod +x ynetd
RUN chmod +x start.sh
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]