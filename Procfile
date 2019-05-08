web: python manage.py runserver
web: gunicorn --pythonpath django_auth --log-file -
heroku ps:scale web=1