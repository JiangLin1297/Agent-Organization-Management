"""
统一实验运行器（Anthropic SDK版）
用法：python run_all.py [deepseek|mimo]
"""
import json, os, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import get_config

try:
    import anthropic
except ImportError:
    print("pip install anthropic"); sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "deepseek"
cfg = get_config(PROVIDER)
BASE_DIR = Path(__file__).parent / PROVIDER
BASE_DIR.mkdir(exist_ok=True)

TASK_PROMPT = """请实现一个网页应用：拼豆图纸生成器。

功能要求：
1. 用户上传任意图片
2. 自动转换为"拼豆图纸"：
   - 网格化（支持选择 32x32 / 48x48 / 64x64）
   - 降色（限制颜色数量，如 10-20 色，使用中位切分法或K-means）
   - 每个格子对应一个拼豆颜色
3. 输出：
   - 可视化网格（Canvas渲染，每个格子显示对应颜色）
   - 每种颜色数量统计表格（用于实际拼豆采购）
   - 支持放大/缩小查看
4. 前端可直接运行（单个HTML文件）

技术约束：
- 不依赖后端（纯前端实现）
- 使用 Canvas / ImageData 处理图像
- 输出一个完整可运行的 index.html
- 支持桌面端和移动端"""

PROMPTS_DIR = Path(__file__).parent / "condition_C" / "prompts"

def load_prompt(name):
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")

def call_llm(client, system_prompt, user_prompt, max_tokens=8000):
    start = time.time()
    try:
        resp = client.messages.create(
            model=cfg["model"],
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.3,
        )
        elapsed = time.time() - start
        text = resp.content[0].text if resp.content else ""
        tokens = (resp.usage.input_tokens + resp.usage.output_tokens) if resp.usage else 0
        return text, tokens, elapsed
    except Exception as e:
        elapsed = time.time() - start
        print(f"    API失败: {e}")
        return "", 0, elapsed

def extract_html(text):
    if "```html" in text:
        s = text.index("```html") + 7
        rest = text[s:]
        if "```" in rest:
            e = rest.index("```")
            return rest[:e].strip()
        return rest.strip()
    if "```" in text:
        s = text.index("```") + 3
        nl = text.index("\n", s) if "\n" in text[s:] else len(text)
        s = nl + 1
        rest = text[s:]
        if "```" in rest:
            e = rest.index("```")
            return rest[:e].strip()
        return rest.strip()
    t = text.strip()
    if t.startswith("<!DOCTYPE") or t.startswith("<html"):
        return t
    idx = t.find("<")
    if idx >= 0:
        return t[idx:]
    return t

def save_condition(cond_dir, html, log, context_log):
    out = cond_dir / "output"
    out.mkdir(parents=True, exist_ok=True)
    logs = cond_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    (logs / "token_usage.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(logs / "context_growth.txt", "w", encoding="utf-8") as f:
        for e in context_log:
            f.write(f"Step {e.get('step', e.get('round', '?'))} [{e['agent']:25s}]: ctx={e['context_length']:>10,}\n")
        f.write(f"\nMax: {max(e['context_length'] for e in context_log):,}\nTotal: {log['total_tokens']:,}\n")

# ── Condition A ────────────────────────────────────────────
def run_condition_A(client):
    print("\n" + "="*60)
    print(f"条件A: 单Agent基线 | {PROVIDER}")
    print("="*60)
    d = BASE_DIR / "condition_A"
    start = time.time()
    text, tokens, elapsed = call_llm(client, "你是一个资深全栈开发者。请直接实现用户要求的完整功能，输出可运行的HTML代码。", TASK_PROMPT)
    html = extract_html(text)
    total = time.time() - start
    log = {"condition": "A", "provider": PROVIDER, "model": cfg["model"],
           "total_tokens": tokens, "api_calls": 1, "total_time": round(total,1),
           "html_length": len(html), "details": [{"tokens": tokens}]}
    ctx_log = [{"step": 1, "agent": "single", "context_length": len(TASK_PROMPT)}]
    save_condition(d, html, log, ctx_log)
    print(f"  Token={tokens}, HTML={len(html)}字符, 耗时={total:.1f}s")
    return log

# ── Condition B ────────────────────────────────────────────
def run_condition_B(client):
    print("\n" + "="*60)
    print(f"条件B: 迭代架构(7轮) | {PROVIDER}")
    print("="*60)
    d = BASE_DIR / "condition_B"
    sp = "你是一个资深全栈开发者。请根据用户要求改进代码，输出完整可运行的HTML文件。"
    rounds = [
        "请实现上述任务的基础版本，输出完整可运行的HTML文件。",
        "基于以下已有代码进行改进：提升图像处理质量、优化颜色量化、改善UI。",
        "基于以下已有代码进行改进：优化网格渲染、增加颜色统计准确性、改善交互。",
        "基于以下已有代码进行改进：提升降色效果、增加网格大小选项、优化移动端。",
        "基于以下已有代码进行改进：增加放大/缩小功能、优化Canvas性能。",
        "基于以下已有代码进行改进：完善所有功能、修复Bug、优化代码结构。",
        "基于以下已有代码进行最终改进：确保所有功能正常、输出最终版本。",
    ]
    history = []
    ctx_log = []
    details = []
    total_start = time.time()
    for i, rp in enumerate(rounds):
        print(f"  [Round {i+1}/7] ", end="")
        if i == 0:
            up = f"任务：\n{TASK_PROMPT}\n\n{rp}"
        else:
            hist = "\n\n".join([f"=== 第{j+1}轮 ===\n{o}" for j, o in enumerate(history)])
            up = f"任务：\n{TASK_PROMPT}\n\n历史输出：\n{hist}\n\n{rp}"
        cl = len(up)
        text, tokens, elapsed = call_llm(client, sp, up)
        history.append(text)
        ctx_log.append({"round": i+1, "agent": "iterative", "context_length": cl})
        details.append({"round": i+1, "tokens": tokens, "context_length": cl})
        print(f"Token={tokens}, ctx={cl:,}")
    total = time.time() - total_start
    html = extract_html(history[-1])
    tt = sum(x["tokens"] for x in details)
    log = {"condition": "B", "provider": PROVIDER, "model": cfg["model"],
           "total_tokens": tt, "api_calls": 7, "total_time": round(total,1),
           "html_length": len(html), "max_context": max(x["context_length"] for x in details),
           "details": details}
    save_condition(d, html, log, ctx_log)
    print(f"  总Token={tt}, 最大ctx={max(x['context_length'] for x in details):,}, 耗时={total:.1f}s")
    return log

# ── Condition C (with CC) ──────────────────────────────────
def run_condition_C(client):
    print("\n" + "="*60)
    print(f"条件C: OIMAC+ContextController | {PROVIDER}")
    print("="*60)
    d = BASE_DIR / "condition_C"
    ctx_log = []
    details = []
    total_start = time.time()

    def step(name, phase, sp_name, up, max_tok=4000):
        print(f"  [{len(details)+1}/7] {name}: {phase}...")
        sp = load_prompt(sp_name)
        cl = len(up)
        text, tokens, elapsed = call_llm(client, sp, up, max_tokens=max_tok)
        details.append({"step": len(details)+1, "agent": name, "phase": phase, "tokens": tokens, "context_length": cl})
        ctx_log.append({"step": len(details), "agent": name, "context_length": cl})
        print(f"    Token={tokens}, ctx={cl:,}")
        return text

    def cc(text, mx=24000):
        return text[:mx] + "\n[...截断...]" if len(text) > mx else text

    td = step("coordinator", "任务分解", "coordinator", f"请分解任务：\n\n{TASK_PROMPT}", 2000)
    rd = step("product_manager", "需求定义", "product_manager", f"任务分解：\n{cc(td)}\n\n任务：\n{TASK_PROMPT}\n\n请输出PRD。", 2000)
    ad = step("architect", "架构设计", "architect", f"需求文档：\n{cc(rd)}\n\n任务：\n{TASK_PROMPT}\n\n请输出架构设计。", 2000)
    fd = step("frontend_dev", "前端实现", "frontend_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现前端UI。只输出你负责的部分。")
    ip = step("image_processing_dev", "图像处理", "image_processing_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现图像处理算法。只输出你负责的部分。")
    tr = step("tester", "测试审查", "tester", f"前端代码：\n{cc(fd)}\n\n图像处理代码：\n{cc(ip)}\n\n请审查代码。", 2000)
    fi_raw = step("coordinator", "最终整合", "coordinator",
        f"请整合为完整HTML：\n\n需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n前端：\n{cc(fd)}\n\n图像处理：\n{cc(ip)}\n\n测试报告：\n{cc(tr)}\n\n任务：\n{TASK_PROMPT}\n\n直接输出HTML代码。", 8000)

    total = time.time() - total_start
    html = extract_html(fi_raw)
    tt = sum(x["tokens"] for x in details)
    mc = max(x["context_length"] for x in details)
    log = {"condition": "C", "provider": PROVIDER, "model": cfg["model"],
           "total_tokens": tt, "api_calls": 7, "total_time": round(total,1),
           "html_length": len(html), "max_context": mc, "details": details}
    save_condition(d, html, log, ctx_log)
    print(f"  总Token={tt}, 最大ctx={mc:,}, 耗时={total:.1f}s")
    return log

# ── Condition D (no CC) ────────────────────────────────────
def run_condition_D(client):
    print("\n" + "="*60)
    print(f"条件D: OIMAC-无ContextController | {PROVIDER}")
    print("="*60)
    d = BASE_DIR / "condition_D"
    all_out = []
    ctx_log = []
    details = []
    total_start = time.time()

    def step(name, phase, sp_name, max_tok=4000):
        print(f"  [{len(details)+1}/7] {name}: {phase}...")
        sp = load_prompt(sp_name)
        full_ctx = "\n\n".join([f"=== {lab} ===\n{o}" for lab, o in all_out])
        if full_ctx:
            up = f"所有前序角色完整产出：\n\n{full_ctx}\n\n任务：\n{TASK_PROMPT}\n\n请完成你的工作。"
        else:
            up = f"任务：\n{TASK_PROMPT}\n\n请进行任务分解。"
        cl = len(up)
        text, tokens, elapsed = call_llm(client, sp, up, max_tokens=max_tok)
        details.append({"step": len(details)+1, "agent": name, "phase": phase, "tokens": tokens, "context_length": cl})
        ctx_log.append({"step": len(details), "agent": name, "context_length": cl})
        all_out.append((name, text))
        print(f"    Token={tokens}, ctx={cl:,}")
        return text

    td = step("coordinator", "任务分解", "coordinator", 2000)
    rd = step("product_manager", "需求定义", "product_manager", 2000)
    ad = step("architect", "架构设计", "architect", 2000)
    fd = step("frontend_dev", "前端实现", "frontend_dev")
    ip = step("image_processing_dev", "图像处理", "image_processing_dev")
    tr = step("tester", "测试审查", "tester", 2000)
    fi_raw = step("coordinator", "最终整合", "coordinator", 8000)

    total = time.time() - total_start
    html = extract_html(fi_raw)
    tt = sum(x["tokens"] for x in details)
    mc = max(x["context_length"] for x in details)
    log = {"condition": "D", "provider": PROVIDER, "model": cfg["model"],
           "total_tokens": tt, "api_calls": 7, "total_time": round(total,1),
           "html_length": len(html), "max_context": mc, "details": details}
    save_condition(d, html, log, ctx_log)
    print(f"  总Token={tt}, 最大ctx={mc:,}, 耗时={total:.1f}s")
    return log

# ── Main ───────────────────────────────────────────────────
def main():
    print("="*60)
    print(f"拼豆图生成器实验 | Provider: {PROVIDER}")
    print(f"Model: {cfg['model']}")
    print(f"Base URL: {cfg['base_url']}")
    print("="*60)

    client = anthropic.Anthropic(api_key=cfg["api_key"], base_url=cfg["base_url"])

    results = {}
    results["A"] = run_condition_A(client)
    results["B"] = run_condition_B(client)
    results["C"] = run_condition_C(client)
    results["D"] = run_condition_D(client)

    print("\n" + "="*60)
    print(f"实验总结 | {PROVIDER} | {cfg['model']}")
    print("="*60)
    print(f"{'条件':<6} {'Token':>10} {'Calls':>6} {'HTML':>8} {'最大ctx':>12} {'耗时':>8}")
    print("-"*54)
    for c in ["A","B","C","D"]:
        r = results[c]
        print(f"{c:<6} {r['total_tokens']:>10,} {r['api_calls']:>6} {r['html_length']:>8,} {r.get('max_context',0):>12,} {r['total_time']:>7.1f}s")

    ratio_cb = results["B"]["total_tokens"] / results["C"]["total_tokens"] if results["C"]["total_tokens"] else 0
    ratio_dc = results["D"]["total_tokens"] / results["C"]["total_tokens"] if results["C"]["total_tokens"] else 0
    print(f"\nOIMAC效果:  C/B = {ratio_cb:.2f}x (条件C vs 迭代)")
    print(f"CC贡献:    D/C = {ratio_dc:.2f}x (无CC vs 有CC)")

    summary = {"provider": PROVIDER, "model": cfg["model"], "timestamp": datetime.now().isoformat(),
               "results": results, "ratios": {"C_vs_B": round(ratio_cb,2), "D_vs_C": round(ratio_dc,2)}}
    (BASE_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n结果已保存至 {BASE_DIR}/")

if __name__ == "__main__":
    main()
