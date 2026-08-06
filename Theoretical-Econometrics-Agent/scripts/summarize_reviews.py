#!/usr/bin/env python3
"""Summarize reviewer reports from Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviews', required=True, help='Review folder')
    args = parser.parse_args()
    folder = Path(args.reviews)
    if not folder.exists():
        print(f'ERROR: folder not found: {folder}')
        return 1

    for path in sorted(folder.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        score = re.search(r'Score:\s*([^\n]+)', text)
        rec = re.search(r'Recommendation:\s*([^\n]+)', text)
        print(f'## {path.name}')
        print(f'- Score: {score.group(1).strip() if score else "N/A"}')
        print(f'- Recommendation: {rec.group(1).strip() if rec else "N/A"}')
        majors = re.findall(r'## Major concerns\n(.*?)(?:\n## |\Z)', text, flags=re.S)
        if majors:
            lines = [ln.strip() for ln in majors[0].splitlines() if ln.strip()]
            for ln in lines[:5]:
                print(f'- {ln}')
        print()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

