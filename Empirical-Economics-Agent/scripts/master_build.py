"""Readiness checker for the empirical research pipeline.

This script is intentionally conservative:
- it discovers the repository root from its own location,
- creates a timestamped log under results/logs,
- reports whether data and project scripts exist,
- never executes analysis scripts or claims reproducibility.

Use --strict in CI to return nonzero while required artifacts are missing.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import json
import os

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_ROOT / "results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_SLUG = os.environ.get("PROJECT_SLUG", "a-share-multifactor-pricing")


def stage_snapshot() -> dict[str, list[str]]:
    stages = {
        "clean": REPO_ROOT / "code" / "clean",
        "build": REPO_ROOT / "code" / "build",
        f"analysis_{PROJECT_SLUG}": REPO_ROOT / "code" / "analysis" / PROJECT_SLUG,
        f"output_{PROJECT_SLUG}": REPO_ROOT / "code" / "output" / PROJECT_SLUG,
    }
    snapshot: dict[str, list[str]] = {}
    for name, path in stages.items():
        if not path.exists():
            snapshot[name] = ["<missing directory>"]
            continue
        files = sorted(
            str(p.relative_to(path))
            for p in path.rglob("*")
            if p.is_file() and not p.name.startswith(".") and p.name != "README.md"
        )
        snapshot[name] = files or ["<empty>"]
    return snapshot


def readiness(snapshot: dict[str, list[str]]) -> tuple[str, list[str]]:
    final_dir = REPO_ROOT / "data" / "final"
    data_files = sorted(
        str(path.relative_to(REPO_ROOT))
        for path in final_dir.glob("*")
        if path.suffix.lower() in {".dta", ".parquet", ".csv"}
    )
    blockers: list[str] = []
    if not data_files:
        blockers.append("data/final/ 中没有分析样本")
    if not (final_dir / "schema.yaml").exists():
        blockers.append("data/final/schema.yaml 不存在")
    if snapshot[f"analysis_{PROJECT_SLUG}"] == ["<empty>"]:
        blockers.append(f"code/analysis/{PROJECT_SLUG}/ 中没有分析脚本")
    if snapshot[f"output_{PROJECT_SLUG}"] == ["<empty>"]:
        blockers.append(f"code/output/{PROJECT_SLUG}/ 中没有输出脚本")
    return ("blocked" if blockers else "ready_for_pipeline_wiring"), blockers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查项目流水线是否具备数据、schema、分析脚本和输出脚本；不执行分析。"
    )
    parser.add_argument("--strict", action="store_true", help="存在 blocker 时返回退出码 1")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_path = LOG_DIR / f"master_build_py_{timestamp}.json"
    snapshot = stage_snapshot()
    status, blockers = readiness(snapshot)
    payload = {
        "timestamp": timestamp,
        "repo_root": str(REPO_ROOT),
        "project_slug": PROJECT_SLUG,
        "status": status,
        "message": (
            "Readiness check only. No clean/build/analysis/output script was executed."
        ),
        "blockers": blockers,
        "stages": snapshot,
    }
    log_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[master_build.py] repo root: {REPO_ROOT}")
    print(f"[master_build.py] wrote readiness log: {log_path}")
    for stage_name, files in payload["stages"].items():
        print(f"  - {stage_name}: {', '.join(files)}")
    if blockers:
        print("[BLOCKED]")
        for blocker in blockers:
            print(f"  - {blocker}")
    else:
        print("[READY] 可以开始接入实际调度；本脚本仍不会执行分析。")
    return 1 if args.strict and blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
