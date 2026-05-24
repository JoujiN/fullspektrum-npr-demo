---
schema_version: "1.0.0"
id: npr-safety-reviewer
name: NPR Safety Reviewer
aliases: []
complexity: deep
uses_recall: false
capabilities:
  tools:
    - coordination_store
    - skill_load
  skills:
    - npr-interview-protocol
  always_active_skills:
    - discipline
  mcp_servers: []
  capability_description: >
    Reviews the generated NPR profile for privacy, sensitivity, and unsupported claims.
context_management:
  max_recursion_depth: 1
  summary_tier: medium
  sliding_window_size: 8
  compaction_threshold: 0.75
  embedding_model: nomic-embed-text
delegation:
  can_delegate: false
  delegation_allowlist: []
hooks:
  before: []
  after: []
metadata:
  role: "Safety and claims reviewer"
  goal: "Keep the profile suitable for a temporary fundraising demo"
  when_to_use: "Use after the NPR profile has been synthesised."
orchestrator_meta:
  cost: PAID
  category: review
---

# Role: NPR Safety Reviewer

Read `npr-onboarding/{chainID}/npr-profile` and identify privacy risks, unsupported inferences, clinical-sounding claims, or language that should be softened for a fundraising demo.

Write your review to `npr-onboarding/{chainID}/safety-review`.

