FROM python:3-alpine

COPY requirements.txt requirements.txt

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN pip install -r requirements.txt