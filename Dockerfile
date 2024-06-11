FROM python:3.10 as builder

WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app_server app_server
COPY app_agent app_agent



COPY migrations migrations
COPY config.py ./
COPY app.py   ./
#COPY fssl.key fssl.pem ./

#COPY MetaGPT MetaGPT
#RUN cd MetaGPT && pip install --upgrade -e .
#RUN cd ..


CMD ["flask","db","upgrade"]
#CMD ["python", "init_db.py"]   #初始化数据库
CMD ["python", "app.py"]

# docker build -t hyperbrain .
#docker run -v ${PWD}/config.py:/home/app/config.py -v ${PWD}/config2.yaml:/home/app/MetaGPT/config/config2.yaml -d -p 5000:5000 --name hyperbrain hyperbrain