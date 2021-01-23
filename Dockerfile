FROM python:3

COPY mrdk.py /app/mrdk.py
COPY priv.py /app/priv.py

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY dk-cron /etc/cron.d/dk-cron

RUN pip install requests \
    && chmod 0644 /etc/cron.d/dk-cron \
    && crontab /etc/cron.d/dk-cron \
    && touch /var/log/cron.log

CMD cd /app && python mrdk.py && cron && tail -f /var/log/cron.log