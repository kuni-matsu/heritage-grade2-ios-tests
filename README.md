# Heritage Grade 2 — Public iOS CI Sandbox

This is a **public, synthetic-only** test repository. It is intentionally separate from the private application repository.

## What is safe to publish here
- Synthetic questions (not copied or paraphrased from the paid 800-question bank)
- Generic StoreKit configuration and isolated test scaffolding
- CI workflows that never check out the private application repository

## What must stay private
- The real 800-question bank and production app assets
- Credentials, API keys, certificates, provisioning profiles and secrets
- The full private repository or its Git history

## Verification scope
The workflows validate synthetic fixtures on Linux, and build and run a **synthetic iOS test host** on an iPhone simulator on macOS. The iOS test checks local StoreKit non-consumable product lookup (¥700), a verified purchase, and a fresh read of the resulting entitlement. Results must be checked in GitHub Actions; the existence of a test does not imply it has passed. The test does **not** prove App Store sandbox sign-in, the app's actual restore button, or the private 800-question production app build. Passing here cannot certify the private iOS build.

## Run locally on Windows
```powershell
py -3 scripts/check_fixture.py
```
