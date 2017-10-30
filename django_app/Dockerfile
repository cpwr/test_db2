FROM python:3.6

COPY ./requirements.txt /app/requirements.txt

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt


CMD [ "python", "./manage.py runserver" ]
