#!/usr/bin/env python3
"""NPR onboarding completion gate for config-only FlowState deployments."""

import base64
import binascii
import json
import re
import sys


STAGES = {
    1: {
        "minimum": 5,
        "required": [
            "preferred_name",
            "reason_for_using_system",
            "role_context",
            "working_style",
            "personalising_follow_up",
        ],
    },
    2: {
        "minimum": 5,
        "required": [
            "archetype",
            "role_context",
            "primary_intent",
            "time_horizon",
            "decision_making_style",
        ],
    },
    3: {
        "minimum": 6,
        "required": [
            "information_processing",
            "cognitive_load",
            "communication_preferences",
            "stress_response",
            "values_motivation",
            "learning_style",
        ],
    },
    4: {
        "minimum": 5,
        "required": [
            "team_dynamics",
            "multi_agency_coordination",
            "digital_environment",
            "accessibility_preferences",
            "risk_uncertainty",
        ],
    },
    5: {
        "minimum": 5,
        "required": [
            "knowledge_baseline",
            "experience",
            "confidence_map",
            "development_goals",
            "ethical_framework",
        ],
    },
    6: {
        "minimum": 6,
        "required": [
            "executive_function",
            "working_memory",
            "attention_regulation",
            "emotional_processing",
            "sensory_processing",
            "load_management",
        ],
    },
}

ALIASES = {
    "reason_for_using": "reason_for_using_system",
    "reason_for_using_the_system": "reason_for_using_system",
    "role": "role_context",
    "context": "role_context",
    "one_personalising_follow_up": "personalising_follow_up",
    "personalizing_follow_up": "personalising_follow_up",
    "values_and_motivation": "values_motivation",
    "risk_and_uncertainty": "risk_uncertainty",
    "multi_agency": "multi_agency_coordination",
    "accessibility": "accessibility_preferences",
    "ethics": "ethical_framework",
    "executive_functioning": "executive_function",
    "attention": "attention_regulation",
    "communication_preference": "communication_preferences",
    "decision_making": "decision_making_style",
    "development_goal": "development_goals",
    "domain_knowledge_baseline": "knowledge_baseline",
    "confidence": "confidence_map",
    "work_style": "working_style",
    "name": "preferred_name",
    "professional_role_context": "role_context",
    "professional_context": "role_context",
    "professional_archetype": "archetype",
}


def emit(body):
    json.dump(body, sys.stdout)
    sys.stdout.write("\n")


def decode_payload(raw):
    if raw is None or raw == "":
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            pass
        try:
            decoded = base64.b64decode(raw, validate=True)
            return json.loads(decoded.decode("utf-8"))
        except (binascii.Error, ValueError, json.JSONDecodeError):
            return None
    return None


def coerce_json(value, fallback):
    if value is None:
        return fallback
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return fallback
    return fallback


def normalise(value):
    value = str(value or "").lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return ALIASES.get(value, value)


def add_coverage(coverage, stage, dimension):
    if not stage or not dimension:
        return
    coverage.setdefault(stage, set()).add(normalise(dimension))


def intish(value):
    try:
        return int(value)
    except Exception:
        return 0


def collect_from_state(state, coverage):
    current_stage = intish(state.get("current_stage"))
    for key in ("answered_dimensions", "covered_dimensions"):
        for dimension in state.get(key) or []:
            add_coverage(coverage, current_stage, dimension)

    for key in ("stage_coverage", "coverage", "stageCoverage"):
        block = state.get(key)
        if not isinstance(block, dict):
            continue
        for stage_key, raw in block.items():
            stage = intish(stage_key)
            if isinstance(raw, list):
                for dimension in raw:
                    add_coverage(coverage, stage, dimension)
            elif isinstance(raw, dict):
                for dimension, enabled in raw.items():
                    if enabled:
                        add_coverage(coverage, stage, dimension)


def collect_from_transcript(transcript, coverage, counts):
    for entry in transcript:
        if not isinstance(entry, dict):
            continue
        stage = intish(entry.get("stage"))
        if not stage:
            continue
        if entry.get("answer") or entry.get("value") or entry.get("response") or entry.get("text"):
            counts[stage] = counts.get(stage, 0) + 1
        dimension = (
            entry.get("dimension")
            or entry.get("pending_dimension")
            or entry.get("field")
            or entry.get("key")
        )
        add_coverage(coverage, stage, dimension)


def main():
    try:
        req = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        emit({"pass": False, "reason": f"invalid request JSON: {exc}"})
        return

    payload = decode_payload(req.get("payload"))
    if payload is None:
        emit({"pass": False, "reason": "payload is not valid JSON"})
        return

    state = coerce_json(payload.get("session_state"), {})
    transcript = coerce_json(payload.get("transcript"), [])
    if not isinstance(state, dict):
        state = {}
    if not isinstance(transcript, list):
        transcript = []

    coverage = {}
    counts = {}
    collect_from_state(state, coverage)
    collect_from_transcript(transcript, coverage, counts)

    total_answers = sum(counts.values()) or intish(state.get("total_answer_count"))
    minimum_total = intish((req.get("policy") or {}).get("minimum_total_answers")) or 32

    failures = []
    for stage, spec in STAGES.items():
        missing = [dim for dim in spec["required"] if dim not in coverage.get(stage, set())]
        count = counts.get(stage, 0)
        if intish(state.get("current_stage")) == stage:
            count = max(count, intish(state.get("current_stage_answer_count")))
        if missing or count < spec["minimum"]:
            failures.append({
                "stage": stage,
                "answer_count": count,
                "minimum": spec["minimum"],
                "missing_dimensions": missing,
            })

    if total_answers < minimum_total:
        failures.append({
            "stage": "all",
            "answer_count": total_answers,
            "minimum": minimum_total,
            "missing_dimensions": [],
        })

    if failures:
        first = failures[0]
        emit({
            "pass": False,
            "reason": "NPR onboarding is not complete enough to synthesize a profile",
            "first_incomplete": first,
            "failures": failures,
        })
        return

    emit({
        "pass": True,
        "reason": "NPR onboarding completion requirements satisfied",
        "total_answer_count": total_answers,
    })


if __name__ == "__main__":
    main()
