# FullSpektrum NPR Demo

This repository packages the FullSpektrum NPR onboarding demo outside the core FlowState repository.

FlowState stays the generic runtime and should remain untouched by this repo. This repo owns the downstream NPR demo assets and backend deployment support only.

## Architecture

- FlowState backend binary built from a pinned FlowState ref and run with systemd on the VPS.
- FlowState config and data under `/var/lib/fullspektrum/flowstate`.
- FullSpektrum NPR agents, skills, swarms, schemas, gates, and generated FlowState config from this repo.
- Qdrant as an optional private Docker Compose sidecar bound to `127.0.0.1`.
- FlowState web UI hosted separately on Vercel.
- Ollama as an optional external service; GPU placement is handled outside this repo.

## What Was Removed From The Default Stack

- The FlowState web container and nginx static/proxy config.
- The default FlowState API container from Compose.
- The leftover FlowState Docker runtime helper.
- The default Ollama Docker service and Ollama volume.
- Full-stack bootstrap commands that tried to run API, web, Qdrant, and embeddings together.

The default deployment path is now backend-only: systemd runs FlowState, Compose only provides private sidecars, and Vercel owns the frontend.

## Quickstart

```bash
cp .env.example .env
make check
```

To run the actual backend on a VPS, follow [deploy/vps/README.md](deploy/vps/README.md). To connect the Vercel-hosted frontend, follow [deploy/vercel/README.md](deploy/vercel/README.md).

## Demo Modes

1. No recall / no embeddings: leave `QDRANT_URL`, `OLLAMA_HOST`, and `EMBEDDING_MODEL` empty, and do not start Qdrant. This is the smallest mode for API/auth/frontend smoke tests; recall-dependent behavior will be unavailable.
2. Qdrant + external embeddings: run `make up` for private Qdrant, set `QDRANT_URL=http://127.0.0.1:6333`, and point `OLLAMA_HOST` plus `EMBEDDING_MODEL` at a working external embedding service.

Start the demo from chat in the FlowState web UI:

```text
@npr-onboarding Start a new NPR onboarding for userId=demo-user
```

## Host Choice

The packaging is VM-friendly but no longer needs one host to run the whole web/API/embedding appliance. A short-term fundraising demo can use one small Linux host for FlowState plus Qdrant, with the web UI on Vercel and embeddings hosted separately if needed.

See [docs/hosting.md](docs/hosting.md).

## FlowState Boundary

Do not upstream this repository into FlowState. If this packaging reveals a generic FlowState platform gap, fix that gap in FlowState with a narrowly-scoped PR. Keep FullSpektrum-specific swarm assets and deployment decisions here.

## Common Commands

```bash
make check
make up
make logs
make ps
make down
```

These commands manage the private Qdrant sidecar only.

## Data

FlowState should use:

- `/var/lib/fullspektrum/flowstate/config`
- `/var/lib/fullspektrum/flowstate/data`

Qdrant uses the Docker named volume:

- `fullspektrum-qdrant-data`

For temporary fundraising demos, snapshot or export these before deleting the host if the session history matters.
