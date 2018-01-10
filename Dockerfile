FROM python:3.6.0 as builder

LABEL maintainer=clarkzjw<hello@jinwei.me>

RUN pip install virtualenv

COPY requirements.txt /app/requirements.txt

COPY bootstrap.py /app/bootstrap.py

RUN /app/bootstrap.py

ADD . /app

WORKDIR /app

RUN /bin/bash -c "source /app/.venv/bin/activate && make html"


FROM nginx:alpine

COPY --from=builder /app/_build/html /usr/share/nginx/html
