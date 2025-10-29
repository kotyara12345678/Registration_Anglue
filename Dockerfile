FROM ubuntu:latest
LABEL authors="glino"

ENTRYPOINT ["top", "-b"]