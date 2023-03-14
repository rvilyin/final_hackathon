migrate:
	python3.10 manage.py makemigrations
	python3.10 manage.py migrate
run:
	python3.10 manage.py runserver