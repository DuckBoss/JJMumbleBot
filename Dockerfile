FROM python:3-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed"
RUN apt-get install -y sudo libopus-dev gcc ffmpeg vlc

# VLC is not supported to be run as root
RUN useradd -d /app -ms /bin/bash jjmumblebot
RUN echo "jjmumblebot ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER jjmumblebot

WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt --no-warn-script-location
COPY . /app

# Allow jjmumblebot user to write in the local host mounted volume
RUN sudo chown -R jjmumblebot.jjmumblebot /app

# Cleanup database files
RUN find /app -name *.db -exec rm -rf {} \;
