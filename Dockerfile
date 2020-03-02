FROM python:3

RUN apt-get update && apt-get install -y pandoc

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install .

CMD [ "dir-sync" ]