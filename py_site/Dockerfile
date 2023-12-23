FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt update && apt install ffmpeg libsm6 libxext6  -y

COPY . .

CMD [ "python3", "app/main.py"]
