FROM python:3.10-slim-buster

ENV TZ=UTC

WORKDIR /app

COPY ./scrapper_database /app/scrapper_database
COPY endpoint.py /app/
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "endpoint.py"]
