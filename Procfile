heroku ps:scale web=1
release: python manage.py makemigrations users
release: python manage.py makemigrations docs
release: python manage.py migrate
release: python manage.py collectstatic
web: gunicorn django_auth.wsgi