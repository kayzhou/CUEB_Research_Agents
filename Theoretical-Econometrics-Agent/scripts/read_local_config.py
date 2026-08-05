#!/usr/bin/env python3
"""Read one value from config/local-tools.json for activation scripts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "local-tools.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("key")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()

    path = Path(args.config).expanduser()
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    value = data.get(args.key, "")
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise TypeError(f"{args.key} must be a string")
    print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
