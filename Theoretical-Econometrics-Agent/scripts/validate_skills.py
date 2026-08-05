#!/usr/bin/env python3
"""校验 .cursor/skills/ 下所有 SKILL.md 的 frontmatter 与本地链接。

用法：
    python scripts/validate_skills.py            # 校验全部 skill
    python scripts/validate_skills.py --skill-dir .cursor/skills/m1-model-specification
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith('---'):
        raise ValueError('SKILL.md 必须以 --- 分隔的 YAML frontmatter 开头')
    parts = text.split('---', 2)
    if len(parts) < 3:
        raise ValueError('frontmatter 缺少结尾的 ---')
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip().strip('"\'')
    return meta


def find_local_links(text: str) -> list[str]:
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)
    out = []
    for link in links:
        link = link.split('#', 1)[0]
        if not link or '://' in link or link.startswith('mailto:'):
            continue
        out.append(link)
    return out


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return [f'{skill_md} 不存在']

    text = skill_md.read_text(encoding='utf-8')
    try:
        meta = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    for field in ('name', 'description'):
        if not meta.get(field):
            errors.append(f'缺少必填 frontmatter 字段：{field}')

    name = meta.get('name', '')
    if name != skill_dir.name:
        errors.append(f'frontmatter name "{name}" 必须与目录名 "{skill_dir.name}" 一致')
    if not re.fullmatch(r'[a-z0-9-]{1,64}', name):
        errors.append('skill 名只允许小写字母、数字和连字符，最长 64 字符')

    for link in find_local_links(text):
        target = (skill_dir / link) if link.startswith('.') else (REPO_ROOT / link)
        if not target.resolve().exists():
            errors.append(f'本地链接失效：{link}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--skill-dir', help='只校验指定 skill 目录（默认校验 .cursor/skills 下全部）')
    args = parser.parse_args()

    if args.skill_dir:
        dirs = [Path(args.skill_dir).resolve()]
    else:
        skills_root = REPO_ROOT / '.cursor' / 'skills'
        dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())

    failed = False
    for d in dirs:
        errors = validate_skill(d)
        if errors:
            failed = True
            print(f'[FAIL] {d.name}')
            for e in errors:
                print(f'  - {e}')
        else:
            print(f'[OK]   {d.name}')

    if failed:
        return 1
    print('全部 skill 校验通过。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
