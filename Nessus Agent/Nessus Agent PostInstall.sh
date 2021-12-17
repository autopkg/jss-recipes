#!/bin/bash

KEY=""
HOST=""
PORT=""

if /Library/NessusAgent/run/sbin/nessuscli agent status | grep "Linked to: None"; then
    /Library/NessusAgent/run/sbin/nessuscli agent link \
    --key="$KEY" \
    --host="$HOST" \
    --port="$PORT"
else
    echo "Tenable Agent already installed and linked!"
    echo "Exiting..."
fi

exit 0