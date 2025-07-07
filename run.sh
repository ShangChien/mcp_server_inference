#!/bin/bash
source /app/.venv/bin/activate
fastmcp run main.py --transport sse --host 0.0.0.0 --port 5003 2>&1 | tee /app/server.log