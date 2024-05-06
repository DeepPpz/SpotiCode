@echo off
setlocal

call venv\Scripts\activate

cd spoticode
python manage.py runserver