FROM python:3

COPY mrdk.py /app/mrdk.py
COPY priv.py /app/priv.py
COPY scheduler.py /app/scheduler.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD cd /app && python scheduler.py