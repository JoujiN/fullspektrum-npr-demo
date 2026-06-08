# AWS EC2 Deployment

Use EC2 when you need standard AWS primitives rather than Lightsail simplicity.

Candidate demo shapes:

- `t4g.small`: low-cost/free-trial candidate, ARM64, 2 GB RAM.
- `t4g.medium`: safer ARM64 shape with more headroom.
- `t3.medium`: x86_64 fallback if ARM64 causes image or dependency friction.

Attach persistent EBS storage and snapshot after rehearsal. Restrict the security group to SSH plus HTTP/HTTPS for the API reverse proxy. Do not expose Qdrant, FlowState's localhost port, or any Ollama endpoint publicly.

After provisioning the instance, follow `deploy/vps/README.md`.
