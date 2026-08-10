---
name: firmware-reverse-engineer
description: Analyze legally obtained MCU firmware binaries, especially raw .bin images, to recover memory layout, functions, peripherals, data flow, state machines, protocols, and algorithms; produce evidence-backed documentation and clean-room, behaviorally equivalent reimplementations. Use when the user provides firmware plus an exact MCU model, requests embedded-firmware reverse engineering, compares authorized firmware versions, or continues development from an existing reverse-engineering workspace.
---

# Firmware Reverse Engineer

Analyze authorized MCU firmware without claiming to recover the original source. Build an auditable behavioral model, then use that model for clean-room reimplementation and further development.

## Required input

Start when both inputs are available:

1. A firmware binary, normally `.bin`
2. The exact MCU part number, such as `nRF52840-QIAA`

Treat PCB photos, schematics, datasheets, product names, captures, logs, debug traces, and additional firmware versions as optional evidence. Do not require the user to supply a flash base, compiler, SDK, RTOS, bootloader, or source tree before beginning; infer them when evidence permits and record uncertainty when it does not.

## Authorization and safety boundary

Proceed only with firmware the user owns, created, or is authorized to analyze, or with a clearly legitimate interoperability, compatibility, repair, archival, or security-research purpose.

- Analyze a binary already supplied by the user.
- Do not provide procedures to bypass readout protection, secure boot, debug locks, flash encryption, authentication, or access controls.
- Do not develop malware, persistence, credential theft, covert access, or destructive payloads.
- Do not expose discovered credentials, private keys, tokens, or personal data. Record their location and type, redact the value, and recommend rotation.
- Do not redistribute proprietary firmware, large decompiled excerpts, or copyrighted vendor code.
- Keep clean-room reimplementation separate from decompiler output. Recreate documented behavior and interfaces, not the vendor's code expression.
- If the request crosses these boundaries, stop that part and continue with safe static analysis, documentation, interoperability, or defensive remediation.

## Working principles

Maintain four evidence classes throughout the project:

- `FACT`: directly observed and reproducible
- `INFERENCE`: best explanation supported by multiple facts
- `HYPOTHESIS`: plausible but requires a named test
- `UNKNOWN`: not currently supportable

Semantic function and variable names are reconstructed labels, never asserted original names. Attach an address, confidence, and evidence to every important label.

Use these confidence bands:

- `95-100 Confirmed`
- `80-94 High confidence`
- `60-79 Probable`
- `40-59 Possible`
- `0-39 Speculative`

Read [references/evidence-model.md](references/evidence-model.md) before assigning confidence or planning validation. Read [references/output-contract.md](references/output-contract.md) before creating or updating the case workspace.

## Workflow

### 1. Create or resume the case workspace

Use a dedicated output directory. Preserve prior evidence and continue from its manifest when present. Never overwrite the input binary.

Record:

- input filename, byte size, SHA-256, and analysis timestamp
- exact MCU model as supplied by the user
- tool names and versions actually used
- authorization context stated by the user
- missing tools and blocked stages

Copy neither the binary nor decompiler output into a public repository unless the user explicitly confirms redistribution rights.

### 2. Perform deterministic triage

Run:

```bash
python3 scripts/triage_firmware.py firmware.bin --mcu "EXACT-PART-NUMBER" --output 00_input_report.json
```

Also use available local inspection tools such as `file`, `xxd`, `strings`, and `binwalk`. Detect file size, entropy, padding, magic bytes, container signatures, possible compression or encryption, multiple images, vector-table candidates, and embedded filesystems.

Do not treat a tool signature as proof. Save command output and classify each conclusion using the evidence model.

### 3. Build the MCU profile

Prefer the manufacturer's datasheet, reference manual, CMSIS/SVD files, linker scripts, and vendor SDK headers. Record citations or local source paths.

Capture at minimum:

- CPU architecture, instruction set, endianness, and exception model
- flash and RAM ranges
- vector-table layout and interrupt count
- peripheral address map
- boot configuration and debug interface
- GPIO, ADC, timers, DMA, serial buses, USB, radio, and power registers that exist on this part

Do not borrow register maps or memory sizes from a similar MCU without labeling the mapping as a hypothesis.

### 4. Determine image layout and load address

Generate multiple base-address candidates when needed. Test them against:

- initial stack pointer range
- reset-vector alignment and instruction-set state
- interrupt targets within executable regions
- absolute references into known flash, RAM, and peripheral ranges
- branch validity, literal pools, strings, and relocation-like patterns
- known bootloader or application offsets

Choose a base only when it explains the evidence better than alternatives. Preserve rejected candidates and reasons in `memory_map.md`.

### 5. Disassemble and cross-check

Prefer a reproducible headless workflow when Ghidra is available. Cross-check critical conclusions with another engine such as Capstone, radare2, Binary Ninja, or IDA when available and properly licensed.

Separate code, data, vector tables, literal pools, jump tables, lookup tables, configuration, calibration, and padding. Record tool configuration, processor language, base address, and analysis options.

Never fabricate results from unavailable tools. Mark a stage `BLOCKED` or `PARTIAL` and continue with available evidence.

### 6. Recover semantics from the bottom up

Create stable address-based IDs before semantic renaming. Map:

1. interrupt handlers and startup code
2. memory-mapped peripheral accesses
3. HAL-like primitives and drivers
4. middleware, schedulers, protocols, and power management
5. application state machines and core algorithms

For every renamed function record original address, generated name, semantic name, callers, callees, category, confidence, and evidence. For variables and inferred structures, record address or base, size, access sites, proposed type, and confidence.

### 7. Reconstruct data flow and algorithms

Prioritize end-to-end flows such as:

```text
physical input -> raw sample -> filtering -> calibration -> normalization
-> state or control algorithm -> protocol/HID output
```

For every core algorithm document:

- inputs and outputs
- persistent state
- constants, thresholds, lookup tables, and units
- sampling and update rates
- filters, formulas, boundary conditions, and error handling
- state transitions and timing conditions
- evidence for each claim and the highest-value next validation

Rate recovery maturity:

- `L0 Unknown`: function exists but behavior is unclear
- `L1 Structural`: inputs, outputs, and call relationships are known
- `L2 Behavioral`: broad behavior is explainable
- `L3 Mathematical`: formulas, thresholds, tables, or state machine are recovered
- `L4 Reimplementable`: an independent implementation can be specified and tested

Do not promote an algorithm to L4 without testable inputs, outputs, edge cases, and a validation plan.

### 8. Recover protocols and timing

Identify report descriptors, packet framing, commands, lengths, checksums, sequence fields, responses, retry behavior, timeouts, and error paths. Cover only protocols visible in the authorized artifact or captures.

Build a timing model from clocks, timer reloads, scheduler ticks, counters, interrupt rates, and captured traces. Distinguish configured maximum rates from observed runtime rates.

### 9. Request targeted dynamic evidence only when needed

If static analysis cannot resolve a high-value unknown, request one minimally sufficient, non-destructive test. Examples include a logic-analyzer capture of an already accessible SPI bus, a USB/BLE capture from normal product use, or an authorized watchpoint on an unlocked development device.

Specify:

- the exact unknown being tested
- signals or addresses to observe
- user action to perform
- expected distinguishing outcomes
- electrical and data-handling precautions

Do not suggest fault injection, protection bypass, invasive extraction, or unsafe probing as a default or fallback.

### 10. Produce a clean-room reimplementation

After the behavioral contract is sufficiently mature, create a separate `reimplementation/` tree. Use readable, modular, testable, hardware-independent code. Implement reconstructed interfaces and behavior from the evidence documents; do not mechanically translate decompiler output.

Include unit tests for known vectors and edge cases, hardware abstraction seams, traceability from requirements to evidence IDs, and explicit stubs for unknown behavior. Mark any implementation based on a hypothesis and keep it disabled or isolated until validated.

### 11. Continue in development mode

For later requests, load the case manifest, evidence register, architecture, data flow, state machines, algorithms, protocols, and unknowns before editing code. Treat the recovered model as the design baseline. Update evidence and tests whenever behavior changes.

## Deliverable status

End every run with separate status groups:

- `VERIFIED`: reproduced from current artifacts
- `PARTIAL`: useful result with named gaps
- `BLOCKED`: unavailable tool, missing evidence, encrypted/compressed content, or authorization boundary
- `NEXT`: the single highest-value next action

Never report a full recovery merely because decompilation succeeded. Never report runtime behavior as verified without runtime evidence.

## Resources

- `scripts/triage_firmware.py`: dependency-free, non-destructive binary triage
- `references/evidence-model.md`: evidence, confidence, and validation rules
- `references/output-contract.md`: standard analysis and reimplementation structure
- `examples/basic-analysis.md`: minimal invocation and expected workflow
- `examples/firmware-diff.md`: authorized two-version comparison example
