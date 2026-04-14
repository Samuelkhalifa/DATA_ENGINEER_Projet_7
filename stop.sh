#!/bin/zsh



if docker ps | grep -q "Up"; then
    echo "docker-compose is running" &&
    cd infra &&
    docker compose down -v
else 
    echo "docker-compose is not running"
fi