# config — 本机工具路径配置

本目录只存放可共享的配置模板与字段约束。本机绝对路径写入
`config/local-tools.json`；该文件已被 `.gitignore` 排除，不得提交或跨机器复用。

## 生成配置

在仓库根目录执行：

```bash
python scripts/configure_local.py
```

脚本优先使用显式参数，其余字段从项目 `.venv`、系统 `PATH` 与常见安装位置探测。
已有配置不会被覆盖；确认覆盖时加 `--force`。

也可复制 `local-tools.example.json` 为 `local-tools.json` 后手工填写。字段约束见
`local-tools.schema.json`。Windows、macOS 与 Linux 示例及激活方式见
`ENVIRONMENT.md` 和根目录 `本地化部署说明.md`。
