#!/usr/bin/env python3
"""Linux regression tests for selecting the Xcode 16.4-compatible simulator."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "select_simulator", Path(__file__).resolve().parent / "select-simulator.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
RUNTIME = module.TARGET_RUNTIME


class SimulatorChoiceTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "runtimes": [
                {"identifier": RUNTIME, "isAvailable": True},
                {"identifier": "com.apple.CoreSimulator.SimRuntime.iOS-26-0",
                 "isAvailable": True},
            ],
            "devices": {
                RUNTIME: [
                    {"name": "iPhone 16", "isAvailable": True,
                     "state": "Shutdown", "udid": "ios18-iphone16"},
                    {"name": "iPhone 16 Pro", "isAvailable": True,
                     "state": "Shutdown", "udid": "ios18-iphone16pro"},
                ],
                "com.apple.CoreSimulator.SimRuntime.iOS-26-0": [
                    {"name": "iPhone 17 Pro", "isAvailable": True,
                     "state": "Booted", "udid": "ios26-iphone17pro"},
                ],
            },
            "devicetypes": [
                {"name": "iPhone 16 Pro",
                 "identifier": "com.apple.CoreSimulator.SimDeviceType.iPhone-16-Pro"}
            ],
        }

    def test_prefers_compatible_ios_18_over_booted_ios_26(self):
        self.assertEqual(module.choice(self.data),
                         ("existing", "ios18-iphone16pro", "iPhone 16 Pro"))

    def test_creates_compatible_device_if_needed(self):
        self.data["devices"][RUNTIME] = []
        self.assertEqual(
            module.choice(self.data),
            ("create", "com.apple.CoreSimulator.SimDeviceType.iPhone-16-Pro",
             "iPhone 16 Pro"),
        )

    def test_reports_missing_ios_18_runtime(self):
        self.data["runtimes"][0]["isAvailable"] = False
        with self.assertRaisesRegex(ValueError, "iOS 18.5"):
            module.choice(self.data)


if __name__ == "__main__":
    unittest.main()
