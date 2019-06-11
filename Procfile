heroku ps:scale web=1
clock: python aps.py
heroku ps:scale clock=1
release: python manage.py makemigrations docs && python manage.py makemigrations users && python manage.py migrate 
&& python manage.py collectstatic
web: gunicorn django_auth.wsgi