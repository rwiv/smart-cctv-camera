#!/bin/bash

cd ..

file=./docker/docker-compose-nginx.yml

if [ "$1" = "up" ]; then
  cmd="$1 -d"
  sudo docker compose -f $file up -d
else if [ "$1" = "stop" ]
  sudo docker compose -f $file stop
else if [ "$1" = "rm" ]
  sudo docker compose -f $file stop
  echo y | sudo docker compose -f $file stop
fi
