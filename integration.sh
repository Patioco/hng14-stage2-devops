#!/bin/bash
set -e
curl -f http://localhost:8000/health || exit 1
echo "API is healthy"