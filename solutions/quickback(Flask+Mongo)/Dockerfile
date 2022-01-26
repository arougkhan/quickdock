FROM python:3.9-slim

RUN apt-get clean  && apt-get -y update

WORKDIR /app
#RUN pip install psycopg2-binary

COPY ./src/python/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src/python/app /app
ENV PYTHONPATH=/

RUN groupadd -g 500 app && useradd -u 1000 -g app app
RUN chmod -R 766 /app/*
RUN chown -R app:app /app/*
USER app

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "controller:application" ]

