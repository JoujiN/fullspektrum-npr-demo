# AWS Lightsail Deployment

Lightsail is the simplest AWS-shaped option for a temporary fundraising demo.

Recommended instance:

- 2 GB RAM for FlowState plus private Qdrant with embeddings external.
- 4 GB RAM for more headroom during a live demo.

## Steps

1. Create an Ubuntu Lightsail instance.
2. Attach a static IP.
3. Allow inbound HTTP/HTTPS only for the public FlowState API reverse proxy.
4. SSH into the instance and follow `deploy/vps/README.md`.
5. Snapshot after a successful rehearsal.

Keep Qdrant, FlowState's localhost port, and any Ollama endpoint private. The public surface should be the HTTPS reverse proxy for the FlowState API only.
