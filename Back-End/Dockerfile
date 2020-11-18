FROM python:alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt

CMD tail -f /dev/null