#!/usr/bin/env bash

set -e

IMPLEMENTATION=${1:-cpython}
COMPOSE_FILE_NAME=docker-compose.${IMPLEMENTATION}.yml

docker-compose --file ${COMPOSE_FILE_NAME} up --build --exit-code-from hypothesis_sqlalchemy-${IMPLEMENTATION}

STATUS=$?

docker-compose --file ${COMPOSE_FILE_NAME} down --remove-orphans

if [[ "$STATUS" -eq "0" ]]; then
	echo "${IMPLEMENTATION} tests passed";
else
	echo "${IMPLEMENTATION} tests failed"
fi

exit ${STATUS}
