cd frontend
npm run build
cd ..
python manage.py collectstatic
REM move %~dp0\frontend\dist\index.html %~dp0\staticfiles\index.html
REM move %~dp0\frontend\dist\static %~dp0\staticfiles\