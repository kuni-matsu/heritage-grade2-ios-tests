#!/usr/bin/env python3
"""Validate only the public synthetic StoreKit fixture, never production assets."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config = json.loads((root / "StoreKitSandbox.storekit").read_text(encoding="utf-8"))
products = config["products"]
assert len(products) == 1
p = products[0]
assert p["productID"] == "jp.heritagemaster.grade2.fullaccess"
assert p["type"] == "NonConsumable"
assert str(p["displayPrice"]) == "700"
assert p["referenceName"] == "Synthetic Grade 2 Unlock"
print("PASS: public synthetic StoreKit product contract")
