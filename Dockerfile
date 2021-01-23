FROM python:3

COPY mrdk.py /app/mrdk.py
COPY priv.py /app/priv.py

RUN apt-get install cron \
    && touch /etc/cron.d/crontab \
    && echo "0 0 6 * * ? cd /app && python mrdk.py" >> /etc/cron.d/crontab
RUN pip install requests

CMD cron && crontab /etc/cron.d/crontab && tail -f /dev/null