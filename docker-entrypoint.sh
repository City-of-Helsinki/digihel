#!/bin/bash

set -e

while ! nc -z db 5432; do echo "Waiting for database connection..." && sleep 3; done
echo "Database available, starting application"

exec "$@"
