"""
脚本名称：utils/validate_claims.py
用途说明：验证 system/claim-registry.json 中声明-证据链接的完整性
输入文件：system/claim-registry.json
输出文件：打印验证报告到 stdout
方法来源：V3.0 声明-证据注册表协议
关键决策：检查核心 claim 是否有证据、证据路径是否存在、状态是否合理
作者：V3.0 模板  日期：2026-06-07
"""

import json
import os
import sys
from pathlib import Path

# Windows 控制台编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_registry():
    path = PROJECT_ROOT / "system" / "claim-registry.json"
    if not path.exists():
        print("[!] claim-registry.json not found, skipping.")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(registry):
    claims = registry.get("claims", [])
    if not claims:
        return [], ["claim registry 为空；M4 起草前至少登记核心 claim"], []

    errors = []
    warnings = []
    core_claims = [c for c in claims if c.get("risk_level") in ("高", "中")]

    for c in claims:
        cid = c.get("id", "?")

        # 检查状态合法性
        valid_statuses = {
            "unsupported", "theoretical", "empirical_pending",
            "empirically_supported", "fragile", "refuted"
        }
        if c.get("status") not in valid_statuses:
            errors.append(f"{cid}: 无效状态 '{c.get('status')}'")

        # 检查证据链接
        if c.get("status") in ("empirical_pending", "empirically_supported"):
            evidence = c.get("evidence", [])
            if not evidence:
                errors.append(f"{cid}: 状态为 {c['status']} 但无 evidence 链接")
            for ev in evidence:
                ev_path = ev.get("path", "")
                if ev_path:
                    abs_path = PROJECT_ROOT / ev_path
                    if not abs_path.exists():
                        warnings.append(f"{cid}: evidence 路径不存在: {ev_path}")

        # 检查首选规格指针
        preferred = c.get("preferred_evidence_id")
        if preferred and c.get("status") == "empirically_supported":
            evidence_ids = [e.get("exp_id") for e in c.get("evidence", [])]
            if preferred not in evidence_ids:
                warnings.append(f"{cid}: preferred_evidence_id '{preferred}' 不在 evidence 列表中")

    return errors, warnings, core_claims


def main():
    registry = load_registry()
    if registry is None:
        return

    errors, warnings, core_claims = validate(registry)
    n_errors, n_warnings = len(errors), len(warnings)

    claims = registry.get("claims", [])
    print(f"声明-证据验证报告")
    print(f"==================")
    print(f"总 claim 数: {len(claims)}")
    print(f"核心 claim 数（中/高风险）: {len(core_claims)}")
    print(f"错误: {n_errors}  警告: {n_warnings}")

    if n_errors == 0 and n_warnings == 0:
        print("✅ 全部通过")
    else:
        print()
        for e in errors:
            print(f"  ❌ {e}")
        for w in warnings:
            print(f"  ⚠ {w}")

    sys.exit(0 if n_errors == 0 else 1)


if __name__ == "__main__":
    main()
