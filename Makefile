THIS_FILE := $(lastword $(MAKEFILE_LIST))
include .env
export $(shell sed 's/=.*//' .env)

ENVIRONMENT := $(if $(NODE_ENV),$(NODE_ENV),development)

ifeq ($(NODE_ENV),production)
  COMPOSE_FILE = docker-compose.prod.yml
else
  COMPOSE_FILE = docker-compose.yml
endif

.PHONY: help build up start down destroy stop restart logs logs-api ps login-timescale login-api db-shell env-check

help:
	@echo "Usage: make [target] [NODE_ENV=development|production]"
	@echo ""
	@echo "Current environment: $(NODE_ENV)"
	@echo ""
	@echo "Available targets:"
	@echo "  build        - Build the Docker images"
	@echo "  up           - Start the containers in detached mode"
	@echo "  start        - Start existing containers"
	@echo "  down         - Stop and remove containers and networks"
	@echo "  destroy      - Stop and remove containers, networks, images, and volumes"
	@echo "  stop         - Stop running containers"
	@echo "  restart      - Restart containers"
	@echo "  logs         - View container logs (last 100 lines)"
	@echo "  logs-api     - View API container logs (last 100 lines)"
	@echo "  ps           - List running containers"
	@echo "  login-timescale - Open a bash shell in the timescale container"
	@echo "  login-api    - Open a bash shell in the API container"
	@echo "  db-shell     - Open a PostgreSQL shell in the timescale container"

env-check:
	@echo "Using $(COMPOSE_FILE) for NODE_ENV: $(NODE_ENV)"

build: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) build $(c)

up: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) up -d $(c)

start: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) start $(c)

down: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) down $(c) && docker network prune --force

destroy: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) down -v $(c)

stop: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) stop $(c)

restart: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) stop $(c)
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) up -d $(c)

logs: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f $(c)

logs-api: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) logs --tail=100 -f api

ps: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) ps

login-timescale: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) exec timescale /bin/bash

login-api: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) exec api /bin/bash

db-shell: env-check
	NODE_ENV=$(NODE_ENV) docker-compose -f $(COMPOSE_FILE) exec timescale psql -Upostgres