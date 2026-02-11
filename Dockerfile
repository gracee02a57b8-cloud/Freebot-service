FROM docker-io.nexus.gk-osnova.ru/python:3.11-slim
WORKDIR /app/

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /app
CMD python3 bot.py;
