#!/bin/bash

RESP=$(curl localhose:5000)
echo "$RESP param1:$1 param2:$2"