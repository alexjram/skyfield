FROM python:3.10-alpine

ARG UID=1000
ARG GID=1000

RUN adduser -u $UID --disabled-password --gecos "" appuser
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /appdata/www
WORKDIR /appdata/www
CMD [ "python", "main.py" ]