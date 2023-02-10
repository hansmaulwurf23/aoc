FROM ubuntu:jammy

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt upgrade -y
RUN export DEBIAN_FRONTEND=noninteractive && apt install python3 python3-pip git -y

WORKDIR /
RUN mkdir aoc
COPY ./requirements.txt /aoc/requirements.txt

RUN pip3 install -r /aoc/requirements.txt