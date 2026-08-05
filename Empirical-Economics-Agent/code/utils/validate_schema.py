"""
脚本名称：utils_validate_schema.py
用途说明：验证 data/final/ 中的 .dta/.parquet/.csv 是否符合 schema.yaml
输入文件：data/final/schema.yaml + 最终样本文件
输出文件：无（stdout 报告 + 非零退出码表示验证失败）
方法来源：自建，使用 pandas；读取 parquet 需要 pyarrow 或 fastparquet
作者：    日期：2026-05-29
"""

import sys
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).parents[2]


def validate_schema(df: pd.DataFrame, schema: dict) -> list[str]:
    """验证 DataFrame 是否符合 schema 定义。返回错误信息列表。"""
    errors: list[str] = []
    variables = schema.get("variables", {})

    for var_name, spec in variables.items():
        # 检查变量存在
        if spec.get("required", False) and var_name not in df.columns:
            errors.append(f"缺失必需变量: {var_name}")
            continue

        if var_name not in df.columns:
            continue  # 非必需变量不存在就算了

        col = df[var_name]

        # 检查类型
        expected_type = spec.get("type", "")
        if expected_type == "int":
            if not pd.api.types.is_integer_dtype(col):
                errors.append(f"{var_name}: 期望 int，实际 {col.dtype}")
        elif expected_type == "float":
            if not pd.api.types.is_numeric_dtype(col):
                errors.append(f"{var_name}: 期望 numeric，实际 {col.dtype}")
        elif expected_type == "datetime":
            if not pd.api.types.is_datetime64_any_dtype(col):
                errors.append(f"{var_name}: 期望 datetime，实际 {col.dtype}")

        # 检查缺失率
        max_missing = spec.get("max_missing", 1.0)
        missing_rate = col.isna().mean()
        if missing_rate > max_missing:
            errors.append(
                f"{var_name}: 缺失率 {missing_rate:.2%} 超过上限 {max_missing:.2%}"
            )

        # 检查数值范围
        if "range" in spec and pd.api.types.is_numeric_dtype(col):
            lo, hi = spec["range"]
            valid = col.dropna()
            if not valid.between(lo, hi).all():
                outliers = valid[~valid.between(lo, hi)]
                errors.append(
                    f"{var_name}: {len(outliers)} 个值超出范围 [{lo}, {hi}]"
                )

    # 检查唯一键
    unique_key = schema.get("unique_key", [])
    if unique_key:
        all_cols = [c for c in unique_key if c in df.columns]
        if len(all_cols) == len(unique_key):
            dup_count = df.duplicated(all_cols).sum()
            if dup_count > 0:
                errors.append(f"唯一键 {unique_key} 有 {dup_count} 行重复")

    return errors


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_schema.py <data_file.(dta|parquet|csv)> [schema.yaml]")
        sys.exit(1)

    data_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        PROJECT_ROOT / "data" / "final" / "schema.yaml"
    )

    if not data_path.exists():
        print(f"错误：数据文件不存在: {data_path}")
        sys.exit(1)

    if not schema_path.exists():
        print(f"错误：schema 文件不存在: {schema_path}")
        print("请先根据 data/final/codebook.md 创建 schema.yaml")
        sys.exit(1)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    print(f"加载数据: {data_path}")
    if data_path.suffix == ".dta":
        df = pd.read_stata(data_path)
    elif data_path.suffix == ".parquet":
        df = pd.read_parquet(data_path)
    elif data_path.suffix == ".csv":
        df = pd.read_csv(data_path)
    else:
        print(f"不支持的文件格式: {data_path.suffix}")
        sys.exit(1)

    print(f"数据维度: {df.shape[0]:,} 行 × {df.shape[1]} 列")
    print(f"Schema 变量数: {len(schema.get('variables', {}))}")

    errors = validate_schema(df, schema)

    if errors:
        print(f"\n验证失败 ({len(errors)} 项错误):")
        for e in errors:
            print(f"  ❌ {e}")
        sys.exit(1)

    print("\n验证通过 ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
