FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

# Копируем внутрь контейнера и даем права всякие
COPY /docker/backend/wait-for-postgres.sh /
COPY /docker/backend/cmd-command.sh /
RUN chmod +x /wait-for-postgres.sh
RUN chmod +x /cmd-command.sh

WORKDIR /app

COPY requirements.txt .

# RUN apt-get update && \
#     apt-get install -y software-properties-common && \
#     add-apt-repository -y ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt install -y python3.7

# RUN apt update -y && apt upgrade -y && \
#  apt-get install python3.7 && \

RUN apt-get install -y libpq-dev

# установить зависимости
RUN pip install -r requirements.txt

COPY . .

# # собрать статические файлы, для того, чтобы
# # запустить клиент на сервере
# RUN python manage.py collectstatic

# # миграция таблиц для правильной работы с бд
# RUN python manage.py migrate

# # Нужно настроить глобальные переменные (для почты, для бд, для
# # хранилища амазона и так далее). Все значения секретные, поэтому
# # нужно писать разработчику, если он даст - сможете протестировать.
# # Ниже пример настройки глобальной переменной. Это для виндовс,
# # для юниксов вместо set - export
# RUN set EDMS-MAIL-PASSWORD=password

EXPOSE 8000

# RUN python manage.py makemigrations docs && \
#  python manage.py makemigrations users && \
#  python manage.py migrate && \
#  python manage.py runserver 0.0.0.0:8000

# CMD python manage.py runserver 0.0.0.0:8000

# RUN chmod +x entrypoint.sh
ENTRYPOINT ["/wait-for-postgres.sh", "edsm-v1-db", "/cmd-command.sh"]