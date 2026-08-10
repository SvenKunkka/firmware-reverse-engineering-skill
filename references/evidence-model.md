# Evidence model

Use this model for every material reverse-engineering claim.

## Evidence classes

| Class | Meaning | Example |
|---|---|---|
| FACT | Direct observation reproducible from a named artifact or trace | A little-endian word at offset 4 is `0x00012591` |
| INFERENCE | Best explanation supported by multiple facts | The word is probably a Thumb reset vector |
| HYPOTHESIS | Plausible explanation with a named discriminating test | A function may implement temperature compensation |
| UNKNOWN | Evidence is insufficient or contradictory | Whether a table is factory or runtime calibration |

## Confidence bands

| Score | Label | Minimum expectation |
|---:|---|---|
| 95-100 | Confirmed | Reproduced by independent evidence or runtime observation |
| 80-94 | High confidence | Multiple consistent static facts and no strong contradiction |
| 60-79 | Probable | A leading explanation with meaningful gaps |
| 40-59 | Possible | Some supporting facts, but credible alternatives remain |
| 0-39 | Speculative | Weak pattern match or early idea only |

Do not use numerical precision to imply certainty. Explain why the score belongs in its band.

## Evidence record

Use stable identifiers such as `E-001`, `F-014`, `A-003`, and `U-007`.

```yaml
id: F-014
claim: Function at 0x00018420 reads ADC channel 3.
class: INFERENCE
confidence: 88
artifacts:
  - disassembly/function_00018420.txt
evidence:
  - writes channel value 3 to the documented ADC selector register
  - waits for the documented conversion-ready event
  - returns a 12-bit masked value
alternatives:
  - could be a vendor wrapper shared by multiple analog sources
how_to_verify:
  - correlate normal key movement with an authorized trace at the returned buffer
status: open
```

## Validation selection

Prefer the test with the highest expected information gain and the lowest risk, cost, and invasiveness. Request one test at a time. A good validation plan states:

1. the exact unknown or competing hypotheses
2. what to observe
3. the normal user action to perform
4. outcomes that would distinguish the hypotheses
5. safety precautions and required authorization

Do not request a dynamic test when static evidence is already sufficient for the user's decision.

## Contradictions

Never discard contradictory evidence silently. Add it to the record, lower confidence, and explain whether it suggests a wrong load address, mixed code/data, a wrapper function, multiple runtime modes, or an incorrect MCU profile.
