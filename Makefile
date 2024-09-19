.PHONY: run-admin
run-admin:
	@docker-compose up postgres -d
	@docker-compose up admin_api 

run-library:
	@docker-compose up admin_api 
	@docker-compose up frontend_api

stop-library:
	@docker-compose down

run-frontend:
	@docker-compose up postgres -d 
	@docker-compose up frontend_api 

admin-consumer:
	@docker-compose run admin_consumer

frontend_consumer:
	@docker-compose run frontend_consumer

test-admin:
	@cd admin_api/
	@pytest

install:
	@pip install $(package)

csu:
	@python manage.py createsuperuser

mms:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@python manage.py shell

dbshell:
	@python manage.py dbshell

test:
	@pytest