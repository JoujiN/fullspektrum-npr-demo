.PHONY: check build up down logs bootstrap pull-embedding ps

check:
	bash scripts/check-demo.sh

build:
	docker compose build

up:
	docker compose up -d --build

pull-embedding:
	docker compose exec ollama ollama pull "$${EMBEDDING_MODEL:-nomic-embed-text}"

bootstrap: check up pull-embedding

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

ps:
	docker compose ps

