.PHONY: check up down logs bootstrap ps qdrant-up qdrant-down qdrant-logs qdrant-ps

check:
	bash scripts/check-demo.sh

up: qdrant-up

qdrant-up:
	docker compose up -d qdrant

bootstrap: check up

down: qdrant-down

qdrant-down:
	docker compose down

logs: qdrant-logs

qdrant-logs:
	docker compose logs -f --tail=100

ps: qdrant-ps

qdrant-ps:
	docker compose ps
