#!/bin/bash

echo "Building tecor demo"
docker build -t vassik/tecor-demo:latest .
echo "Pushing docker image to hub"
docker push vassik/tecor-demo:latest