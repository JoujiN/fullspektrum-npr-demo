# AWS Lightsail Deployment

Lightsail is the simplest AWS-shaped option for a temporary fundraising demo.

Recommended instance:

- 4 GB RAM if running FlowState, Qdrant, and Ollama on the same host.
- 2 GB RAM only after a rehearsal proves it is stable enough.

## Steps

1. Create an Ubuntu Lightsail instance.
2. Attach a static IP.
3. Allow inbound HTTP/HTTPS only for the public demo surface.
4. SSH into the instance and follow `deploy/vps/README.md`.
5. Snapshot after a successful rehearsal.

Keep Qdrant and Ollama bound to Docker's internal network. The public surface should be the web container or a reverse proxy in front of it.

