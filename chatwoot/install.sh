#!/usr/bin/env bash
# Installs Chatwoot with Docker on an Ubuntu/Debian server.
#
#   ./install.sh chat.example.com   public install with automatic HTTPS
#                                   (point the domain's DNS to this server first)
#   ./install.sh                    local only, on http://localhost:3000
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

set_env() {  # set_env KEY VALUE — replace or append
  if grep -q "^$1=" .env; then sed -i "s|^$1=.*|$1=$2|" .env; else echo "$1=$2" >> .env; fi
}

domain="${1:-}"
domain="${domain#https://}"; domain="${domain#http://}"; domain="${domain%%/*}"
if [ -n "$domain" ]; then
  set_env CHATWOOT_DOMAIN "$domain"
  set_env COMPOSE_PROFILES https
  set_env FRONTEND_URL "https://$domain"
  set_env FORCE_SSL true
fi

docker compose pull
docker compose up -d postgres redis
echo "Preparing the database..."
docker compose run --rm rails bundle exec rails db:chatwoot_prepare
docker compose up -d

echo
echo "Chatwoot is running. Open $(grep ^FRONTEND_URL= .env | cut -d= -f2-) and create the admin account."
