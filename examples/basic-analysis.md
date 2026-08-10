# Example: basic authorized analysis

## User request

```text
Use $firmware-reverse-engineer to analyze the attached firmware.bin.
MCU: nRF52840-QIAA

I own this development firmware. Focus on the sensor-to-HID data flow and tell me whether the core algorithm is reimplementable.
```

## Expected agent behavior

1. Hash and triage the binary without modifying it.
2. Build the exact MCU profile from authoritative documentation.
3. test load-address and vector-table candidates.
4. Recover peripheral access, functions, call graph, and the sensor-to-HID data flow.
5. Grade each algorithm from L0 to L4 with evidence IDs.
6. Create a clean-room specification and tests only for behavior supported by evidence.
7. Return `VERIFIED`, `PARTIAL`, `BLOCKED`, and one `NEXT` action.

The agent must not claim to have restored original source code or fabricate output from tools that were unavailable.
