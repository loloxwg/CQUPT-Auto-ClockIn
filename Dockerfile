FROM python:3

COPY mrdk.py /app/mrdk.py
COPY priv.py /app/priv.py

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

CMD cd /app && python mrdk.py