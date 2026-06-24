# Runtime Directory

这个目录只保留可迁移的轻量配置。

可提交：

- `path_aliases.json`：跨平台路径别名。
- `README.md`：本说明。

不要提交：

- `last_context_bootstrap.json`
- `llm_routes.json`
- `commands/command_ledger.jsonl`
- `cleanup/*.json`

这些都是本机运行状态、模型路由或清理收据，已经在 `.gitignore` 中排除。
