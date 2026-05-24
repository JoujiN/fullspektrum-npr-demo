# Generic VPS Deployment

Use this path for Hetzner, DigitalOcean, Linode, AWS, GCP, or any plain Ubuntu/Debian VM.

The default VPS shape is backend-only:

- FlowState binary runs under systemd on `127.0.0.1:8080`.
- FlowState config/data live under `/var/lib/fullspektrum/flowstate`.
- Qdrant runs privately with Docker Compose and binds only to localhost.
- HTTPS reverse proxy exposes the FlowState API origin.
- The FlowState web UI is deployed separately to Vercel.
- Ollama is optional/external. Do not add it as a default service here.

## 1. Install Host Packages

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates git make build-essential golang-go docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

The distro `golang-go` package is convenient for bootstrapping, but confirm the version before building:

```bash
go version
```

## 2. Install This Repo's Assets

```bash
sudo install -d /opt/fullspektrum
sudo git clone <this-repo-url> /opt/fullspektrum/npr-demo
cd /opt/fullspektrum/npr-demo
sudo install -m 0755 scripts/write-flowstate-config.sh /usr/local/bin/write-flowstate-config
```

Create the service user and data directories:

```bash
sudo useradd --system --home /var/lib/fullspektrum/flowstate --shell /usr/sbin/nologin flowstate || true
sudo install -d -o flowstate -g flowstate /var/lib/fullspektrum/flowstate/config
sudo install -d -o flowstate -g flowstate /var/lib/fullspektrum/flowstate/data
sudo install -d /etc/fullspektrum
sudo cp .env.example /etc/fullspektrum/flowstate.env
sudo nano /etc/fullspektrum/flowstate.env
```

Set at least:

```text
FLOWSTATE_REF=<immutable FlowState commit SHA or tag>
ANTHROPIC_API_KEY=...
FLOWSTATE_AUTH_SECRET=...
FLOWSTATE_AUTH_CSRF_KEY=...
FLOWSTATE_AUTH_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
FULLSPEKTRUM_ASSET_ROOT=/opt/fullspektrum/npr-demo
```

Generate auth secrets with:

```bash
openssl rand -base64 32
openssl rand -base64 32
```

## 3. Build FlowState From A Pinned Ref

```bash
set -a
. /etc/fullspektrum/flowstate.env
set +a

mkdir -p /tmp/fullspektrum-build
cd /tmp/fullspektrum-build
git clone "$FLOWSTATE_REPO" flowstate
cd flowstate
git fetch --depth 1 origin "$FLOWSTATE_REF"
git checkout --detach FETCH_HEAD
grep -E '^(go|toolchain) ' go.mod
GOTOOLCHAIN=local make build
sudo install -m 0755 build/flowstate /usr/local/bin/flowstate
/usr/local/bin/flowstate --help
```

For a deterministic demo build, use the exact Go version required by the pinned FlowState ref before running `make build`. Prefer the `toolchain` directive in FlowState's `go.mod` when present; otherwise use the approved patch release for the `go` directive's minor version:

```bash
GO_VERSION=<required version, for example 1.24.3>
GO_ARCH=linux-amd64
curl -fsSLO "https://go.dev/dl/go${GO_VERSION}.${GO_ARCH}.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go${GO_VERSION}.${GO_ARCH}.tar.gz"
export PATH="/usr/local/go/bin:$PATH"
export GOTOOLCHAIN=local
go version
```

Use `GO_ARCH=linux-arm64` on ARM64 hosts.

Record the deployed FlowState revision:

```bash
git rev-parse HEAD
```

## 4. Choose A Demo Mode

1. No recall / no embeddings: leave `QDRANT_URL`, `OLLAMA_HOST`, and `EMBEDDING_MODEL` empty. Skip the Qdrant step below. This is useful for API/auth/frontend smoke tests, but recall-dependent behavior will be unavailable.
2. Qdrant + external embeddings: set `QDRANT_URL=http://127.0.0.1:6333`, set `OLLAMA_HOST` to a working external or host-local embedding service, and set `EMBEDDING_MODEL=nomic-embed-text`.

## 5. Start Private Qdrant

From `/opt/fullspektrum/npr-demo`:

```bash
sudo docker compose up -d qdrant
sudo docker compose ps
curl http://127.0.0.1:6333/healthz
```

The Compose file publishes Qdrant only on `127.0.0.1`. Do not expose `6333/tcp` or `6334/tcp` publicly.

## 6. Install The systemd Service

Install the concrete unit file from this repo:

```bash
sudo install -m 0644 deploy/vps/flowstate.service /etc/systemd/system/flowstate.service
```

Start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now flowstate
sudo systemctl status flowstate
curl http://127.0.0.1:8080/
```

`ExecStartPre=/usr/local/bin/write-flowstate-config` rewrites the generated FlowState config on every restart, so changes in `/etc/fullspektrum/flowstate.env` are picked up after `sudo systemctl restart flowstate`.

## 7. Pre-Demo Smoke Test

No recall / no embeddings mode:

```bash
sudo sed -i 's#^QDRANT_URL=.*#QDRANT_URL=#' /etc/fullspektrum/flowstate.env
sudo sed -i 's#^OLLAMA_HOST=.*#OLLAMA_HOST=#' /etc/fullspektrum/flowstate.env
sudo sed -i 's#^EMBEDDING_MODEL=.*#EMBEDDING_MODEL=#' /etc/fullspektrum/flowstate.env
sudo systemctl restart flowstate
sudo stat -c '%a' /var/lib/fullspektrum/flowstate/config/flowstate/config.yaml | grep -qx 600
! sudo grep -Eq '^(qdrant:|embedding_model:)' /var/lib/fullspektrum/flowstate/config/flowstate/config.yaml
curl -fsS http://127.0.0.1:8080/ >/dev/null
```

Qdrant + external embeddings mode:

```bash
sudo docker compose ps qdrant
curl -fsS http://127.0.0.1:6333/healthz
```

Set `QDRANT_URL=http://127.0.0.1:6333`, `OLLAMA_HOST`, and `EMBEDDING_MODEL` in `/etc/fullspektrum/flowstate.env`, then verify the external embedding service from the VPS. For Ollama-compatible services:

```bash
. /etc/fullspektrum/flowstate.env
curl -fsS "$OLLAMA_HOST/api/tags" >/dev/null
sudo systemctl restart flowstate
sudo grep -E '^(qdrant:|embedding_model:)' /var/lib/fullspektrum/flowstate/config/flowstate/config.yaml
```

Vercel frontend to backend:

- Open the Vercel web UI and sign in against the HTTPS API origin.
- Start `@npr-onboarding Start a new NPR onboarding for userId=demo-smoke`.
- Confirm the session cookie is set for the API origin, the chat response streams progressively, and `journalctl -u flowstate -n 100` shows no auth, CORS, or stream disconnect errors.

## 8. Expose Only The API Through HTTPS

Open only:

- `22/tcp` for SSH.
- `80/tcp` for ACME HTTP challenge, if your proxy needs it.
- `443/tcp` for the public FlowState API origin.

Keep `8080`, `6333`, `6334`, and any Ollama port private.

Use one of the concrete examples in this repo and replace `api.example.com`:

```bash
deploy/vps/caddy.example.Caddyfile
deploy/vps/nginx.example.conf
```

Set `FLOWSTATE_AUTH_SECURE_COOKIES=true` and include the Vercel frontend origin in `FLOWSTATE_AUTH_ALLOWED_ORIGINS`.

## 9. Optional External Ollama

Ollama is not part of the default Docker Compose stack. If the demo needs local embeddings, run Ollama on a separate GPU host or as a host-local service, then set:

```text
OLLAMA_HOST=https://ollama.example.internal
EMBEDDING_MODEL=nomic-embed-text
```

Keep that endpoint private or otherwise protected.
