---
name: npr-state-discipline
description: Keep NPR onboarding state, transcript, stage coverage, and canonical memory keys consistent
category: Domain
tier: project
when_to_use: NPR onboarding state updates, stage progression, profile memory persistence
related_skills:
  - discipline
  - npr-onboarding-conversation
---

# NPR State Discipline

Use this skill whenever updating NPR onboarding state or transcript memory.

## Required Invariants

- `pending_dimension` always names the question the user just answered or the next question to ask.
- Append the user's answer to `transcript` before increasing counts.
- Increment `current_stage_answer_count` and `total_answer_count` only for real user answers.
- Mark a stage complete only when both its minimum answer count and required coverage are satisfied.
- Store `memory_key`, `profile_key`, and `fsone_export_key` as soon as both user ID and preferred name are known.
- Use canonical profile memory under `npr/user/{safe_user_id}/{safe_username}`.

## Identity Fallback

If no runtime/user ID is available, create a local pseudo ID in the form:

`flowstate-npr-YYYYMMDD-shortname`

The pseudo ID is only a config-level fallback. Preserve any real application user ID if one is supplied later.

## Write Discipline

When both `transcript` and `session-state` change, write both before replying to the user. Do not synthesize while state says any required coverage is missing.

