#####################Dockerfile for FM-backend############################

FROM python:3.7.5-slim

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y curl

RUN apt-get install -y vim

ENV directory /home/ubuntu/docker_images/om-backend

WORKDIR ${directory}

ADD requirements.txt ${directory}/requirements.txt

ADD manage.py ${directory}/manage.py

COPY azure_blob_app ${directory}/azure_blob_app

COPY blob_api ${directory}/blob_api

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

CMD ["python3","manage.py","runserver","0.0.0.0:8081"]
