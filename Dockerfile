FROM python:3.10 as builder

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app_server app_server

COPY migrations migrations
#COPY config.py agents_config.json  ./
COPY config.py ./
COPY app.py   ./
#COPY fssl.key fssl.pem ./

CMD ["flask","db","upgrade"]
#CMD ["python", "init_db.py"]   #初始化数据库
CMD ["python", "app.py"]
