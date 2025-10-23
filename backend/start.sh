#!/bin/bash

# This ensures the script exits if any command fails
set -e

# Run the Uvicorn server. It will use the PORT environment variable
# provided by Render, or default to 8000.
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
