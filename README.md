<!-- SVENKUNKKA-README-NAV:BEGIN -->
[English overview](#project-overview-en) · [中文项目说明](#project-overview-zh) · [Maintainer on X / 维护者 X](https://x.com/Svenu1s5)
<!-- SVENKUNKKA-README-NAV:END -->

# Firmware Reverse Engineer Skill

An open Codex Skill for evidence-backed analysis of legally obtained MCU firmware and clean-room, behaviorally equivalent reimplementation.

The minimum input is intentionally small:

```text
firmware.bin
MCU: nRF52840-QIAA
```

The Skill guides an agent from deterministic binary triage through memory-map recovery, disassembly, peripheral recognition, call/data-flow reconstruction, state machines, protocol and algorithm analysis, targeted validation, and a testable clean-room implementation.

## What it does

- Starts with a raw `.bin` and an exact MCU part number
- Distinguishes facts, inferences, hypotheses, and unknowns
- Tracks addresses, confidence, evidence, tools, and reproducibility
- Recovers hardware interfaces, timing, state machines, protocols, and algorithms
- Produces a structured analysis workspace and clean-room reimplementation plan
- Continues into development mode from the recovered behavioral model

It does **not** promise restoration of original source code, symbols, comments, or project structure.

## Safety and public-release scope

This repository is for firmware the user owns or is authorized to analyze, including interoperability, compatibility, repair, archival, and defensive research. It intentionally excludes instructions for bypassing readout protection, secure boot, debug locks, flash encryption, authentication, or other access controls. It also excludes credential extraction, malicious payload development, and redistribution of proprietary firmware or decompiled vendor code.

See [SECURITY.md](SECURITY.md) and the authorization section in [SKILL.md](SKILL.md).

## Repository structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── triage_firmware.py
├── references/
│   ├── evidence-model.md
│   └── output-contract.md
├── examples/
│   ├── basic-analysis.md
│   └── firmware-diff.md
├── SECURITY.md
├── LICENSE
└── README.md
```

## Install

Use the Codex skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo SvenKunkka/firmware-reverse-engineering-skill \
  --path . \
  --name firmware-reverse-engineer
```

The default installation directory is `~/.codex/skills/firmware-reverse-engineer`.

Manual installation is also possible:

```bash
git clone https://github.com/SvenKunkka/firmware-reverse-engineering-skill.git \
  ~/.codex/skills/firmware-reverse-engineer
```

The Skill becomes available to new Codex turns after installation.

## Use

Attach the authorized firmware and prompt:

```text
Use $firmware-reverse-engineer to analyze this firmware.
MCU: nRF52840-QIAA
```

For an authorized version comparison:

```text
Use $firmware-reverse-engineer to compare firmware_v1.bin and firmware_v2.bin.
MCU: STM32F411CEU6
Focus on algorithm, constants, timing, and protocol changes.
```

The bundled triage utility can also be run directly:

```bash
python3 scripts/triage_firmware.py firmware.bin \
  --mcu "nRF52840-QIAA" \
  --output 00_input_report.json
```

It uses only the Python standard library and never modifies the input binary.

## Optional tools

The Skill can use whatever is legitimately available in the environment, including Ghidra, binwalk, Capstone, radare2, Graphviz, vendor CMSIS/SVD data, and licensed commercial analysis tools. Missing optional tools must be reported; results must never be fabricated.

## License

MIT. The license covers this Skill and its helper script, not any third-party firmware analyzed with it.


---

<!-- SVENKUNKKA-PROJECT-INFO:BEGIN -->

<a id="project-overview-zh"></a>
## 中文项目说明

面向合法取得 MCU 固件的 Codex Skill，从二进制初筛、内存映射、外设和状态机分析推进到协议理解、定向验证与洁净室重实现，明确区分事实、推断和未知。

**使用入口：** 将仓库安装为 `firmware-reverse-engineer` 技能，提供固件与准确 MCU 型号后调用；也可独立运行 `python3 scripts/triage_firmware.py`，参数见 README。

**范围说明：** 不承诺恢复原始源码、符号或注释；不包含绕过读保护、安全启动、调试锁和认证的流程，分析与发布范围须符合授权。

<a id="project-overview-en"></a>
## English project overview

A Codex Skill for legally obtained MCU firmware, progressing from binary triage, memory maps, peripheral and state-machine analysis to protocol understanding, targeted validation and clean-room reimplementation, distinguishing facts, inferences and unknowns.

**Getting started:** Install the repository as the `firmware-reverse-engineer` skill and provide firmware plus the exact MCU part number. The `python3 scripts/triage_firmware.py` utility also runs independently; see the README for arguments.

**Scope:** It does not promise original source, symbol or comment recovery. It excludes procedures for bypassing readout protection, secure boot, debug locks and authentication; analysis and publication must remain within authorization.

**仓库维护者 / Repository maintainer:** [SvenKunkka](https://github.com/SvenKunkka) · [X / Twitter](https://x.com/Svenu1s5)

<!-- SVENKUNKKA-PROJECT-INFO:END -->
