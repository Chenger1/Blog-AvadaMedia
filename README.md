# Blog-AvadaMedia

# Used Django 3 for main apps

### Build-in Django admin page replaced with adminLTE. 

_If you want to test it:_

1. Install requirements.txt
2. Download adminLTE source files and place **dict** and **plugins** directories
to **static/django-admin** (Maybe you will need to execute `python manage.py collectstatic` command)
   
3. Create postgres db and set your **db_name**, **username** and **password**
to settings.py. 
   
4. Use something like __https://djecrety.ir/__ for generating new secret_key
and set it in settings as well. 
   
5. Also, create superuser account with `python manage.py createsuperuser`
6. Run it with `python manage.py runserver`