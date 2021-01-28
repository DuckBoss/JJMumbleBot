FROM docker.io/python:3-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update --no-install-recommends \
&& apt-get install -y apt-utils --no-install-recommends 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed" \
&& apt-get install -y ffmpeg vlc --no-install-recommends \
&& apt-get install -y libopus-dev gcc openssl \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable VLC to be executed as root
RUN sed -i 's/geteuid/getppid/' /usr/bin/vlc

# Expose primary web interface port
EXPOSE 7000

WORKDIR /app
# Add all the requirements.txt files from the requirements folder and install them.
ADD ./requirements/ /app
RUN pip install -r requirements.txt -r web_server.txt --no-warn-script-location
COPY . /app

# Cleanup database files
RUN find /app -name "*.db" -exec rm -rf {} \;

ENTRYPOINT ["python", "/app"]

