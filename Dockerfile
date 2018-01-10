FROM python:3.6.0 as builder

LABEL maintainer=clarkzjw<hello@jinwei.me>

RUN pip install virtualenv

COPY requirements.txt /app/requirements.txt

COPY bootstrap.py /app/bootstrap.py

RUN /app/bootstrap.py

ADD . /app

WORKDIR /app

RUN /bin/bash -c "source /app/.venv/bin/activate && make html"


FROM alpine:latest

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk add --update git openssh-client && rm -rf /var/cache/apk/*

WORKDIR /html

ENV COMMIT_USER="clarkzjw"
ENV COMMIT_EMAIL="hello@jinwei.me"

RUN git clone git@github.com:clarkzjw/blog.jinwei.me.git /html && git checkout gh-pages

COPY --from=builder /app/_build/html /html

RUN git add -A && git commit -m "`date`" && git push origin gh-pages


FROM nginx:alpine

COPY --from=builder /app/_build/html /usr/share/nginx/html
