#!/usr/bin/env bash

set -ex

sudo rm /usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` > docker-compose
chmod +x docker-compose
sudo mv docker-compose /usr/local/bin
