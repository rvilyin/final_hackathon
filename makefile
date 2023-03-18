migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
run:
	python3 manage.py runserver 0.0.0.0:8000
restart:
	systemctl daemon-reload
	systemctl restart daphne
	systemctl restart nginx
