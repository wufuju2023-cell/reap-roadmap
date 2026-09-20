# reap-roadmap

REAP / AlphaProof 研究导航（公开版，单文件离线 HTML）。

- `index.html` — 公开版导航页：**不含任何本机路径**，全部链接均为云端资源
  （GitHub / HuggingFace / arXiv）。窄屏或浏览器放大后，点左上角「☰ 目录」展开侧栏。
- `roadmap_data.py` + `gen_roadmap.py` — 生成器：
  - `python3 gen_roadmap.py --variant=public index.html`（公开版，本页）
  - `python3 gen_roadmap.py roadmap.html`（含私有路径的完整版，仅本地使用）

覆盖内容：AlphaProof（Nature 2025 + 官方伪代码 + Nexus 2026）、nanoproof、REAP、
V1（REAL-Prover 7B + 价值头）、V1-1 agentic-tool、V2（实验性）、GitHub / HuggingFace
总表；预备知识含 Lean 源码学习、MCTS+RL 笔记、13 个主题资料与
[Jev × AlphaProof 分析](https://github.com/wufuju2023-cell/jev-alpha-proof-analysis)。
