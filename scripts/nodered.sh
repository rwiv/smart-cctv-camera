#!/bin/bash

cd ..

if [ "$1" = "up" ]; then
  cmd="$1 -d"
else
  cmd="$1"
fi

sudo docker compose -f ./docker/docker-compose-nodered.yml $cmd
