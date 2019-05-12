web: gunicorn django_auth.wsgi
heroku ps:scale web=1 -a edms-mtuci
heroku run python manage.pymigrate -a edms-mtuci