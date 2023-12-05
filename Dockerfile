FROM python:3.10-slim-buster

ENV TZ=UTC

WORKDIR /app

COPY ./scrapper_database /app/scrapper_database
COPY endpoint.py /app/
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# CMD ["python", "scrapper_database/spiders/spider.py"]

CMD ["python", "endpoint.py"]

# Comando predeterminado al iniciar el contenedor (comentado por ahora)
# CMD ["scrapy", "runspider", "scrapper_database/spiders/current.py", "-o", "current.jsonl"]
