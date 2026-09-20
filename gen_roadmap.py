# -*- coding: utf-8 -*-
"""Generate the single-file offline navigation roadmap (roadmap.html)."""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from roadmap_data import META, NOTES, QUICK, MODULES, GUIDES  # noqa: E402


def load_exists():
    out = {}
    for name in ("exists_wsl.json", "exists_remote.json"):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                out.update(json.load(f))
    return out


EXISTS = load_exists()

VARIANT = "full"  # "full" | "gh"

GH_RULES = [
    ("/home/zhai/project/reap/alpha-proof-original-math-version.wsl-backup",
     "https://github.com/wufuju2023-cell/alpha-proof-original-math-version", "main", False),
    ("/home/zhai/project/reap/reap-source-code-explain",
     "https://github.com/wufuju2023-cell/reap-source-code-explain", "main", False),
    ("/home/zhai/project/reap/new-update-model",
     "https://github.com/wufuju2023-cell/reap-new-update-model", "master", False),
    ("/home/zhai/project/reap", None, None, True),
    ("/home/zhai/project/gap-advance-plan-of-nano-proof-v1-m1",
     "https://github.com/wufuju2023-cell/gap-advance-plan-of-nano-proof-v1-m1", "main", False),
    ("/home/zhai/project/alphaproof-nexus-results",
     "https://github.com/google-deepmind/alphaproof-nexus-results", "main", False),
    ("/home/zhai/project/alphaproof-official-materials",
     "https://github.com/wufuju2023-cell/alphaproof-official-materials", "main", False),
    ("/home/zhai/project/Lean-source-code-learning-to-know-reap",
     "https://github.com/wufuju2023-cell/Lean-source-code-learning-to-know-reap", "main", False),
    ("/home/zhai/project/formal-imo",
     "https://github.com/google-deepmind/formal-imo", "main", True),
    ("/home/zhai/project/miniF2F",
     "https://github.com/google-deepmind/miniF2F", "master", True),
    ("/home/zhai/project/environment-spec",
     "https://github.com/wufuju2023-cell/reap-new-update-model", "master", False),
]


def gh_url(path):
    """Map a WSL path to a GitHub URL. Returns (url, short_label) or (None, None)."""
    for prefix, repo, branch, root_only in GH_RULES:
        if path == prefix or path.startswith(prefix + "/"):
            if repo is None:
                return None, None
            rel = path[len(prefix):].lstrip("/")
            if root_only or not rel:
                return repo, repo.split("/")[-1]
            kind = "blob" if "." in rel.split("/")[-1] else "tree"
            short = "/".join(rel.split("/")[-2:])
            return f"{repo}/{kind}/{branch}/{rel}", short
    return None, None


REMOTE_GH_RULES = [
    ("/mnt/gloway/projects/reap-new-update-model-value-head", None, None, True),
    ("/mnt/gloway/projects/reap-new-update-model/nanoproof",
     "https://github.com/kripner/nanoproof", "main", True),
    ("/mnt/gloway/projects/reap-new-update-model-master",
     "https://github.com/wufuju2023-cell/reap-new-update-model", "master", False),
    ("/mnt/gloway/projects/reap-new-update-model",
     "https://github.com/wufuju2023-cell/reap-new-update-model", "master", False),
    ("/mnt/gloway/projects/reap-publicize-work",
     "https://github.com/wufuju2023-cell/reap-rsi-public", "master", False),
    ("/mnt/gloway/projects/reap-rsi-public",
     "https://github.com/wufuju2023-cell/reap-rsi-public", "master", False),
    ("/mnt/gloway/projects/reap-agentic-v1-1",
     "https://github.com/wufuju2023-cell/reap-agentic-v1-1", "main", False),
    ("/mnt/gloway/projects/v1-1-agentic-tool",
     "https://github.com/wufuju2023-cell/v1-1-agentic-tool", "main", False),
    ("/mnt/gloway/projects/9-14-project-my-new-linux",
     "https://github.com/wufuju2023-cell/9-14-project-my-new-linux", "main", False),
    ("/mnt/gloway/projects/lean-corpus/mathlib4",
     "https://github.com/leanprover-community/mathlib4", "master", True),
    ("/home/a/文档/mcts-theory-learning",
     "https://github.com/wufuju2023-cell/mcts-theory-learning", "main", False),
    ("/home/a/文档/hsy-alphaproof-public",
     "https://github.com/hsy221329/hsy-alphaproof-public", "main", False),
    ("/mnt/gloway/projects/reap-gap-advance-alpha-proof",
     "https://github.com/wufuju2023-cell/reap-gap-advance-alpha-proof", "main", False),
    ("/mnt/gloway/projects/multi-agent-rl-alpha-proof",
     "https://github.com/wufuju2023-cell/multi-agent-rl-alpha-proof", "main", False),
]

MLT_REPO = "https://github.com/wufuju2023-cell/ml-theory-reference"
TOPIC_NAMES = [
    "Transformer数学理论参考资料", "ttt-参考资料", "样本效率理论参考资料",
    "信息几何理论参考资料", "RLVR-OPSD-参考资料", "残差连接理论参考资料",
    "贝叶斯概率与机器学习参考资料", "随机微分方程与机器学习参考资料",
    "高维概率论参考资料", "扩散模型数学理论参考资料", "LoRA微调数学理论参考资料",
    "RNN-LSTM数学理论参考资料", "元学习参考资料",
]


JEV_REPO = "https://github.com/wufuju2023-cell/jev-alpha-proof-analysis"


def gh_url_remote(path):
    if path.startswith("/home/a/文档/jev-and-open-rebuilt"):
        rest = path[len("/home/a/文档/jev-and-open-rebuilt"):].lstrip("/")
        if not rest:
            return f"{JEV_REPO}/tree/main", "jev-alpha-proof-analysis"
        tail = rest if rest.startswith("alpha-proof") else "jev/" + rest
        kind = "blob" if "." in tail.split("/")[-1] else "tree"
        return f"{JEV_REPO}/{kind}/main/{tail}", "/".join(tail.split("/")[-2:])
    if path.startswith("/home/a/文档/"):
        rel = path[len("/home/a/文档/"):]
        top = rel.split("/")[0]
        if top in TOPIC_NAMES:
            sub = rel[len(top):].lstrip("/")
            tail = "topics/" + top + (("/" + sub) if sub else "")
            if sub and "." in sub.split("/")[-1]:
                return f"{MLT_REPO}/blob/main/{tail}", sub
            return f"{MLT_REPO}/tree/main/{tail}", tail
    for prefix, repo, branch, root_only in REMOTE_GH_RULES:
        if path == prefix or path.startswith(prefix + "/"):
            if repo is None:
                return None, None
            rel = path[len(prefix):].lstrip("/")
            if root_only or not rel:
                return repo, repo.split("/")[-1]
            if rel == "app/VALUE_HEAD.md":
                return f"{repo}/tree/{branch}/app", "app/"
            kind = "blob" if "." in rel.split("/")[-1] else "tree"
            short = "/".join(rel.split("/")[-2:])
            return f"{repo}/{kind}/{branch}/{rel}", short
    return None, None


def gh_any(m, p):
    return gh_url(p) if m == "wsl" else gh_url_remote(p)


def key(m, p):
    return m + "|" + p


def ex_state(m, p):
    return EXISTS.get(key(m, p), None)  # True / False / None


TAG_CLASS = {
    "核心": "t-core", "主线": "t-main", "优先": "t-core", "实验性": "t-exp",
    "官方": "t-off", "上游": "t-off", "源头": "t-off", "参考": "t-ref",
    "远程": "t-remote", "私有": "t-priv", "代码": "t-code", "模型": "t-model",
    "环境": "t-env", "评测": "t-eval", "计划": "t-plan", "设计": "t-plan",
    "规格": "t-plan", "分析": "t-ref", "预备": "t-prep", "2026": "t-off",
    "Agent": "t-off", "fork": "t-off", "公开镜像": "t-pub", "实验": "t-exp",
    "工作区": "t-code", "基础设施": "t-env", "论文": "t-model",
}

M_BADGE = {"wsl": "WSL", "remote": "F/E 远程"}


def e(s):
    return html.escape(str(s), quote=True)



def hu(url):
    return str(url).replace(" ", "%20")


MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def md(s):
    s = str(s)
    out, pos = [], 0
    for m in MD_LINK.finditer(s):
        out.append(e(s[pos:m.start()]))
        out.append(f'<a href="{e(hu(m.group(2)))}" target="_blank" rel="noopener">{e(m.group(1))}</a>')
        pos = m.end()
    out.append(e(s[pos:]))
    return "".join(out)


def chip(m, p):
    if VARIANT == "public":
        url, short = gh_any(m, p)
        if not url:
            return ""
        return (f'<a class="lbtn l-github ghpath" href="{e(hu(url))}" target="_blank" '
                f'rel="noopener" title="{e(url)}">GitHub · {e(short)}</a>')
    if VARIANT == "gh" and m == "wsl":
        url, short = gh_url(p)
        if not url:
            return ""
        return (f'<a class="lbtn l-github ghpath" href="{e(hu(url))}" target="_blank" '
                f'rel="noopener" title="{e(p)}">GitHub · {e(short)}</a>')
    st = ex_state(m, p)
    cls = "pchip"
    mark = ""
    if st is False:
        cls += " miss"
        mark = '<span class="warn" title="路径当前不存在">⚠</span>'
    elif st is None:
        cls += " unknown"
    return (f'<span class="{cls}" data-m="{m}" data-p="{e(p)}" '
            f'title="{e(p)}">{mark}<span class="mb">{M_BADGE[m]}</span>'
            f'<span class="pt">{e(p)}</span>'
            f'<button class="cp" type="button">复制</button></span>')


def qlink(m, p, label):
    if VARIANT in ("gh", "public"):
        if VARIANT == "public":
            url, _ = gh_any(m, p)
        else:
            url, _ = gh_url(p) if m == "wsl" else (None, None)
        if not url:
            return ""
        return (f'<a class="qlink ghlink" href="{e(hu(url))}" target="_blank" '
                f'rel="noopener" title="{e(url)}">{e(label)}</a>')
    st = ex_state(m, p)
    cls = "qlink" + (" miss" if st is False else "")
    return f'<span class="{cls}" data-m="{m}" data-p="{e(p)}">{e(label)}</span>'


def link_btn(l):
    kind, url, label = l
    return f'<a class="lbtn l-{e(kind)}" href="{e(hu(url))}" target="_blank" rel="noopener">{e(label)}</a>'


PUBLIC_TAG_MAP = {"远程": "云端"}


def render_card(c):
    tag_items = []
    for t in c["tags"]:
        label = PUBLIC_TAG_MAP.get(t, t) if VARIANT == "public" else t
        tag_items.append(f'<span class="tag {TAG_CLASS.get(t, "t-ref")}">{e(label)}</span>')
    tags = "".join(tag_items)
    if VARIANT == "public":
        kept = [(m, p) for m, p in c["paths"] if gh_any(m, p)[0]]
        dropped = len(c["paths"]) - len(kept)
    else:
        kept, dropped = list(c["paths"]), 0
    paths = "".join(chip(m, p) for m, p in kept)
    lks = c["links"]
    if VARIANT == "public":
        lks = [l for l in lks if "私有" not in l[2]]
    links = "".join(link_btn(l) for l in lks)
    quick = ""
    if c["quick"]:
        items = "".join(qlink(m, p, lbl) for lbl, m, p in c["quick"])
        quick = f'<div class="quick"><span class="ql-t">入口</span>{items}</div>'
    reads = f'<div class="reads">读法：{e(c["reads"])}</div>' if c["reads"] else ""
    lead = f'<div class="lead">{e(c["lead"])}</div>' if c.get("lead") else ""
    muted = (f'<div class="muted">（{dropped} 项未公开材料已省略）</div>'
             if dropped else "")
    if VARIANT == "public":
        search = " ".join([c["title"], c["desc"], c.get("lead", "")] + [q[0] for q in c["quick"]])
    else:
        search = " ".join([c["title"], c["desc"], c.get("lead", "")] + [p for _, p in kept] + [q[0] for q in c["quick"]])
    return (f'<div class="card" id="{e(c["id"])}" data-s="{e(search.lower())}">'
            f'<div class="ch"><span class="ct">{e(c["title"])}</span>{tags}</div>'
            f'<div class="cd">{e(c["desc"])}</div>{lead}{reads}'
            f'<div class="paths">{paths}</div>{muted}{quick}'
            f'<div class="links">{links}</div></div>')


def plain(s):
    return MD_LINK.sub(r"\1", str(s))


def render_table(t):
    head = "".join(f"<th>{e(c)}</th>" for c in t["cols"])
    rows = ""
    for r in t["rows"]:
        tds = "".join(f"<td>{md(v)}</td>" for v in r)
        search = " ".join(plain(v) for v in r)
        rows += f'<tr data-s="{e(search.lower())}">{tds}</tr>'
    return (f'<div class="tablewrap" id="{e(t["id"])}"><div class="tcap">{md(t["title"])}</div>'
            f'<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')


def render_items(items):
    out = []
    for it in items:
        if isinstance(it, dict) and it.get("type") == "table":
            out.append(render_table(it))
        else:
            out.append(render_card(it))
    return "\n".join(out)


SHORT = {
    "c_dossier": "分析档案", "c_reap_source": "源码精读", "c_nano_analysis": "nano 分析",
    "c_reap_gap": "REAP 差距", "c_v1_spec": "V1 规格", "c_v1_result": "实验记录",
    "c_v1_value_head": "价值头", "c_914_plan": "9-14 计划", "c_agentic_repo": "V1-1 仓库",
    "c_v2_spec": "V2 规格", "c_v2_code": "V2 代码",
}


def quick_section():
    rows = ""
    for title, how, refs in QUICK:
        jumps = " ".join(f'<a class="jump" href="#{r}">↗ {SHORT.get(r, r)}</a>' for r in refs)
        rows += f'<tr><td class="qk">{e(title)}</td><td>{e(how)}</td><td>{jumps}</td></tr>'
    return (f'<div class="tablewrap" id="quick"><div class="tcap">我该读哪个？—— {len(QUICK)} 条主线路径</div>'
            f'<table class="qtab"><thead><tr><th>场景</th><th>顺序</th><th>直达</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def guides_section():
    out = ['<section id="guides"><h3>学习顺序 · 开发顺序 · 模块上下文</h3><div class="guides">']
    for t in GUIDES:
        out.append(render_table(t))
    out.append("</div></section>")
    return "\n".join(out)


ACTIVE_MODULES = MODULES
ACTIVE_NOTES = NOTES


def notes_section():
    out = ['<div class="notes">']
    for t, body in [(n[0], n[1]) for n in ACTIVE_NOTES]:
        out.append(f'<div class="note"><span class="nt">{e(t)}</span>{e(body)}</div>')
    out.append("</div>")
    return "\n".join(out)


def toc():
    out = ['<nav id="toc"><div class="toc-t">目录</div>']
    out.append('<a class="toc-l toc-top" href="#quick">我该读哪个？</a>')
    out.append('<a class="toc-l toc-top" href="#guides">学习 / 开发 / 上下文</a>')
    for mod in ACTIVE_MODULES:
        out.append(f'<div class="toc-m">{e(mod["title"])}</div>')
        for part in mod["parts"]:
            out.append(f'<a class="toc-l" href="#{part["id"]}">{e(part["title"])}</a>')
    out.append('<a class="toc-l toc-top" href="#gh-hf">GitHub / HF 总表</a>')
    out.append("</nav>")
    return "\n".join(out)


CSS = """
:root{--bg:#f7f8fa;--fg:#1c2026;--mut:#5b636e;--line:#e3e6ea;--card:#fff;--acc:#0b6bcb;--warn:#c62828;--ok:#1b7f3b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.65 -apple-system,'Segoe UI',Roboto,'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{background:#fff;border-bottom:1px solid var(--line);padding:14px 20px 10px;position:sticky;top:0;z-index:20}
h1{font-size:19px;margin:0 0 2px}.sub{color:var(--mut);font-size:12.5px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.modebtn{border:1px solid var(--line);background:#fff;border-radius:6px;padding:4px 10px;font-size:12.5px;cursor:pointer}
.modebtn.on{background:var(--acc);border-color:var(--acc);color:#fff}
#q{flex:1;min-width:200px;max-width:340px;border:1px solid var(--line);border-radius:6px;padding:5px 9px;font-size:13px}
#cnt{color:var(--mut);font-size:12px}
.wrap{display:flex;gap:20px;max-width:1280px;margin:0 auto;padding:16px 20px 60px}
nav#toc{width:250px;flex:0 0 250px;position:sticky;top:96px;align-self:flex-start;max-height:calc(100vh - 110px);overflow:auto;font-size:13px;border-right:1px solid var(--line);padding-right:10px}
.toc-t{font-weight:700;margin:6px 0}.toc-m{margin:12px 0 4px;font-weight:700;color:#000;font-size:13px}
.toc-l{display:block;color:var(--mut);padding:2.5px 0;border-left:2px solid transparent;padding-left:8px}
.toc-l:hover{color:var(--acc)}.toc-top{color:var(--fg);font-weight:600}
main{flex:1;min-width:0}
h2{font-size:17px;border-bottom:2px solid var(--line);padding-bottom:6px;margin:26px 0 12px}
h3{font-size:15px;margin:20px 0 10px;color:#000}
.notes{display:grid;gap:8px;margin:8px 0 14px}
.note{background:#fff8e6;border:1px solid #f0dfae;border-radius:8px;padding:8px 11px;font-size:12.8px;color:#5a4a1a}
.nt{display:inline-block;font-weight:700;margin-right:6px;color:#8a6a00}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 13px;margin:8px 0}
.cards2{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:8px}
.cards2 .card{margin:0}
.ch{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}
.ct{font-weight:700;font-size:14px}
.tag{font-size:11px;border-radius:4px;padding:1px 6px;background:#eef1f5;color:#445}
.t-core{background:#fde7e7;color:#a01}b.t-main{background:#e3f0ff;color:#06c}
.t-main{background:#e3f0ff;color:#06c}.t-exp{background:#f1e7ff;color:#63c}
.t-off{background:#e8f5e9;color:#1b7f3b}.t-ref{background:#eef1f5;color:#556}
.t-remote{background:#fff3e0;color:#b26a00}.t-priv{background:#ffe9ec;color:#a33}
.t-code{background:#e6f7f7;color:#067}.t-model{background:#e8eaf6;color:#35c}
.t-env{background:#f3f0e6;color:#6a5a2a}.t-eval{background:#e8f5e9;color:#2a6}
.t-plan{background:#eef7e6;color:#4a7}.t-prep{background:#eef1f5;color:#667}
.t-pub{background:#e8f5e9;color:#1b7f3b}
.cd{color:#3c434c;font-size:13px;margin-top:4px}
.reads{color:var(--mut);font-size:12px;margin-top:3px}
.paths{display:flex;flex-direction:column;gap:3px;margin-top:7px}
.pchip{display:flex;align-items:center;gap:6px;font-size:12px;background:#f2f4f7;border:1px solid #e6e9ee;border-radius:6px;padding:2px 6px;max-width:100%}
.pchip .mb{flex:0 0 auto;color:#666;font-size:10.5px;border:1px solid #d5dae1;border-radius:3px;padding:0 4px;background:#fff}
.pchip .pt{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-family:ui-monospace,Consolas,monospace;color:#333}
.pchip a.pt{color:var(--acc);text-decoration:none}.pchip a.pt:hover{text-decoration:underline}
.pchip.miss{background:#fdecec;border-color:#f3c9c9}.pchip.miss .pt{color:#a33}
.pchip.miss a.pt{color:#a33;pointer-events:none}
.pchip.off{opacity:.62}.pchip.off a.pt{color:#333;pointer-events:none;text-decoration:none}
.qlink.off{opacity:.55;cursor:default;color:#667}
.pchip .cp{margin-left:auto;flex:0 0 auto;border:1px solid #d5dae1;background:#fff;border-radius:4px;font-size:10.5px;color:#555;cursor:pointer;padding:0 5px}
.pchip .cp:hover{background:#eef1f5}
.quick{margin-top:6px;font-size:12.5px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.ql-t{color:var(--mut)}.qlink{font-family:ui-monospace,Consolas,monospace;background:#eef6ff;border:1px solid #d6e6fa;border-radius:5px;padding:1px 6px;cursor:pointer;color:#06c}
.qlink.miss{background:#fdecec;border-color:#f3c9c9;color:#a33;text-decoration:line-through}
.links{margin-top:7px;display:flex;flex-wrap:wrap;gap:6px}
.lbtn{font-size:12px;border:1px solid var(--line);border-radius:6px;padding:2px 9px;background:#fff}
.lbtn:hover{text-decoration:none;border-color:var(--acc)}
.l-github{color:#24292f}.l-hf{color:#b26a00}.l-arxiv{color:#b31b1b}.l-doi{color:#06c}.l-web{color:#067}
.tablewrap{background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0}
.tcap{font-weight:700;font-size:13.5px;margin-bottom:6px}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border-bottom:1px solid #eef0f3;text-align:left;padding:4.5px 8px;vertical-align:top}
th{color:#333;background:#fafbfc;white-space:nowrap}
.qk{font-weight:600;white-space:nowrap}
.jump{font-size:11.5px;color:var(--mut);margin-right:5px}
footer{max-width:1280px;margin:0 auto;padding:10px 20px 40px;color:var(--mut);font-size:12px}
.hidden{display:none !important}
.muted{color:var(--mut);font-size:12px;margin-top:4px}
.lead{color:#2f3a46;font-size:12.8px;margin-top:4px;padding-left:8px;border-left:3px solid #dbe4ee}
.plead{color:#44505e;font-size:13px;margin:-4px 0 10px;padding-left:9px;border-left:3px solid #cfe0f4}
.guides .tablewrap{margin:10px 0}
.guides td{font-size:12.3px}
kbd{background:#eef1f5;border-radius:3px;padding:0 4px;font-size:11px}
#navbtn{display:none;border:1px solid var(--line);background:#fff;border-radius:6px;padding:4px 10px;font-size:12.5px;cursor:pointer;color:var(--fg)}
#navbtn:hover{border-color:var(--acc);color:var(--acc)}
#backdrop{display:none}
@media (max-width:1000px){
  #navbtn{display:inline-block}
  nav#toc{display:none;position:fixed;left:0;top:0;bottom:0;width:290px;max-width:86vw;background:#fff;z-index:60;padding:16px 14px;overflow:auto;border-right:1px solid var(--line);box-shadow:0 8px 30px rgba(0,0,0,.18);max-height:100vh}
  body.nav-open nav#toc{display:block}
  body.nav-open #backdrop{display:block;position:fixed;inset:0;background:rgba(15,20,30,.32);z-index:50}
  .wrap{display:block;padding:12px}
  .cards2{grid-template-columns:1fr}
}
"""

JS = r"""
const DISTRO = "__DISTRO__";
const SSH_HOST = "my-new-linux";
const MODES = __MODES__;
let mode = null;
function isWin(){ return /Windows/i.test(navigator.userAgent); }
function detectMode(){
  try{ const saved = localStorage.getItem("navmode"); if(saved && MODES.indexOf(saved)>=0) return saved; }catch(e){}
  if(isWin() && MODES.indexOf("vscode")>=0) return "vscode";
  if(!isWin() && location.pathname.indexOf("/home/a/")===0 && MODES.indexOf("remote")>=0) return "remote";
  return MODES.indexOf("wsl")>=0 ? "wsl" : MODES[0];
}
function hrefFor(m, p){
  if(mode === "vscode"){
    const enc = encodeURI(p);
    return m === "wsl"
      ? "vscode://vscode-remote/wsl+" + DISTRO + enc
      : "vscode://vscode-remote/ssh-remote+" + SSH_HOST + enc;
  }
  if(m !== mode) return null;
  if(m === "wsl" && isWin()) return "file:///wsl.localhost/" + DISTRO + encodeURI(p);
  return "file://" + encodeURI(p);
}
function linkify(el, p, text){
  if(el.tagName === "A") return el;
  const a = document.createElement("a");
  a.textContent = text; a.title = p;
  a.className = el.className; a.dataset.m = el.dataset.m; a.dataset.p = p;
  el.replaceWith(a); return a;
}
function applyMode(){
  if(!MODES || !MODES.length) return;
  document.querySelectorAll(".modebtn").forEach(b=>b.classList.toggle("on", b.dataset.mode===mode));
  document.querySelectorAll(".pchip").forEach(ch=>{
    const m = ch.dataset.m, p = ch.dataset.p, pt = ch.querySelector(".pt");
    const href = ch.classList.contains("miss") ? null : hrefFor(m, p);
    ch.classList.toggle("off", !href);
    const a = linkify(pt, p, p);
    if(href){ a.href = href; } else { a.removeAttribute("href"); }
  });
  document.querySelectorAll(".qlink").forEach(q=>{
    const m = q.dataset.m, p = q.dataset.p;
    const href = q.classList.contains("miss") ? null : hrefFor(m, p);
    const a = linkify(q, p, q.textContent);
    if(href){ a.href = href; a.classList.remove("off"); }
    else { a.removeAttribute("href"); a.classList.add("off"); }
  });
  try{ localStorage.setItem("navmode", mode); }catch(e){}
}
function norm(s){ return String(s).toLowerCase().replace(/[_\-/.]+/g," ").replace(/\s+/g," ").trim(); }
function setupCopy(){
  document.addEventListener("click", ev=>{
    const b = ev.target.closest(".cp"); if(!b) return;
    const ch = b.closest(".pchip"); const p = ch.dataset.p;
    const done = ()=>{ b.textContent="已复制"; setTimeout(()=>b.textContent="复制",1200); };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(p).then(done).catch(()=>fallback(p,done));
    } else fallback(p, done);
  });
}
function fallback(txt, cb){
  const ta=document.createElement("textarea"); ta.value=txt; document.body.appendChild(ta);
  ta.select(); try{document.execCommand("copy"); cb();}catch(e){} document.body.removeChild(ta);
}
function setupSearch(){
  const q = document.getElementById("q"), cnt = document.getElementById("cnt");
  const items = ()=>document.querySelectorAll(".card, .tablewrap tbody tr");
  q.addEventListener("input", ()=>{
    const s = norm(q.value); let n=0;
    items().forEach(el=>{
      const t = norm(el.dataset.s || el.textContent);
      const hit = !s || t.indexOf(s) >= 0;
      el.classList.toggle("hidden", !hit); if(hit) n++;
    });
    document.querySelectorAll("h3").forEach(h=>{
      const sec=h.closest("section"); if(!sec) return;
      const vis=sec.querySelectorAll(".card:not(.hidden), .tablewrap:not(.hidden)").length>0;
      h.classList.toggle("hidden", !vis);
    });
    cnt.textContent = s ? ("命中 " + n + " 项") : "";
  });
}
document.addEventListener("DOMContentLoaded", ()=>{
  mode = detectMode();
  document.querySelectorAll(".modebtn").forEach(b=>b.addEventListener("click", ()=>{ mode=b.dataset.mode; applyMode(); }));
  const nb = document.getElementById("navbtn"), bd = document.getElementById("backdrop");
  if(nb){ nb.addEventListener("click", ()=>document.body.classList.toggle("nav-open")); }
  if(bd){ bd.addEventListener("click", ()=>document.body.classList.remove("nav-open")); }
  document.querySelectorAll("#toc a").forEach(a=>a.addEventListener("click", ()=>{
    if(window.innerWidth <= 1000) document.body.classList.remove("nav-open");
  }));
  window.addEventListener("resize", ()=>{
    if(window.innerWidth > 1000) document.body.classList.remove("nav-open");
  });
  applyMode(); setupCopy(); setupSearch();
  const obs = new IntersectionObserver(es=>{
    es.forEach(en=>{ if(!en.isIntersecting) return;
      document.querySelectorAll("#toc .toc-l").forEach(a=>a.classList.remove("cur"));
      const a=document.querySelector('#toc a[href="#'+en.target.id+'"]'); if(a) a.classList.add("cur");
    });
  }, {rootMargin:"-20% 0px -70% 0px"});
  document.querySelectorAll("section[id]").forEach(s=>obs.observe(s));
});
"""


JS_PUBLIC = r"""
function fallback(txt, cb){
  const ta=document.createElement("textarea"); ta.value=txt; document.body.appendChild(ta);
  ta.select(); try{document.execCommand("copy"); cb();}catch(e){} document.body.removeChild(ta);
}
function setupCopy(){
  document.addEventListener("click", ev=>{
    const b = ev.target.closest(".cp"); if(!b) return;
    const ch = b.closest(".pchip"); const p = ch.dataset.p;
    const done = ()=>{ b.textContent="已复制"; setTimeout(()=>b.textContent="复制",1200); };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(p).then(done).catch(()=>fallback(p,done));
    } else fallback(p, done);
  });
}
function norm(s){ return String(s).toLowerCase().replace(/[_\-/.]+/g," ").replace(/\s+/g," ").trim(); }
function setupSearch(){
  const q=document.getElementById("q"), cnt=document.getElementById("cnt");
  const items=()=>document.querySelectorAll(".card, .tablewrap tbody tr");
  q.addEventListener("input", ()=>{
    const s=norm(q.value); let n=0;
    items().forEach(el=>{
      const t=norm(el.dataset.s || el.textContent);
      const hit=!s || t.indexOf(s)>=0;
      el.classList.toggle("hidden", !hit); if(hit) n++;
    });
    document.querySelectorAll("h3").forEach(h=>{
      const sec=h.closest("section"); if(!sec) return;
      const vis=sec.querySelectorAll(".card:not(.hidden), .tablewrap:not(.hidden)").length>0;
      h.classList.toggle("hidden", !vis);
    });
    cnt.textContent = s ? ("命中 " + n + " 项") : "";
  });
}
document.addEventListener("DOMContentLoaded", ()=>{
  const nb=document.getElementById("navbtn"), bd=document.getElementById("backdrop");
  if(nb){ nb.addEventListener("click", ()=>document.body.classList.toggle("nav-open")); }
  if(bd){ bd.addEventListener("click", ()=>document.body.classList.remove("nav-open")); }
  document.querySelectorAll("#toc a").forEach(a=>a.addEventListener("click", ()=>{
    if(window.innerWidth <= 1000) document.body.classList.remove("nav-open");
  }));
  window.addEventListener("resize", ()=>{ if(window.innerWidth > 1000) document.body.classList.remove("nav-open"); });
  setupCopy(); setupSearch();
  const obs = new IntersectionObserver(es=>{
    es.forEach(en=>{ if(!en.isIntersecting) return;
      document.querySelectorAll("#toc .toc-l").forEach(a=>a.classList.remove("cur"));
      const a=document.querySelector('#toc a[href="#'+en.target.id+'"]'); if(a) a.classList.add("cur");
    });
  }, {rootMargin:"-20% 0px -70% 0px"});
  document.querySelectorAll("section[id]").forEach(s=>obs.observe(s));
});
"""

PUBLIC_DROP_TABLES = {"t_gloway", "t_lexar", "t_win"}
PUBLIC_DROP_CARDS = {"c_lean_wsl"}
PUBLIC_TITLE_OVERRIDE = {}


def main():
    global VARIANT
    out_path = os.path.join(HERE, "roadmap.html")
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--variant=gh" in sys.argv:
        VARIANT = "gh"
        out_path = os.path.join(HERE, "roadmap-gh.html")
    if "--variant=public" in sys.argv:
        VARIANT = "public"
        out_path = os.path.join(HERE, "roadmap-public.html")
    if pos:
        out_path = pos[0]

    global ACTIVE_MODULES, ACTIVE_NOTES
    if VARIANT in ("gh", "public"):
        modules = []
        for mod in MODULES:
            parts = []
            for part in mod["parts"]:
                items = []
                for it in part["items"]:
                    if isinstance(it, dict) and it.get("type") == "table":
                        if VARIANT == "public" and it.get("id") in PUBLIC_DROP_TABLES:
                            continue
                        items.append(dict(it))
                    elif isinstance(it, dict) and "id" in it:
                        if VARIANT == "public" and it["id"] in PUBLIC_DROP_CARDS:
                            continue
                        items.append(it)
                if not items:
                    continue
                title = part["title"]
                if VARIANT == "public":
                    title = PUBLIC_TITLE_OVERRIDE.get(part["id"], title)
                parts.append({**part, "title": title, "items": items})
            if parts:
                modules.append({**mod, "parts": parts})
        ACTIVE_MODULES = modules
        ACTIVE_NOTES = [n for n in NOTES if not n[2]]

    if VARIANT == "public":
        modes = []
    elif VARIANT == "gh":
        modes = ["vscode"]
    else:
        modes = ["vscode", "remote", "wsl"]
    mode_labels = {"vscode": "Windows · 用 VSCode 跳转", "remote": "在 my-new-linux 上打开",
                   "wsl": "在 WSL 内打开（file://）"}

    suffix = {"gh": " · GitHub 版", "public": " · 公开版（仅云端链接）"}.get(VARIANT, "")
    body = []
    body.append('<header>')
    body.append(f'<h1>{e(META["title"])}{suffix}</h1>')
    body.append(f'<div class="sub">{e(META["subtitle"])} · 生成 {e(META["generated"])} · 单文件离线</div>')
    body.append('<div class="bar">')
    body.append('<button id="navbtn" type="button" title="展开/收起目录">☰ 目录</button>')
    for m in modes:
        body.append(f'<span class="modebtn" data-mode="{m}">{mode_labels[m]}</span>')
    body.append('<input id="q" type="search" placeholder="搜索：标题 / 路径 / 关键词（如 value head、v1-result）">')
    body.append('<span id="cnt"></span>')
    body.append('</div></header>')
    body.append('<div class="wrap">')
    body.append(toc())
    body.append('<main>')
    body.append(notes_section())
    body.append(quick_section())
    body.append(guides_section())
    for mod in ACTIVE_MODULES:
        body.append(f'<h2>{e(mod["title"])}</h2>')
        for part in mod["parts"]:
            body.append(f'<section id="{part["id"]}"><h3>{e(part["title"])}</h3>')
            if part.get("lead"):
                body.append(f'<div class="plead">{e(part["lead"])}</div>')
            body.append('<div class="cards2">')
            body.append(render_items(part["items"]))
            body.append('</div></section>')
    body.append("</main></div>")
    body.append('<div id="backdrop"></div>')
    if VARIANT == "public":
        foot = ('本页为公开版：全部链接均为云端资源（GitHub / HuggingFace / arXiv）。'
                '窄屏或放大后点左上角「☰ 目录」展开侧栏。')
    elif VARIANT == "gh":
        foot = ('本页为 GitHub 版：所有 WSL 本机路径均已替换为 GitHub 链接（含新公开的 '
                'reap-source-code-explain / Lean-source-code-learning-to-know-reap / '
                'alphaproof-official-materials）；F/E 盘路径保留，Windows 下默认用 VSCode 跳转。')
    else:
        foot = ('路径存在性：⚠ = 当前不存在 / 无标记 = 未校验。'
                'Windows 下默认「VSCode 跳转」（wsl.localhost 在 mirrored 网络模式不可用）；'
                'file:// 模式仅在该文件所在机器上可点。窄屏或放大后点「☰ 目录」展开侧栏。')
    body.append(f'<footer>生成于 {e(META["generated"])} · 重新生成：python3 gen_roadmap.py · {foot}</footer>')

    html_doc = ("<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
                f"<title>{e(META['title'])}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
                + "\n".join(body) +
                f"\n<script>{JS_PUBLIC if VARIANT == 'public' else JS.replace('__DISTRO__', META['wsl_distro']).replace('__MODES__', json.dumps(modes))}</script>\n</body>\n</html>\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print("wrote", out_path, len(html_doc), "bytes")


if __name__ == "__main__":
    main()
