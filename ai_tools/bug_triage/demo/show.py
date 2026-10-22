"""Print a compact summary of `bug-triage triage` JSON read from stdin."""

import json
import sys

r = json.load(sys.stdin)
d = r["decision"]
t1 = r["trace"][0]["prediction"]
print(f"  tier1:    {t1['component']} -> {t1['team']}")
print(
    f"  decision: {d['component']} -> {d['team']}  "
    f"(source={d['source']}, escalated={d['escalated']}, confidence={d['confidence']:.2f})"
)
print(f"  contact:  {d['assignee']} (suggested)   severity: {d['severity']}")
print(f"  dup:      {d['duplicate_of']}   known issue: {d['known_issue']}")
print(f"  why:      {d['rationale']}")
print("  timing:   " + " · ".join(f"{t['tier']} {t['elapsed_ms']:.0f} ms" for t in r["trace"]))
