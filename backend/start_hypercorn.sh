#!/bin/bash

# backend/start_hypercorn.sh

set -e

# Run the server with Hypercorn
hypercorn app.main:app --bind "0.0.0.0:${PORT:-8000}"
