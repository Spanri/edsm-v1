heroku ps:scale web=1
heroku run python manage.py makemigrations users
heroku run python manage.py makemigrations docs
heroku run python manage.py migrate
heroku run python manage.py collectstatic
web: gunicorn django_auth.wsgi