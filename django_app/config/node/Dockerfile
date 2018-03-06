FROM node:latest

#ENV http_proxy http://192.168.25.146:3128/
#ENV https_proxy http://192.168.25.146:3128/
#ENV no_proxy 192.168.16.75

RUN mkdir /src
WORKDIR /src

COPY package.json package.json

RUN npm install -g

COPY . /src/
