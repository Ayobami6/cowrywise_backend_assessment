.PHONY: run-admin
run-admin:
	@docker-compose up postgres -d
	@docker-compose up rabbitmq -d
	@docker-compose up admin_api 

run-library:
	@docker-compose up -d

run-frontend:
	@docker-compose up postgres -d 
	@docker-compose up rabbitmq -d
	@docker-compose up frontend_api 

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