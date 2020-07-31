FROM python:3.7.4

RUN apt -y update && \
    apt install -y default-mysql-client

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
