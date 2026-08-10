# Output contract

Create only the files supported by current evidence. Empty placeholder reports are less useful than explicit `PARTIAL` or `BLOCKED` entries in the manifest.

## Analysis workspace

```text
reverse_engineering/
├── README.md
├── manifest.json
├── executive_summary.md
├── 00_input_report.json
├── mcu_profile.md
├── memory_map.md
├── firmware_map.md
├── functions.csv
├── variables.csv
├── callgraph.md
├── callgraph.dot
├── dataflow.md
├── state_machines.md
├── constants.md
├── timing_model.md
├── peripherals.md
├── protocols.md
├── algorithms.md
├── evidence.md
├── unknowns.md
├── tool_logs/
├── disassembly/
└── reimplementation/
    ├── README.md
    ├── docs/
    │   ├── architecture.md
    │   ├── behavioral_requirements.md
    │   ├── interfaces.md
    │   └── traceability.md
    ├── include/
    ├── src/
    └── tests/
```

## Manifest

Track at minimum:

```json
{
  "schema_version": 1,
  "input": {
    "filename": "firmware.bin",
    "sha256": "...",
    "size": 0
  },
  "mcu": {
    "user_supplied_part": "EXACT-PART-NUMBER",
    "profile_status": "verified|partial|blocked"
  },
  "tools": [],
  "status": {
    "verified": [],
    "partial": [],
    "blocked": [],
    "next": ""
  }
}
```

Use only observed tool versions and actual hashes. Never invent a successful run.

## Executive summary

Answer these questions first:

1. What does the firmware appear to do?
2. Which architectures, peripherals, protocols, and schedulers are evidenced?
3. Which core algorithms have reached L3 or L4?
4. What remains unknown or contradictory?
5. Is clean-room implementation currently feasible, and which parts are safe to implement?
6. What single next action would reduce uncertainty most?

## Function map

Recommended CSV columns:

```text
address,generated_name,semantic_name,category,size,callers,callees,confidence,evidence_ids,status
```

## Unknowns

Each unknown must contain a stable ID, question, current evidence, alternatives, confidence, impact, and the safest highest-value verification method. Close unknowns by linking the new evidence; do not delete their history.

## Clean-room traceability

Map each behavioral requirement and test to evidence IDs. Keep copied decompiler output outside the implementation tree. Do not place the input firmware or proprietary extracted artifacts in source control.
