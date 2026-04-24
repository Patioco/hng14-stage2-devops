#!/bin/bash
set -e
curl -f http://localhost:8000/health
echo "API is healthy"