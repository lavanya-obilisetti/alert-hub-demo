#!/usr/bin/env python3
"""Classify the sample alerts: planned maintenance, known repeat, or new incident.

Uses only the fake files in sample-data/. Run:  python3 triage.py
"""
import json
from pathlib import Path

DATA = Path(__file__).parent / "sample-data"
TARGET_MIN = 60


def load(name):
    return json.loads((DATA / name).read_text())


def classify(alert, windows, tickets):
    """Rule order: maintenance first, then repeat, then new."""
    for w in windows:
        in_window = w["start_offset_min"] <= 0 <= w["end_offset_min"]  # offsets are relative to "now"
        if alert["host"] in w["hosts"] and in_window:
            return "maintenance", w["reason"]
    past = [t for t in tickets if t["signature"] == alert["signature"] and t["status"] == "closed"]
    if past:
        return f"repeat #{len(past) + 1}", past[0]["resolution"]
    return "new incident", ""


def main():
    alerts, tickets = load("alerts.json"), load("ticket_history.json")
    windows, runbooks = load("maintenance_windows.json"), load("runbooks.json")
    has_runbook = {r["signature"]: bool(r["title"]) for r in runbooks}

    print(f"{'ID':7} {'Host':18} {'Age':>5}  {'Result':16} {'Runbook':8} Note")
    print("-" * 86)
    for a in sorted(alerts, key=lambda x: -x["minutes_ago"]):
        result, note = classify(a, windows, tickets)
        over = " (over target)" if result != "maintenance" and a["minutes_ago"] > TARGET_MIN else ""
        rb = "yes" if has_runbook.get(a["signature"]) else "no"
        print(f"{a['id']:7} {a['host']:18} {a['minutes_ago']:>4}m  {result:16} {rb:8} {note}{over}")


if __name__ == "__main__":
    main()
