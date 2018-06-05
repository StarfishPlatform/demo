#! /usr/bin/env bash
set -Eeuxo pipefail;

docker build . --tag starfish-demo-crm:0.1

! docker rm -f starfish-demo-crm 

docker run --net="host" \
  --name starfish-demo-crm \
  starfish-demo-crm:0.1

