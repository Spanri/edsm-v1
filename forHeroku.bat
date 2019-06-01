cd frontend
npm run build
cd ..
c:/Users/Spanri/Desktop/CRM-diplom/venv/Scripts/activate.bat
python manage.py collectstatic
move %~dp0\frontend\dist\index.html %~dp0\staticfiles\index.html
move %~dp0\frontend\dist\static %~dp0\staticfiles\static