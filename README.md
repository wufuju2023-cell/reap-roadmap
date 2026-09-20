# reap-roadmap

REAP / AlphaProof 研究导航（公开版，单文件离线 HTML）。

- `index.html` — 公开版导航页：**不含任何私有路径**，全部链接均为云端资源
  （GitHub / HuggingFace / arXiv）。内容包含：
  - 两大模块（项目 / 预备知识与支线）、文件级深链（点进具体文件而不是仓库根）；
  - **整体学习顺序 S0→S7**（每阶段目标 + 按序阅读链接 + 完成标志）；
  - **开发顺序 M0→M8**（做什么 + 代码落点 + 必读上下文）；
  - **模块 → 上下文速查表**；
  - 快速路径 8 条、GitHub / HF / 论文总表。
  窄屏或浏览器放大后，点左上角「☰ 目录」展开侧栏。
- `roadmap_data.py` + `gen_roadmap.py` — 生成器：
  - `python3 gen_roadmap.py --variant=public index.html`（公开版，本页）
  - `python3 gen_roadmap.py roadmap.html`（含私有路径的完整版，仅本地使用）
