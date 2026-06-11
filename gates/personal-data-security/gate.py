#!/usr/bin/env python3
"""Personal data security gate for FlowState ext-gate payloads."""
import base64
import json
import os
import re
import sys
from typing import Any


PATTERNS = {
    "NI_NUMBER": re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]?\b"),
    "NHS_NUMBER": re.compile(r"\b\d{3}\s?\d{3}\s?\d{4}\b"),
    "UK_POSTCODE": re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", re.IGNORECASE),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "UK_PHONE": re.compile(r"\b(?:\+44\s?\d{4}|\(?0\d{2,4}\)?)\s?\d{3,4}\s?\d{3,4}\b"),
    "DOB": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-](?:19|20)\d{2}\b"),
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}\b"),
}


def decode_payload(payload: Any) -> Any:
    if isinstance(payload, (dict, list)):
        return payload
    if payload is None:
        return ""
    if isinstance(payload, str):
        raw = payload.strip()
        decoded = _try_b64(raw)
        if decoded is not None:
            raw = decoded
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return payload


def _try_b64(value: str) -> str | None:
    try:
        decoded = base64.b64decode(value, validate=True)
    except Exception:
        return None
    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return None


def flatten(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, ensure_ascii=False)


def scan(text: str) -> list[tuple[str, str, tuple[int, int]]]:
    findings: list[tuple[str, str, tuple[int, int]]] = []
    for category, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append((category, match.group(0), match.span()))
    return findings


def redact(text: str, findings: list[tuple[str, str, tuple[int, int]]]) -> str:
    out = text
    for category, _match, (start, end) in sorted(findings, key=lambda item: item[2][0], reverse=True):
        out = out[:start] + f"[REDACTED:{category}]" + out[end:]
    return out


def main() -> None:
    req = json.load(sys.stdin)
    payload = decode_payload(req.get("payload", req.get("content", "")))

    policy = req.get("policy") or {}
    action = (
        req.get("mode")
        or policy.get("action")
        or policy.get("mode")
        or os.environ.get("PDS_MODE")
        or "strip"
    ).lower()

    text = flatten(payload)
    findings = scan(text)

    if not findings:
        json.dump({"pass": True, "categories_checked": list(PATTERNS.keys())}, sys.stdout)
        return

    counts: dict[str, int] = {}
    for category, _match, _span in findings:
        counts[category] = counts.get(category, 0) + 1
    summary = [{"category": category, "count": count} for category, count in sorted(counts.items())]

    if action == "block":
        examples = [match for _category, match, _span in findings[:5]]
        json.dump(
            {
                "pass": False,
                "reason": "personal data detected",
                "categories": [item["category"] for item in summary],
                "examples": examples,
            },
            sys.stdout,
        )
        return

    redactions = [
        {"category": category, "original": match, "position": span[0]}
        for category, match, span in sorted(findings, key=lambda item: item[2][0])
    ]
    json.dump(
        {
            "pass": True,
            "output": redact(text, findings),
            "redactions": redactions,
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
