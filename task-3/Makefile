
# I've created simple Makefile for most common commands for both Docker and Django(api-service)
# I will use and explain them in README file

DOCKER_COMPOSE = docker compose

# Docker commands

createnetwork:
	docker network create core-network
up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up --build -d

build:
	$(DOCKER_COMPOSE) build

logs:
	$(DOCKER_COMPOSE) logs -f


# Django commands
migrate:
	$(DOCKER_COMPOSE) exec api python manage.py migrate --noinput

test:
	$(DOCKER_COMPOSE) exec api pytest

createsuperuser:
	$(DOCKER_COMPOSE) exec api python manage.py createsuperuser

collectstatic:
	$(DOCKER_COMPOSE) exec api python manage.py collectstatic --noinput

shell:
	$(DOCKER_COMPOSE) exec api python manage.py shell


