

dev-sync:
    uv sync --group=dev

dev-up:
    docker compose up -d  postgres ollama 

dev-down:
    docker compose down --remove-orphans

dev-restart: dev-down dev-up
    echo "Restarting development environment..."

logs SERVICE:
    docker compose logs -f {{SERVICE}}

test-up:
    docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d postgres ollama --force-recreate

build:
    uv build

build-dev:
    uv build --group=dev
