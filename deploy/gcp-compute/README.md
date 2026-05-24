# GCP Compute Engine Deployment

GCP's always-free `e2-micro` is not enough for the full stack. Use a paid VM or trial credits.

Candidate demo shapes:

- `e2-small`: possible if Qdrant and embeddings are light.
- `e2-medium`: safer single-box target for FlowState, Qdrant, and Ollama.

Use a standard persistent disk, firewall only the public web surface, and snapshot after rehearsal.

After provisioning the instance, follow `deploy/vps/README.md`.

