FROM ubuntu

RUN apt update && apt install python3-venv -y

WORKDIR /root/brownbook

COPY modules .
COPY SinCity .
COPY __main__.py .
COPY __init__.py .
COPY requirements.txt .
COPY agent.json .

RUN python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
