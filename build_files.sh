python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade pip
python manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate