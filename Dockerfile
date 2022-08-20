FROM python:3.10

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt