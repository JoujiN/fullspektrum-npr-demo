---
name: npr-evidence-synthesis
description: Convert NPR onboarding transcript evidence into calibrated, schema-ready profile claims
category: Domain
tier: project
when_to_use: NPR profile synthesis, profile review, evidence calibration
related_skills:
  - epistemic-rigor
  - critical-thinking
  - npr-safety-boundaries
---

# NPR Evidence Synthesis

Use this skill when turning onboarding answers into profile content.

## Evidence Rules

- Use only transcript/state evidence.
- Prefer a small number of well-supported traits over many weak ones.
- Every trait should have a source that points back to something the user said.
- Lower confidence when evidence is sparse, indirect, or contradicted.
- Preserve uncertainty in plain language instead of filling gaps.

## Claim Calibration

- Strong repeated evidence: confidence around `0.75` to `0.9`.
- Clear single answer: confidence around `0.55` to `0.7`.
- Inferred or partial evidence: confidence around `0.35` to `0.55`.
- Do not include claims with no evidence.

## Output Bias

The profile should help the product adapt to the user. Favour practical preferences, support needs, goals, constraints, and interaction guidance over personality labels.

