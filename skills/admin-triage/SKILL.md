---
name: admin-triage
description: Urgency and impact prioritisation for life-admin tasks, tuned for neurodivergent adults
category: Life Admin
tier: domain
when_to_use: When receiving a raw dump of overdue or avoided life-admin tasks and deciding what to act on first
related_skills:
  - deadline-urgency
  - npr-safety-boundaries
---

# Skill: Admin Triage

## What I Do

I apply a two-axis prioritisation matrix - urgency and impact - to life-admin tasks. I also identify friction patterns common for neurodivergent adults, so the output is not only "what matters first", but "what makes this startable".

Use consequence-based prioritisation, not shame-based prioritisation.

## The Matrix

```text
                 HIGH IMPACT          LOW IMPACT
HIGH URGENCY   | ACT NOW (1)       | DELEGATE/AUTOMATE (3) |
LOW URGENCY    | SCHEDULE (2)      | DROP/PARK (4)         |
```

Priority scores:

- `1` - Act Now: high urgency and high impact.
- `2` - Schedule: low urgency and high impact.
- `3` - Delegate/Automate: high urgency and low impact.
- `4` - Drop/Park: low urgency and low impact.

## Urgency Heuristics

Classify as high urgency if any of these apply:

- legal, regulatory, housing, employment, benefits, health, school/college, or tax deadline within 28 days
- fine, interest, arrears, service interruption, enforcement, missed appointment, or automatic rollover is possible
- notice, summons, claim, complaint, or request has a response-by date within 28 days
- renewal lapses within 14 days
- court date, appointment, hearing, review, inspection, or assessment is within 14 days
- deadline is unknown but the source is high-consequence, for example HMRC, council tax, court, landlord, NHS, DWP, DVLA, employer, insurer, lender

Classify as low urgency if:

- no material consequence is likely for at least 29 days
- deadline is self-imposed or aspirational
- reminder is proactive rather than overdue

## Impact Heuristics

Classify as high impact if inaction may lead to any of:

- financial penalty, fine, debt interest, arrears, or enforcement
- loss of legal status, tenancy risk, driving risk, passport/ID risk, right-to-work risk, or benefits disruption
- health risk, missed medication review, missed assessment, or treatment delay
- damaged relationship with statutory body, employer, school, landlord, bank, insurer, utility, or healthcare provider
- contract breach or automatic rollover at worse terms
- loss of access to essential services

Classify as low impact if:

- task is admin tidying with no external enforcement
- missed deadline means mild inconvenience
- worst case is resending a message, repeating an email, or making a non-urgent call

## Neurodivergent Friction Flags

Use these optional flags to explain why a task may be stuck:

- `time_blindness` - deadline is abstract, far away, or suddenly now.
- `demand_pressure` - task feels like a demand and may trigger freeze/avoidance.
- `working_memory_load` - too many details must be held at once.
- `uncertainty` - the user does not know what the notice means or what happens next.
- `phone_call` - the next step requires a call.
- `portal_login` - password, MFA, forms, or upload friction.
- `sensory_load` - travel, waiting rooms, noise, lighting, or paperwork environment.
- `shame_spiral` - task carries embarrassment, fear, or self-blame.
- `transition_cost` - task requires stopping another activity or leaving home.
- `paperwork_density` - dense forms, jargon, or many fields.

## Support Modes

Pick one support mode per task:

- `micro-step` - one action under 5 minutes.
- `body-double` - best done with co-working/accountability.
- `template` - needs wording, script, or form text.
- `phone-script` - needs a short call script.
- `calendar-anchor` - needs a date, reminder, and transition buffer.
- `low-power` - best handled in a minimal-energy version.
- `delegate` - can be handed to another person or service.
- `automate` - can be set as direct debit, renewal reminder, rule, or recurring task.

## Output Format

For each task emit:

```json
{
  "title": "Respond to council tax reminder",
  "deadline": "clarify urgently",
  "priority": 1,
  "urgency": "high",
  "impact": "high",
  "friction_flags": ["uncertainty", "shame_spiral"],
  "support_mode": "phone-script",
  "next_micro_action": "Find the letter and highlight the account/reference number.",
  "rationale": "Council tax reminders can escalate if ignored."
}
```

## Example Prioritisation Decisions

| Task | Urgency | Impact | Priority | Rationale |
|---|---|---:|---:|---|
| HMRC self-assessment overdue by 3 months | high | high | 1 | Penalties and interest may escalate. |
| Respond to council tax reminder letter | high | high | 1 | Ignored reminders can lead to enforcement. |
| Renew car insurance, expires in 10 days | high | high | 1 | Driving uninsured has legal and financial consequences. |
| Book annual GP check-up | low | high | 2 | Not immediate, but health impact is meaningful. |
| Review broadband contract rolling over next month | low | high | 2 | Contract may renew on worse terms. |
| Set up direct debit for water bill | high | low | 3 | Useful and time-sensitive, but can often be automated. |
| File old bank statements | low | low | 4 | No immediate external consequence. |

## Edge Cases

- Uncertain deadline and high-consequence source: use `deadline: "clarify urgently"` and usually `priority: 1`.
- Uncertain deadline and low-consequence source: use `deadline: "clarify when ready"` and likely `priority: 4`.
- Multiple tasks, single bill: collapse duplicates and preserve the highest urgency.
- Task needs more information: make the first micro-action "identify the reference/date/amount" rather than "solve the whole task".
- User is overwhelmed: return the smallest safe plan: one Act Now item, one Schedule item, and one Park item.

## Language Rules

- Use neutral phrases: "stuck", "friction", "next visible step", "support needed".
- Avoid moralising phrases: "lazy", "irresponsible", "failed", "should have", "just do it".
- Do not diagnose. Describe patterns and supports only.
