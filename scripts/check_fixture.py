#!/usr/bin/env python3
"""Check a synthetic fixture only. No private repository access or real questions."""
from pathlib import Path
import json
root = Path(__file__).resolve().parents[1]
fixture = json.loads((root / "fixtures" / "synthetic-questions.json").read_text(encoding="utf-8"))
assert len(fixture) == 4
assert {x["category"] for x in fixture} == {"制度", "日本", "世界", "時事"}
assert all(len(x["choices"]) == 4 and 0 <= x["answer"] < 4 for x in fixture)
assert all(x["synthetic"] is True for x in fixture)
print("PASS: synthetic public fixture only; no real question-bank data")
