#!/usr/bin/env python3
"""Attach local StoreKit file to Xcode's Run and Test actions using a verified path.

StoreKitConfigurationFileReference resolves relative to the .xcscheme's directory.
XcodeGen's default prefix does not necessarily resolve to the desired location.
"""
import os
from pathlib import Path
import xml.etree.ElementTree as ET

scheme = Path("Grade2SyntheticHost.xcodeproj/xcshareddata/xcschemes/SyntheticHost.xcscheme")
catalog = Path("StoreKitSandbox.storekit")
assert scheme.is_file(), f"Generated Xcode shared scheme missing: {scheme}"
assert catalog.is_file(), f"Synthetic StoreKit configuration missing: {catalog}"

identifier = os.path.relpath(catalog.resolve(), scheme.parent.resolve()).replace(os.sep, "/")
assert not identifier.startswith("/") and identifier.endswith("/StoreKitSandbox.storekit"), identifier
assert (scheme.parent / identifier).resolve() == catalog.resolve(), "StoreKit path does not resolve"

tree = ET.parse(scheme)
root = tree.getroot()
launch = root.find("LaunchAction")
test = root.find("TestAction")
assert launch is not None, "Generated scheme has no LaunchAction"
assert test is not None, "Generated scheme has no TestAction"
generated_reference = launch.find("StoreKitConfigurationFileReference")
assert generated_reference is not None, "XcodeGen failed to attach the StoreKit configuration"
assert generated_reference.attrib.get("identifier", "").endswith("StoreKitSandbox.storekit"), (
    "Generated scheme points to a different StoreKit file"
)

for action in (launch, test):
    for element in list(action):
        if element.tag == "StoreKitConfigurationFileReference":
            action.remove(element)
    ET.SubElement(action, "StoreKitConfigurationFileReference", {"identifier": identifier})

tree.write(scheme, encoding="UTF-8", xml_declaration=True)
verified = ET.parse(scheme).getroot()
for name in ("LaunchAction", "TestAction"):
    action = verified.find(name)
    reference = action.find("StoreKitConfigurationFileReference")
    assert reference is not None and reference.attrib.get("identifier") == identifier
    assert (scheme.parent / identifier).resolve().is_file()
print(f"Verified StoreKit file reference for both run and test: {identifier}")
