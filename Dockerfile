FROM conductorcr.azurecr.io/vision/flaskbase

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


WORKDIR /app

COPY . /app

CMD ./start.sh
