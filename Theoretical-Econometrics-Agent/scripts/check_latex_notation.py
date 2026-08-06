#!/usr/bin/env python3
"""Lightweight LaTeX notation and label checks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_tex_tree(main_tex: Path) -> str:
    """Read main.tex and recursively follow input/include directives."""
    root = main_tex.parent.resolve()
    pattern = re.compile(r'\\(?:input|include)\{([^}]+)\}')
    visited: set[Path] = set()
    chunks: list[str] = []

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in visited:
            return
        visited.add(path)
        text = path.read_text(encoding='utf-8')
        chunks.append(text)
        for rel in pattern.findall(text):
            rel_path = Path(rel if rel.endswith('.tex') else rel + '.tex')
            candidates = (path.parent / rel_path, root / rel_path)
            child = next((candidate for candidate in candidates if candidate.exists()), None)
            if child is not None:
                visit(child)

    visit(main_tex)
    return '\n'.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--tex', required=True, help='Path to main.tex')
    args = parser.parse_args()
    main_tex = Path(args.tex)

    if not main_tex.exists():
        print(f'ERROR: not found: {main_tex}')
        return 1

    text = read_tex_tree(main_tex)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:ref|eqref|autoref|cref)\{([^}]+)\}', text)
    dup_labels = sorted({x for x in labels if labels.count(x) > 1})
    missing_refs = sorted(set(refs) - set(labels))

    print(f'Labels: {len(labels)}')
    print(f'References: {len(refs)}')

    if dup_labels:
        print('Duplicate labels:')
        for x in dup_labels:
            print(f'- {x}')

    if missing_refs:
        print('Missing referenced labels:')
        for x in missing_refs:
            print(f'- {x}')

    key_symbols = {
        'W_N': r'W_N',
        'tau_0': r'\\tau_0|\\tau_\{0\}',
        'widehat tau': r'\\widehat\s*\{?\s*\\tau|\\hat\s*\{?\s*\\tau',
        'theta_0': r'\\theta_0|\\theta_\{0\}',
        'widehat theta': r'\\widehat\s*\{?\s*\\theta|\\hat\s*\{?\s*\\theta',
    }
    for name, pattern in key_symbols.items():
        if not re.search(pattern, text):
            print(f'WARNING: expected symbol pattern not found: {name}')

    if dup_labels or missing_refs:
        return 1
    print('LaTeX label check passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

