# FROM django
# ADD . /my-django-app
# WORKDIR /my-django-app
# RUN pip install -r requirements.txt
# CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]

FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/

# RUN apt-get install python3.7-dev
# RUN apt-get install -y libpq-dev
RUN pip install -r requirements.txt

COPY . /app/