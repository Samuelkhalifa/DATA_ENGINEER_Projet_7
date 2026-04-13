#!/bin/zsh


# activate docker-compose
cd infra &&
docker compose down -v &&
docker compose up

