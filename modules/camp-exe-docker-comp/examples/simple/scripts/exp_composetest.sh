#!/bin/bash
echo "Waiting for 5 sec to set up deployment"
sleep 5
RESP=$(curl 127.0.0.1:5000)
#RESP='Hello World! I have been called.'
echo "$RESP param1:$1 param2:$2"