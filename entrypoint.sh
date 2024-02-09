#!/bin/bash

SCRIPT_PATH="/app/main.py"

if [ -f $SCRIPT_PATH ]; then

    pushd $(dirname $SCRIPT_PATH)
    python $(basename $SCRIPT_PATH)
    exit 0
else
    echo "No file found at $1"
    exit 1
fi