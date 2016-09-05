FROM python:3.5-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir envelopes
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
    && apk update && apk add py3-lxml \
    && ln -s /usr/lib/python3.5/site-packages/lxml /usr/local/lib/python3.5/site-packages/lxml

COPY . /usr/src/app
CMD python3 ./source/arround.py
