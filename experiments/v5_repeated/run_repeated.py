"""
V5.3 Repeated Experiment Runner
Runs each condition 5 times per model for statistical validation.
Usage: python run_repeated.py [deepseek|mimo|all]
"""
import json, os, sys, time, statistics
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "OIMAC_experiment_Pixel"))
from config import get_config

try:
    import anthropic
except ImportError:
    print("pip install anthropic"); sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

NUM_RUNS = 5
PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "all"

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

PROMPTS_DIR = Path(__file__).parent.parent / "OIMAC_experiment_Pixel" / "condition_C" / "prompts"

def load_prompt(name):
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")

def call_llm(client, system_prompt, user_prompt, max_tokens=8000, model=None):
    start = time.time()
    try:
        resp = client.messages.create(
            model=model or cfg["model"],
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
        print(f"    API error: {e}")
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

def run_condition_A(client, run_id, provider, cfg_local):
    d = Path(__file__).parent / provider / "condition_A" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    text, tokens, elapsed = call_llm(client, "你是一个资深全栈开发者。请直接实现用户要求的完整功能，输出可运行的HTML代码。", TASK_PROMPT, model=cfg_local["model"])
    html = extract_html(text)
    result = {"condition": "A", "run": run_id, "tokens": tokens, "time": round(elapsed, 1), "html_length": len(html)}
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_condition_B(client, run_id, provider, cfg_local):
    d = Path(__file__).parent / provider / "condition_B" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
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
    total_tokens = 0
    start = time.time()
    for i, rp in enumerate(rounds):
        if i == 0:
            up = f"任务：\n{TASK_PROMPT}\n\n{rp}"
        else:
            hist = "\n\n".join([f"=== 第{j+1}轮 ===\n{o}" for j, o in enumerate(history)])
            up = f"任务：\n{TASK_PROMPT}\n\n历史输出：\n{hist}\n\n{rp}"
        text, tokens, _ = call_llm(client, sp, up, model=cfg_local["model"])
        history.append(text)
        total_tokens += tokens
    elapsed = time.time() - start
    html = extract_html(history[-1])
    result = {"condition": "B", "run": run_id, "tokens": total_tokens, "time": round(elapsed, 1), "html_length": len(html)}
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_condition_C(client, run_id, provider, cfg_local):
    d = Path(__file__).parent / provider / "condition_C" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    total_tokens = 0
    start = time.time()

    def step(name, phase, sp_name, up, max_tok=4000):
        sp = load_prompt(sp_name)
        text, tokens, _ = call_llm(client, sp, up, max_tokens=max_tok, model=cfg_local["model"])
        return text, tokens

    def cc(text, mx=24000):
        return text[:mx] + "\n[...截断...]" if len(text) > mx else text

    td, t = step("coordinator", "任务分解", "coordinator", f"请分解任务：\n\n{TASK_PROMPT}", 2000); total_tokens += t
    rd, t = step("product_manager", "需求定义", "product_manager", f"任务分解：\n{cc(td)}\n\n任务：\n{TASK_PROMPT}\n\n请输出PRD。", 2000); total_tokens += t
    ad, t = step("architect", "架构设计", "architect", f"需求文档：\n{cc(rd)}\n\n任务：\n{TASK_PROMPT}\n\n请输出架构设计。", 2000); total_tokens += t
    fd, t = step("frontend_dev", "前端实现", "frontend_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现前端UI。只输出你负责的部分。"); total_tokens += t
    ip, t = step("image_processing_dev", "图像处理", "image_processing_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现图像处理算法。只输出你负责的部分。"); total_tokens += t
    tr, t = step("tester", "测试审查", "tester", f"前端代码：\n{cc(fd)}\n\n图像处理代码：\n{cc(ip)}\n\n请审查代码。", 2000); total_tokens += t
    fi_raw, t = step("coordinator", "最终整合", "coordinator",
        f"请整合为完整HTML：\n\n需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n前端：\n{cc(fd)}\n\n图像处理：\n{cc(ip)}\n\n测试报告：\n{cc(tr)}\n\n任务：\n{TASK_PROMPT}\n\n直接输出HTML代码。", 8000); total_tokens += t

    elapsed = time.time() - start
    html = extract_html(fi_raw)
    result = {"condition": "C", "run": run_id, "tokens": total_tokens, "time": round(elapsed, 1), "html_length": len(html)}
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_condition_D(client, run_id, provider, cfg_local):
    d = Path(__file__).parent / provider / "condition_D" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    all_out = []
    total_tokens = 0
    start = time.time()

    def step(name, phase, sp_name, max_tok=4000):
        sp = load_prompt(sp_name)
        full_ctx = "\n\n".join([f"=== {lab} ===\n{o}" for lab, o in all_out])
        if full_ctx:
            up = f"所有前序角色完整产出：\n\n{full_ctx}\n\n任务：\n{TASK_PROMPT}\n\n请完成你的工作。"
        else:
            up = f"任务：\n{TASK_PROMPT}\n\n请进行任务分解。"
        text, tokens, _ = call_llm(client, sp, up, max_tokens=max_tok, model=cfg_local["model"])
        all_out.append((name, text))
        return text, tokens

    _, t = step("coordinator", "任务分解", "coordinator", 2000); total_tokens += t
    _, t = step("product_manager", "需求定义", "product_manager", 2000); total_tokens += t
    _, t = step("architect", "架构设计", "architect", 2000); total_tokens += t
    _, t = step("frontend_dev", "前端实现", "frontend_dev"); total_tokens += t
    _, t = step("image_processing_dev", "图像处理", "image_processing_dev"); total_tokens += t
    _, t = step("tester", "测试审查", "tester", 2000); total_tokens += t
    fi_raw, t = step("coordinator", "最终整合", "coordinator", 8000); total_tokens += t

    elapsed = time.time() - start
    html = extract_html(fi_raw)
    result = {"condition": "D", "run": run_id, "tokens": total_tokens, "time": round(elapsed, 1), "html_length": len(html)}
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_model(provider):
    cfg_local = get_config(provider)
    client = anthropic.Anthropic(api_key=cfg_local["api_key"], base_url=cfg_local["base_url"])
    all_results = {"A": [], "B": [], "C": [], "D": []}

    for run_id in range(1, NUM_RUNS + 1):
        print(f"\n{'='*60}")
        print(f"Provider: {provider} | Run {run_id}/{NUM_RUNS}")
        print(f"{'='*60}")

        for cond, func in [("A", run_condition_A), ("B", run_condition_B), ("C", run_condition_C), ("D", run_condition_D)]:
            print(f"  Condition {cond}...", end=" ", flush=True)
            result = func(client, run_id, provider, cfg_local)
            all_results[cond].append(result)
            print(f"tokens={result['tokens']}, time={result['time']}s")

    # Save raw results
    out_dir = Path(__file__).parent / provider
    (out_dir / "all_runs.json").write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")

    # Compute statistics
    stats = {}
    for cond in ["A", "B", "C", "D"]:
        tokens_list = [r["tokens"] for r in all_results[cond]]
        stats[cond] = {
            "mean": round(statistics.mean(tokens_list), 1),
            "std": round(statistics.stdev(tokens_list), 1) if len(tokens_list) > 1 else 0,
            "min": min(tokens_list),
            "max": max(tokens_list),
            "n": len(tokens_list),
            "values": tokens_list,
        }

    # t-tests (unpaired, two-tailed)
    from scipy import stats as sp_stats
    def do_t_test(a_vals, b_vals, label):
        t_stat, p_val = sp_stats.ttest_ind(a_vals, b_vals)
        return {"label": label, "t_stat": round(t_stat, 4), "p_value": round(p_val, 6), "significant_005": bool(p_val < 0.05)}

    t_tests = []
    t_tests.append(do_t_test(stats["C"]["values"], stats["B"]["values"], "C_vs_B"))
    t_tests.append(do_t_test(stats["C"]["values"], stats["D"]["values"], "C_vs_D"))
    t_tests.append(do_t_test(stats["B"]["values"], stats["D"]["values"], "B_vs_D"))

    summary = {
        "provider": provider,
        "model": cfg_local["model"],
        "timestamp": datetime.now().isoformat(),
        "num_runs": NUM_RUNS,
        "stats": stats,
        "t_tests": t_tests,
    }
    (out_dir / "stats_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Results for {provider} ({cfg_local['model']})")
    print(f"{'='*60}")
    for cond in ["A", "B", "C", "D"]:
        s = stats[cond]
        print(f"  {cond}: mean={s['mean']:,.0f} std={s['std']:,.0f} min={s['min']:,} max={s['max']:,}")
    for tt in t_tests:
        sig = "***" if tt["p_value"] < 0.001 else "**" if tt["p_value"] < 0.01 else "*" if tt["p_value"] < 0.05 else "n.s."
        print(f"  {tt['label']}: t={tt['t_stat']}, p={tt['p_value']} {sig}")

    return summary

def main():
    if PROVIDER == "all":
        providers = ["deepseek", "mimo"]
    else:
        providers = [PROVIDER]

    all_summaries = {}
    for p in providers:
        all_summaries[p] = run_model(p)

    # Generate CSV
    csv_lines = ["provider,condition,mean_tokens,std_tokens,min_tokens,max_tokens,n"]
    for p, s in all_summaries.items():
        for cond in ["A", "B", "C", "D"]:
            st = s["stats"][cond]
            csv_lines.append(f"{p},{cond},{st['mean']},{st['std']},{st['min']},{st['max']},{st['n']}")

    # Add t-test rows
    csv_lines.append("")
    csv_lines.append("# T-Test Results")
    csv_lines.append("provider,comparison,t_stat,p_value,significant_005")
    for p, s in all_summaries.items():
        for tt in s["t_tests"]:
            csv_lines.append(f"{p},{tt['label']},{tt['t_stat']},{tt['p_value']},{tt['significant_005']}")

    out_path = Path(__file__).parent / "results_summary.csv"
    out_path.write_text("\n".join(csv_lines), encoding="utf-8")
    print(f"\nCSV saved to {out_path}")

if __name__ == "__main__":
    main()
