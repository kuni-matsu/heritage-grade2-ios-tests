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
The initial workflows check GitHub-hosted Ubuntu/macOS runner availability and validate the synthetic fixture. **They do not yet compile the actual iPhone app or verify a real StoreKit purchase.** Passing here cannot certify the private iOS build.

## Run locally on Windows
```powershell
py -3 scripts/check_fixture.py
```
