FROM python:3.7-stretch

RUN adduser zirkel

WORKDIR /home/zirkel/

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y latexmk texlive-full
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn psycopg2


COPY app app
COPY migrations migrations
COPY .env config.py start.sh website.py ./
RUN chmod u+x start.sh

RUN mkdir ~/.ssh
COPY id_rsa.korrespondenzzirkel .ssh/id_rsa

ENV FLASK_APP website.py

RUN chown -R zirkel:zirkel ./

USER zirkel

RUN mkdir .data

EXPOSE 5000

ENTRYPOINT ["./start.sh"]