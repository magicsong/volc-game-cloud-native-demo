#!/bin/sh

# Start the game server in the background
/opt/veloren-server-cli &

python3 /opt/health_check.py
