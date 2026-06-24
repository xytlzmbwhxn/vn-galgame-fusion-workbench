# Full Script Corpus

这里提供完整 VN 剧本研究的公开模板。

公开仓库只保留：

- `corpus_manifest.example.json`
- 可公开的方法说明
- 可复用的指标字段和分析入口

使用真实完整剧本前，必须确认来源合法、授权边界清楚，并把分析结果压缩成可复用方法、节奏指标或风格画像。生成时不得复制原文对白或叙述。

推荐流程：

```powershell
py .\00_workbench_core\tools\analyze_full_script_corpus.py --manifest .\01_reference_log\full_script_corpus\corpus_manifest.example.json --out-dir .\01_reference_log\full_script_corpus
```

如果没有合法语料，就不要声称已经做过具体作品级语料校准；回退到公开方法卡和公开风格资产。
