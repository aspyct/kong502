FROM python:3

WORKDIR  /usr/src/app
COPY buggy-service.py ./

EXPOSE 8000
EXPOSE 8001
EXPOSE 8002

CMD [ "python", "./buggy-service.py" ]
