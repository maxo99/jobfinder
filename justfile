

dev-sync:
    uv sync --group=dev

dev-deploy:
    docker compose -f docker-compose.yml up -d

dev-down:
    docker compose -f docker-compose.yml down --remove-orphans

dev-logs:
    docker compose -f docker-compose.yml logs -f

test-deploy:
    docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d postgres ollama --force-recreate