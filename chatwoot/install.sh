#!/usr/bin/env bash
# Installs Chatwoot with Docker on an Ubuntu/Debian server.
# Usage:  ./install.sh [public-url]     e.g. ./install.sh https://chat.example.com
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com | sh
fi

if [ ! -f .env ]; then
  cp .env.template .env
  for key in SECRET_KEY_BASE POSTGRES_PASSWORD REDIS_PASSWORD; do
    len=32; [ "$key" = SECRET_KEY_BASE ] && len=64
    sed -i "s|^$key=__GENERATED__|$key=$(openssl rand -hex $len)|" .env
  done
  echo "Created .env with fresh secrets."
fi

if [ "${1:-}" != "" ]; then
  sed -i "s|^FRONTEND_URL=.*|FRONTEND_URL=$1|" .env
  case "$1" in https://*) sed -i "s|^FORCE_SSL=.*|FORCE_SSL=true|" .env ;; esac
fi

docker compose pull
docker compose up -d postgres redis
echo "Preparing the database..."
docker compose run --rm rails bundle exec rails db:chatwoot_prepare
docker compose up -d

echo
echo "Chatwoot is starting on port 3000 (local only)."
echo "Open $(grep ^FRONTEND_URL= .env | cut -d= -f2-) and create the admin account."
