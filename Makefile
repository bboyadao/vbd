init: up mi mock _test

test: up _test

up:
	docker-compose up -d

mi:
	docker-compose exec web python manage.py migrate

mock:
	docker-compose exec web python manage.py mock_user --len 50

stop:
	docker-compose stop

down:
	docker-compose down

_test:
	docker-compose exec web python manage.py test

r:
	python manage.py runserver
mk:
	python manage.py makemigrations
sh:
	python manage.py shell_plus --ipython
cl:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	find . -path "*/db.sqlite3"  -delete
su:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')" | python manage.py shell

mock_user:
	python manage.py mock_user



