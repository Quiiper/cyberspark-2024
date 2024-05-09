FROM python:3.8-slim
WORKDIR /chr

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget supervisor
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN echo "Spark{54Y_NH3B_MLOU5IY4_70_7H3_C4M3r4}" > /flag.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "app.py" ]
