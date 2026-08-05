#!/usr/bin/env python3
"""从 templates/paper-project 模板初始化一个理论计量论文工作区。

用法：
    python scripts/init_project.py --name spatial-break-qml --output projects
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / 'templates' / 'paper-project'
LATEX_GENERATED_PATTERNS = (
    '*.acn',
    '*.acr',
    '*.alg',
    '*.aux',
    '*.bbl',
    '*.bcf',
    '*.blg',
    '*.dvi',
    '*.fdb_latexmk',
    '*.fls',
    '*.glg',
    '*.glo',
    '*.gls',
    '*.idx',
    '*.ilg',
    '*.ind',
    '*.ist',
    '*.lof',
    '*.log',
    '*.lot',
    '*.maf',
    '*.mtc*',
    '*.nav',
    '*.out',
    '*.ps',
    '*.run.xml',
    '*.snm',
    '*.synctex*',
    '*.toc',
    '*.vrb',
    '*.xdv',
    '*.pdf',
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True, help='项目 slug（小写英文 kebab-case，如 spatial-break-qml）')
    parser.add_argument('--output', default='projects', help='输出父目录（默认 projects/）')
    parser.add_argument('--force', action='store_true', help='已存在时覆盖')
    args = parser.parse_args()

    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', args.name):
        print(f'ERROR: 项目名必须是小写英文 kebab-case，收到："{args.name}"')
        return 1

    if not TEMPLATE.exists():
        print(f'ERROR: 模板不存在：{TEMPLATE}')
        return 1

    out_parent = Path(args.output).expanduser()
    if not out_parent.is_absolute():
        out_parent = REPO_ROOT / out_parent
    out_dir = out_parent.resolve() / args.name
    if out_dir.exists():
        if not args.force:
            print(f'ERROR: 目录已存在：{out_dir}。使用 --force 覆盖。')
            return 1
        shutil.rmtree(out_dir)

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        TEMPLATE,
        out_dir,
        ignore=shutil.ignore_patterns(*LATEX_GENERATED_PATTERNS),
    )
    try:
        shown = out_dir.relative_to(REPO_ROOT)
    except ValueError:
        shown = out_dir
    print(f'已初始化论文工作区：{out_dir}')
    print('下一步：')
    print(f'  1. 编辑 {shown}/config/model_specification.yaml')
    print(f'  2. 把核心文献放入 {shown}/literature/library/')
    print('  3. 在 system/metadata.md 登记项目 slug 与当前模块')
    return 0


if __name__ == '__main__':
    sys.exit(main())
