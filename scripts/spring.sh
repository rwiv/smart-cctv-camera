#!/bin/bash

cd ..

file=./docker/docker-compose-spring.yml

if [ "$1" = "up" ]; then
  sudo docker compose -f $file --env-file ./docker/.env up -d
elif [ "$1" = "stop" ]; then
  sudo docker compose -f $file --env-file ./docker/.env stop
elif [ "$1" = "rm" ]; then
  sudo docker compose -f $file --env-file ./docker/.env stop
  echo y | sudo docker compose -f $file --env-file ./docker/.env rm
fi
