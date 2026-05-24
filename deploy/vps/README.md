# Generic VPS Deployment

Use this path for Hetzner, DigitalOcean, Linode, or any plain Ubuntu/Debian VM.

## Host Setup

Install Docker and the Compose v2 plugin, then clone this repository:

```bash
git clone <this-repo-url> fullspektrum-npr-demo
cd fullspektrum-npr-demo
cp .env.example .env
nano .env
```

Set provider credentials and auth secrets, then run:

```bash
make bootstrap
```

Open firewall ports:

- `22/tcp` for SSH.
- `80/tcp` and `443/tcp` if putting a reverse proxy in front.
- Or only the configured `WEB_PORT` for a private temporary demo.

Do not expose Qdrant or Ollama directly to the public internet.

