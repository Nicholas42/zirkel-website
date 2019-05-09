FROM python:3.6-alpine

RUN adduser -D zirkel

WORKDIR /home/zirkel/

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY .env config.py start.sh ./
RUN chmod u+x start.sh

ENV FLASK_APP website.py

RUN chown -R zirkel:zirkel ./

USER zirkel

EXPOSE 5000

ENTRYPOINT ["./start.sh"]