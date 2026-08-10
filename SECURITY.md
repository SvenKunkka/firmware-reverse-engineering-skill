# Security and responsible-use policy

Use this Skill only on firmware you own, created, or are authorized to analyze, or for a legitimate interoperability, compatibility, repair, archival, or defensive-security purpose.

## Supported scope

- Static analysis of a lawfully obtained binary
- Documentation of observable behavior and interfaces
- Defensive review of unsafe patterns
- Non-destructive validation on an authorized, unlocked device
- Clean-room reimplementation based on documented behavior

## Out of scope

- Bypassing readout protection, secure boot, debug locks, flash encryption, authentication, or access controls
- Extracting or publishing secrets, credentials, personal data, or proprietary firmware
- Malware, persistence, covert access, destructive payloads, or unauthorized surveillance
- Republishing substantial decompiled vendor code

If analysis reveals a likely secret, record only its type, location, and evidence; redact the value and recommend rotation. Report vulnerabilities responsibly to the affected vendor or maintainer.

To report a vulnerability in this repository itself, open a private GitHub security advisory for the repository. Do not include third-party firmware or secrets in a public issue.
