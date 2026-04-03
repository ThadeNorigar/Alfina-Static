#!/bin/bash
set -e

cd "$(dirname "$0")"
git pull origin main
docker compose up -d --force-recreate
echo "Alfina-Static deployed successfully"
