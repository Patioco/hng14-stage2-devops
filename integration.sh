#!/bin/bash

set -e

echo "Submitting job..."
JOB_ID=$(curl -s -X POST http://localhost:3000/submit | jq -r '.job_id')

echo "Polling..."
for i in {1..10}; do
  STATUS=$(curl -s http://localhost:3000/status/$JOB_ID | jq -r '.status')
  if [ "$STATUS" == "completed" ]; then
    echo "Success"
    exit 0
  fi
  sleep 2
done

echo "Failed"
exit 1