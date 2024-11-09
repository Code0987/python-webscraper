FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"

RUN pip install --upgrade pip

WORKDIR /

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
COPY ./config /config

CMD ["uvicorn", "app.api:api", "--host", "0.0.0.0", "--port", "80"]
