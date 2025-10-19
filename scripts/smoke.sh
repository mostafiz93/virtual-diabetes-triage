#!/usr/bin/env bash
set -euo pipefail
IMG="$1"
CID=$(docker run -d -p 8080:8080 "$IMG")
trap "docker logs $CID; docker rm -f $CID >/dev/null 2>&1 || true" EXIT
for i in {1..30}; do
  if curl -s localhost:8080/health >/dev/null; then break; fi
  sleep 1
done
echo "Health:"; curl -s localhost:8080/health; echo
curl -s -X POST localhost:8080/predict   -H "content-type: application/json"   -d '{"age":0.02,"sex":-0.044,"bmi":0.06,"bp":-0.03,"s1":-0.02,"s2":0.03,"s3":-0.02,"s4":0.02,"s5":0.02,"s6":-0.001}' | jq .
