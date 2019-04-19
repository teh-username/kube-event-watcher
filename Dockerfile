FROM python:3.7-alpine

RUN pip3 install -q kubernetes==9.0.0
WORKDIR /app
COPY /app .

CMD ["python", "-u", "/app/main.py"]
