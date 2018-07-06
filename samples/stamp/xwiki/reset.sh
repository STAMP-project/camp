#!/bin/bash

echo "Removing containers"
docker rm -f xwiki-mysql-db
docker rm -f xwiki-smoke-client-test
docker rm -f xwiki-web
docker rm -f xwiki-postgres-db