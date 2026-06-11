#!/usr/bin/env python3
"""Validate adulting triage output for downstream specialists."""
import base64
import json
import sys
from typing import Any


def decode_payload(payload: Any) -> Any:
    if isinstance(payload, (dict, list)):
        return payload
    if payload is None:
        return {}
    if isinstance(payload, str):
        raw = payload.strip()
        if not raw:
            return {}
        for candidate in (raw, _try_b64(raw)):
            if candidate is None:
                continue
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
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


def main() -> None:
    try:
        req = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        json.dump({"pass": False, "reason": f"invalid JSON input: {exc}"}, sys.stdout)
        return

    payload = decode_payload(req.get("payload"))
    if isinstance(payload, dict) and "tasks" not in payload and "payload" in payload:
        payload = decode_payload(payload.get("payload"))

    if not isinstance(payload, dict):
        json.dump({"pass": False, "reason": "payload must be an object with a 'tasks' key"}, sys.stdout)
        return

    tasks = payload.get("tasks")
    if not isinstance(tasks, list):
        json.dump({"pass": False, "reason": "payload missing 'tasks' list"}, sys.stdout)
        return
    if not tasks:
        json.dump({"pass": False, "reason": "tasks list is empty"}, sys.stdout)
        return

    incomplete: list[str] = []
    for task in tasks:
        if not isinstance(task, dict):
            incomplete.append("<non-object task entry>")
            continue

        title = task.get("title") or "<untitled>"
        deadline = task.get("deadline")
        priority = task.get("priority")

        missing: list[str] = []
        if not deadline or (isinstance(deadline, str) and not deadline.strip()):
            missing.append("deadline")
        if priority is None:
            missing.append("priority")
        elif not isinstance(priority, int) or not (1 <= priority <= 4):
            missing.append("priority (must be integer 1-4)")

        if missing:
            incomplete.append(f"{title} (missing: {', '.join(missing)})")

    if incomplete:
        reason = f"{len(incomplete)} task(s) failed validation: {'; '.join(incomplete)}"
        json.dump({"pass": False, "reason": reason, "incomplete": incomplete}, sys.stdout)
        return

    json.dump({"pass": True}, sys.stdout)


if __name__ == "__main__":
    main()
