# GCP Compute Engine Deployment

GCP's always-free `e2-micro` is not enough for a comfortable backend plus Qdrant demo. Use a paid VM or trial credits.

Candidate demo shapes:

- `e2-small`: possible for FlowState plus private Qdrant with embeddings external.
- `e2-medium`: safer backend target with more rehearsal headroom.

Use a standard persistent disk, firewall only SSH plus the HTTPS API reverse proxy, and snapshot after rehearsal.

After provisioning the instance, follow `deploy/vps/README.md`.
