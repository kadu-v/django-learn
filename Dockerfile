FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /workspace
ADD requirements.txt /workspace/
RUN pip install -r requirements.txt
ADD . /workspace/