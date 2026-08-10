# Example: authorized firmware comparison

## User request

```text
Use $firmware-reverse-engineer to compare firmware_v1.bin and firmware_v2.bin.
MCU: STM32F411CEU6

Both files are our internal releases. Identify changes in timing, constants, protocol handling, and the input-filter algorithm. Then propose regression tests for a clean-room implementation.
```

## Expected agent behavior

- Hash and map both inputs independently.
- Confirm comparable image regions before interpreting byte-level differences.
- Separate code movement from behavioral changes.
- Map changed functions, constants, tables, and protocol fields to evidence IDs.
- Explain algorithm changes at the behavioral or mathematical level.
- Create regression tests from documented input/output behavior rather than copied decompiler code.
- Preserve uncertainties and request one targeted validation only if it materially changes the conclusion.
