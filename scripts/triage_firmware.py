#!/usr/bin/env python3
"""Non-destructive, dependency-free triage for an authorized firmware image."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import sys
from collections import Counter
from pathlib import Path


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in Counter(data).values())


def trailing_run(data: bytes, value: int) -> int:
    count = 0
    for byte in reversed(data):
        if byte != value:
            break
        count += 1
    return count


def arm_vector_hint(data: bytes) -> dict[str, object]:
    if len(data) < 8:
        return {"available": False, "reason": "fewer than 8 bytes"}

    initial_sp, reset_vector = struct.unpack_from("<II", data, 0)
    stack_like = 0x10000000 <= initial_sp < 0x40000000 and initial_sp % 4 == 0
    thumb_like = bool(reset_vector & 1)
    target = reset_vector & ~1
    target_in_image_if_base_zero = target < len(data)

    return {
        "available": True,
        "initial_sp_hex": f"0x{initial_sp:08x}",
        "reset_vector_hex": f"0x{reset_vector:08x}",
        "reset_target_hex": f"0x{target:08x}",
        "stack_pointer_looks_sram_like": stack_like,
        "reset_vector_has_thumb_bit": thumb_like,
        "reset_target_in_image_if_base_zero": target_in_image_if_base_zero,
        "classification": "candidate_only",
    }


def build_report(path: Path, mcu: str | None) -> dict[str, object]:
    data = path.read_bytes()
    size = len(data)
    zeros = data.count(0)
    ffs = data.count(0xFF)

    return {
        "schema_version": 1,
        "input": {
            "filename": path.name,
            "size": size,
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "mcu": {"user_supplied_part": mcu, "verification_status": "not_verified"},
        "statistics": {
            "shannon_entropy_bits_per_byte": round(shannon_entropy(data), 6),
            "zero_byte_ratio": round(zeros / size, 6) if size else 0.0,
            "ff_byte_ratio": round(ffs / size, 6) if size else 0.0,
            "trailing_zero_bytes": trailing_run(data, 0),
            "trailing_ff_bytes": trailing_run(data, 0xFF),
        },
        "vector_hints": {"arm_cortex_m_at_offset_zero": arm_vector_hint(data)},
        "limitations": [
            "Vector-table output is a heuristic candidate, not proof of architecture or load address.",
            "Entropy alone cannot prove compression or encryption.",
            "This report does not disassemble code or identify embedded filesystems.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("firmware", type=Path, help="Path to the authorized firmware image")
    parser.add_argument("--mcu", help="Exact MCU part number supplied by the user")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.firmware.is_file():
        print(f"error: firmware file not found: {args.firmware}", file=sys.stderr)
        return 2

    report = build_report(args.firmware, args.mcu)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
