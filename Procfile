heroku ps:scale web=1
release: python manage.py makemigrations users
release: python manage.py makemigrations docs
release: python manage.py migrate
web: gunicorn django_auth.wsgi