# Hosting Notes

This demo is short-term fundraising infrastructure. Optimise for reliable setup, easy teardown, and durable enough state for the demo window.

## Does Provider Choice Change The Implementation?

Only at the deployment wrapper layer.

The common implementation should stay:

- One FlowState backend binary installed from a pinned FlowState ref.
- One systemd service for the FlowState backend.
- One private Qdrant sidecar with persistent storage.
- One Vercel-hosted FlowState web UI pointed at the API origin.
- Optional external Ollama or embedding service when GPU capacity exists.
- FullSpektrum config, agents, skills, schemas, and swarms copied into FlowState config.

Provider-specific work should live under `deploy/` and cover host bootstrap, firewall, DNS, TLS, and backup/snapshot instructions.

## Recommended Short-Term Hosts

### AWS Lightsail

Best main-provider default for a temporary demo. A 2 GB instance can be enough for FlowState plus Qdrant if embeddings are external; use 4 GB for more headroom.

### AWS EC2

Good if you need standard AWS primitives. `t4g.small` can be attractive while the T4g free trial is available, but it is ARM64 and only 2 GB RAM. Validate the FlowState build and memory pressure before committing to a live demo.

### GCP Compute Engine

Viable on a paid VM or with trial credits. The always-free `e2-micro` is too small for a comfortable backend plus Qdrant demo.

### Oracle Always Free

Technically a strong free option. Use it only if capacity is already secured and the backend has been soak-tested.

### Hetzner

Not free. It remains one of the cheapest reliable paid VPS options if main-provider branding is not important.

## Sizing

Minimum credible backend target:

- 2 vCPU.
- 2 GB RAM.
- 40 GB persistent disk.

For extra safety during a live fundraising demo:

- 4 GB RAM if Qdrant will hold meaningful demo memory.
- Externalize Ollama or any GPU-backed embedding workload.
- Snapshot `/var/lib/fullspektrum/flowstate` and the Qdrant volume after a successful rehearsal.
- Keep provider API spend caps enabled outside this repo.
