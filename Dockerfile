FROM python:3.7.4

EXPOSE 8090

ENV DB_HOST="redis"
ENV DB_PORT="6379"
ENV DB_NAME="numbers"
ENV APP_HOST="0.0.0.0"
ENV APP_PORT="8090"

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python", "./main.py"]
