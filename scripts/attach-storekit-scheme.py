#!/usr/bin/env python3
"""Verify XcodeGen StoreKit scheme path and attach it to XCTest as well."""
from pathlib import Path
import xml.etree.ElementTree as ET

scheme = Path("Grade2SyntheticHost.xcodeproj/xcshareddata/xcschemes/SyntheticHost.xcscheme")
assert scheme.is_file(), f"Shared scheme missing: {scheme}"
tree = ET.parse(scheme)
root = tree.getroot()
launch = root.find("LaunchAction")
assert launch is not None, "Generated scheme has no LaunchAction"
source = launch.find("StoreKitConfigurationFileReference")
assert source is not None, "XcodeGen did not generate the StoreKit run configuration"
identifier = source.attrib.get("identifier", "")
assert identifier == "../../StoreKitSandbox.storekit", (
    f"Unexpected StoreKit scheme reference: {identifier!r}"
)
test = root.find("TestAction")
assert test is not None, "Generated scheme has no TestAction"
for element in list(test):
    if element.tag == "StoreKitConfigurationFileReference":
        test.remove(element)
ET.SubElement(test, "StoreKitConfigurationFileReference", {"identifier": identifier})
tree.write(scheme, encoding="UTF-8", xml_declaration=True)
print(f"StoreKit scheme reference active for run and test: {identifier}")
