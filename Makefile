mig:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

superuser:
	python manage.py createsuperuser