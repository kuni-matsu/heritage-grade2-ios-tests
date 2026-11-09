#!/usr/bin/env python3
"""Use an iOS 18.5 iPhone simulator compatible with Xcode 16.4.

Avoid selecting an iOS 26 simulator when both generations are installed.
Only a simulator UUID is printed to stdout; diagnostics go to stderr.
"""
import json
import subprocess
import sys

TARGET_RUNTIME = "com.apple.CoreSimulator.SimRuntime.iOS-18-5"
PREFERRED_NAMES = ("iPhone 16 Pro", "iPhone 16", "iPhone 16e", "iPhone SE (3rd generation)")


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def choice(data):
    """Return ('existing', udid, name) or ('create', type_identifier, name)."""
    runtimes = [
        r for r in data.get("runtimes", [])
        if r.get("identifier") == TARGET_RUNTIME and r.get("isAvailable", False)
    ]
    if not runtimes:
        raise ValueError("Xcode 16.4 requires the available iOS 18.5 simulator runtime")

    def rank(name):
        return PREFERRED_NAMES.index(name) if name in PREFERRED_NAMES else len(PREFERRED_NAMES)

    devices = [
        d for d in data.get("devices", {}).get(TARGET_RUNTIME, [])
        if d.get("isAvailable", False)
        and d.get("udid")
        and d.get("name", "").startswith("iPhone")
    ]
    if devices:
        devices.sort(key=lambda d: (rank(d["name"]), d.get("state") != "Booted"))
        selected = devices[0]
        return ("existing", selected["udid"], selected["name"])

    types = [
        t for t in data.get("devicetypes", [])
        if t.get("identifier") and t.get("name", "").startswith("iPhone")
    ]
    if not types:
        raise ValueError("No iPhone simulator device type is installed")
    types.sort(key=lambda t: rank(t["name"]))
    selected = types[0]
    return ("create", selected["identifier"], selected["name"])


def main():
    data = json.loads(run("xcrun", "simctl", "list", "-j").stdout)
    try:
        action, identifier, name = choice(data)
    except ValueError as error:
        print(error, file=sys.stderr)
        print("Installed runtimes:", data.get("runtimes", []), file=sys.stderr)
        sys.exit(2)
    if action == "existing":
        print(f"Selected iOS 18.5 device: {name}", file=sys.stderr)
        print(identifier)
    else:
        print(f"Creating iOS 18.5 device: {name}", file=sys.stderr)
        created = run("xcrun", "simctl", "create", "SyntheticGrade2CI",
                      identifier, TARGET_RUNTIME)
        print(created.stdout.strip())


if __name__ == "__main__":
    main()
