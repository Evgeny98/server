FROM python:3.7.4

EXPOSE 8090

COPY . /app
WORKDIR /app

ENV DB_HOST="localhost"

ENV DB_PORT="8090"

ENV DB_NAME="numbers"

ENV APP_HOST="localhost

ENV APP_PORT="8090"

RUN pip3 install -r requirements.txt

CMD ["python", "./main.py"]
