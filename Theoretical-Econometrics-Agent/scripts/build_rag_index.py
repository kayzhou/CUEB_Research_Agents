#!/usr/bin/env python3
"""Build a lightweight local literature index.

This script intentionally avoids external dependencies. It indexes .txt, .md, .tex, .bib, and .csv files.
For PDFs, first convert them to text with your preferred PDF tool and place the .txt file beside the PDF.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r'[A-Za-z][A-Za-z0-9_-]{2,}')
SUPPORTED = {'.txt', '.md', '.tex', '.bib', '.csv'}


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', required=True, help='Literature library folder')
    parser.add_argument('--out', required=True, help='Output index folder')
    args = parser.parse_args()

    library = Path(args.library).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not library.exists():
        print(f'ERROR: library folder not found: {library}')
        return 1

    jsonl_path = out / 'rag_index.jsonl'
    catalog_path = out / 'rag_catalog.csv'

    rows = []
    with jsonl_path.open('w', encoding='utf-8') as jf:
        for path in sorted(library.rglob('*')):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED:
                continue
            text = path.read_text(encoding='utf-8', errors='ignore')
            tokens = tokenize(text)
            counts = Counter(tokens)
            top_terms = [w for w, _ in counts.most_common(30)]
            rec = {
                'path': str(path.relative_to(library)),
                'sha16': file_hash(path),
                'n_chars': len(text),
                'n_tokens': len(tokens),
                'top_terms': top_terms,
                'preview': text[:500].replace('\n', ' '),
            }
            jf.write(json.dumps(rec, ensure_ascii=False) + '\n')
            rows.append(rec)

    with catalog_path.open('w', encoding='utf-8', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=['path', 'sha16', 'n_chars', 'n_tokens', 'top_terms', 'preview'])
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row['top_terms'] = ';'.join(row['top_terms'])
            writer.writerow(row)

    print(f'Indexed {len(rows)} files.')
    print(f'Wrote {jsonl_path}')
    print(f'Wrote {catalog_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

