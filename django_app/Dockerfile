FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=""
ENV LC_NAME="uk_UA.UTF-8"
RUN mkdir /config
ADD requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN mkdir /src;
COPY .env /src/.env
WORKDIR /src
