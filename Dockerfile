FROM python:3-slim

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . /app/

RUN find /app -name *.db -exec rm -rf {} \;

RUN apt-get update
RUN apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed"
RUN apt-get install -y libopus-dev gcc ffmpeg vlc

RUN pip install -r requirements.txt

