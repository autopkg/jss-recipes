#!/bin/bash

KEY=""
HOST=""
PORT=""

if [ ! -f "/Library/NessusAgent/run/sbin/nessuscli" ]; then
    echo "Nessus Agent package did not successfully install."
    echo "Try re-running the policy."
    exit 1
fi

if /Library/NessusAgent/run/sbin/nessuscli agent status | grep "Linked to: None"; then
    /Library/NessusAgent/run/sbin/nessuscli agent link \
    --key="$KEY" \
    --host="$HOST" \
    --port="$PORT"
else
    echo "Nessus Agent already installed and linked!"
fi

exit 0