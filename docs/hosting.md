# Hosting Notes

This demo is short-term fundraising infrastructure. Optimise for reliable setup, easy teardown, and durable enough state for the demo window.

## Does Provider Choice Change The Implementation?

Only at the deployment wrapper layer.

The common implementation should stay:

- One FlowState backend container.
- One FlowState web container.
- One Qdrant sidecar with persistent storage.
- One Ollama sidecar or external embedding endpoint.
- Mounted FullSpektrum config, agents, skills, schemas, and swarms.

Provider-specific work should live under `deploy/` and cover host bootstrap, firewall, DNS, TLS, and backup/snapshot instructions.

## Recommended Short-Term Hosts

### AWS Lightsail

Best main-provider default for a temporary demo. Use 4 GB RAM if running FlowState, Qdrant, and Ollama together. The 2 GB plan may work for light demos but leaves little headroom.

### AWS EC2

Good if you need standard AWS primitives. `t4g.small` can be attractive while the T4g free trial is available, but it is ARM64 and only 2 GB RAM. Validate Docker images and memory pressure before committing to a live demo.

### GCP Compute Engine

Viable on a paid VM or with trial credits. The always-free `e2-micro` is too small for the full stack.

### Oracle Always Free

Technically the strongest free option. Use it only if capacity is already secured and the full stack has been soak-tested.

### Hetzner

Not free. It remains one of the cheapest reliable paid VPS options if main-provider branding is not important.

## Sizing

Minimum credible single-box target:

- 2 vCPU.
- 4 GB RAM.
- 40 GB persistent disk.

For extra safety during a live fundraising demo:

- 4 GB RAM minimum.
- Snapshot the host or Docker volumes after a successful rehearsal.
- Keep provider API spend caps enabled outside this repo.

