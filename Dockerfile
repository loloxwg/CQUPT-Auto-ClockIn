FROM python:3

COPY mrdk.py /app/mrdk.py
COPY priv.py /app/priv.py

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN touch /etc/cron.d/crontab \
    && echo "0 0 6 * * ? cd /app && python mrdk.py" >> /etc/cron.d/crontab

RUN pip install requests

CMD cd /app && python mrdk.py && cron && crontab /etc/cron.d/crontab && tail -f /dev/null