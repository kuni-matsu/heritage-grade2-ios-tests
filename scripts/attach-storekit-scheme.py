#!/usr/bin/env python3
"""Attach the synthetic StoreKit catalog to XcodeGen's generated shared scheme."""
from pathlib import Path
import xml.etree.ElementTree as ET

scheme = Path("Grade2SyntheticHost.xcodeproj/xcshareddata/xcschemes/SyntheticHost.xcscheme")
assert scheme.exists(), f"Generated shared scheme missing: {scheme}"
tree = ET.parse(scheme)
root = tree.getroot()
for action_name in ("LaunchAction", "TestAction"):
    action = root.find(action_name)
    assert action is not None, f"XcodeGen scheme has no {action_name}"
    for element in list(action):
        if element.tag == "StoreKitConfigurationFileReference":
            action.remove(element)
    ET.SubElement(action, "StoreKitConfigurationFileReference", {
        "identifier": "container:StoreKitSandbox.storekit"
    })
tree.write(scheme, encoding="UTF-8", xml_declaration=True)
assert "container:StoreKitSandbox.storekit" in scheme.read_text()
print("StoreKit configuration attached to Xcode shared scheme")
