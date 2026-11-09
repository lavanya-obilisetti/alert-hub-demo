# Triage rules

Every alert, from any source, goes through the same three steps.

1. **Normalize.** Convert the alert to one shape: source, channel, severity, environment, host, check, title, start time and a `signature` (`host:check`).
2. **Check planned maintenance.** If the host is inside a maintenance window right now, mark the alert *planned maintenance* and move it out of the main queue. It stays visible in a collapsed list so nothing is hidden.
3. **Check history.** If a closed ticket with the same signature exists, mark the alert *repeat #N* and show the last fix. Otherwise it is a *new incident*.

## What the dashboard adds

| Signal | Why it matters |
| --- | --- |
| Time left against a 60-minute response target | Shows what to pick up first and what is overdue |
| "No ticket yet" tag | Finds alerts nobody has logged |
| Runbook found or missing | Finds alert types that need a runbook written |
| Unassigned tickets | Finds work waiting for an owner |
| One chip per source | Shows a quiet source at a glance, so a broken integration is not mistaken for "no alerts" |

## Where an AI assistant helps

An assistant can read the normalized alert, the ticket history and the runbook, then suggest a first-pass classification and next step for a person to confirm. In this demo the rules are plain code, so the logic is easy to read and test. All data here is invented.
