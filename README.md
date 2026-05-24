# FullSpektrum NPR Demo

This repository packages the FullSpektrum NPR onboarding demo outside the core FlowState repository.

FlowState stays the generic runtime. This repo owns the downstream application layer: demo configuration, NPR swarm assets, Docker packaging, Qdrant/Ollama sidecars, and provider-specific deployment notes.

## What This Runs

- FlowState API from a pinned FlowState git ref.
- FlowState web UI from the same pinned FlowState git ref.
- Qdrant with a persistent Docker volume.
- Ollama for the `nomic-embed-text` embedding model.
- FullSpektrum NPR swarm, agents, skills, and schemas mounted into FlowState config.

## Quickstart

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```bash
ANTHROPIC_API_KEY=...
FLOWSTATE_AUTH_SECRET=...
FLOWSTATE_AUTH_CSRF_KEY=...
```

Generate the auth secrets with:

```bash
openssl rand -base64 32
openssl rand -base64 32
```

Start the stack:

```bash
make bootstrap
```

Open:

```text
http://localhost:8081
```

Start the demo from chat:

```text
@npr-onboarding Start a new NPR onboarding for userId=demo-user
```

## Host Choice

The packaging is deliberately VM-friendly. A short-term fundraising demo should run cleanly on one small Linux host with Docker Compose.

Recommended shapes:

- AWS Lightsail 4 GB for a main-provider demo with low ops friction.
- AWS EC2 `t4g.small` only if ARM64 and 2 GB RAM are acceptable.
- GCP Compute Engine paid VM or trial credits when GCP is preferred.
- Oracle Always Free only after capacity and boot have already been proven.
- Hetzner 4 GB when cheapest reliable paid hosting matters; it is not free.

See [docs/hosting.md](docs/hosting.md).

## FlowState Boundary

Do not upstream this repository into FlowState. If this packaging reveals a generic FlowState platform gap, fix that gap in FlowState with a narrowly-scoped PR. Keep FullSpektrum-specific swarm assets and deployment decisions here.

## Common Commands

```bash
make check
make build
make up
make pull-embedding
make logs
make down
```

## Data

Docker named volumes hold demo state:

- `fullspektrum-flowstate-config`
- `fullspektrum-flowstate-data`
- `fullspektrum-qdrant-data`
- `fullspektrum-ollama-data`

For temporary fundraising demos, snapshot or export these before deleting the host if the session history matters.

