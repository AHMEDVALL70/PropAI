#!/bin/bash
echo "🔒 Starting AhmedVall PropAI Proxy Server..."
if [ -f .env ]; then
    export $(cat .env | xargs)
fi
pip install -r requirements.txt
python proxy-server.py