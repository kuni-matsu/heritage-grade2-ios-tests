#!/usr/bin/env python3
"""Select (or create) an available iOS simulator on the GitHub macOS runner.

Only a simulator UUID is printed to stdout; diagnostics go to stderr.
"""
import json
import re
import subprocess
import sys


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def version(value):
    return tuple(int(s) for s in re.findall(r"\\d+", value))


data = json.loads(run("xcrun", "simctl", "list", "-j").stdout)
devices = []
for runtime_id, entries in data.get("devices", {}).items():
    if ".SimRuntime.iOS-" not in runtime_id:
        continue
    for d in entries:
        if d.get("isAvailable", False) and "iPhone" in d.get("name", ""):
            devices.append(d)
if devices:
    devices.sort(key=lambda d: (d.get("name") == "iPhone 17 Pro", d.get("state") == "Booted"), reverse=True)
    print(f"Found available device: {devices[0]['name']}", file=sys.stderr)
    print(devices[0]["udid"])
    sys.exit(0)

runtimes = [
    r for r in data.get("runtimes", [])
    if r.get("isAvailable", False)
    and (r.get("identifier", "").startswith("com.apple.CoreSimulator.SimRuntime.iOS-"))
]
if not runtimes:
    print("No available iOS simulator devices or runtimes on this macOS runner.", file=sys.stderr)
    print("Available runtime data:", data.get("runtimes", []), file=sys.stderr)
    sys.exit(2)
runtime = max(runtimes, key=lambda r: version(r.get("identifier", "")))
types = [
    t for t in data.get("devicetypes", [])
    if "iPhone" in t.get("name", "") and t.get("identifier")
]
if not types:
    print("No iPhone simulator device types installed.", file=sys.stderr)
    sys.exit(3)
types.sort(key=lambda t: (t.get("name") == "iPhone 17 Pro", t.get("name") == "iPhone 17"), reverse=True)
device_type = types[0]
print(f"Creating {device_type['name']} with {runtime['identifier']}", file=sys.stderr)
created = run(
    "xcrun", "simctl", "create", "SyntheticGrade2CI",
    device_type["identifier"], runtime["identifier"]
)
print(created.stdout.strip())
