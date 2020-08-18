FROM python:3.7.0-alpine3.8

RUN mkdir /app
ADD requirements.txt /app/
WORKDIR /app

ENV PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/app/ \
    PYTHONUNBUFFERED=1

RUN apk --no-cache add \
    bash \
    git \
    python3 \
    python3-dev \
    zlib-dev \
    libffi-dev \
    ca-certificates \
    py-pip \
    build-base \
    libxslt-dev \
    libxml2-dev \
    libffi-dev \
    py-psutil \
    postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers && \
    pip install --upgrade pip xlrd && \

RUN pip install -r /app/requirements.txt
RUN apk --purge del .build-deps

ADD . /app/

RUN echo $GIT_SHA > /app/version.txt

STOPSIGNAL SIGINT

CMD bin/boot.sh