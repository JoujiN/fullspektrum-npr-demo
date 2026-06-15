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
- Store `memory_key`, `profile_key`, and `profile_export_key` as soon as both user ID and preferred name are known.
- Use canonical profile memory under `npr/user/{safe_user_id}/{safe_username}`.
- Keep live draft state, transcripts, stage insights, synthesis output, reviews, and human summaries under the runtime `{chainID}/...` coordination-store namespace.
- Do not read or write legacy static `npr-onboarding/...` draft keys when a runtime `{chainID}` is available.

## Identity Fallback

If no runtime/user ID is available, create a local pseudo ID in the form:

`flowstate-npr-YYYYMMDD-shortname`

The pseudo ID is only a config-level fallback. Preserve any real application user ID if one is supplied later.

If a supplied application user ID conflicts with an existing chain-local `session-state.userId`, treat the existing state and transcript as belonging to another account/session. Initialise fresh draft state under the current `{chainID}` and do not copy the foreign transcript.

## Write Discipline

When both `transcript` and `session-state` change, write both before replying to the user. Do not synthesize while state says any required coverage is missing.
