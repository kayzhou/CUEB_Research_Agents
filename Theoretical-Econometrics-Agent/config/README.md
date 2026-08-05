# config — 本机工具路径配置

本目录只管理框架级本机路径，不存放论文模型配置。
论文的 `model_specification.yaml` 与 `simulation_design.yaml` 位于 `projects/{slug}/config/`。

## 使用

```bash
python scripts/configure_local.py
```

或复制 `local-tools.example.json` 为 `local-tools.json` 后手工填写绝对路径。
字段约束见 `local-tools.schema.json`，完整分平台示例见根目录 `使用手册.md`。

`local-tools.json` 已被 `.gitignore` 忽略：它只属于当前电脑，不应提交、打包给别人或跨机器复用。
