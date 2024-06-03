#!/bin/bash

cd ..

file=./docker/docker-compose-nginx.yml

if [ "$1" = "up" ]; then
  sudo docker compose -f $file up -d
elif [ "$1" = "stop" ]; then
  sudo docker compose -f $file stop
elif [ "$1" = "rm" ]; then
  sudo docker compose -f $file stop
  echo y | sudo docker compose -f $file stop
fi
