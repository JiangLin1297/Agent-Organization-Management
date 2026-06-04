"""
V5.3 Task 2: Data Analysis Task Experiment
Runs a non-HTML data analysis task to test generalization.
Usage: python run_task2.py [deepseek|mimo|all]
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

NUM_RUNS = 3
PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "all"

# A data analysis task - different from HTML generation
TASK_PROMPT = """请分析以下销售数据，生成一份完整的数据分析报告。

数据（CSV格式，5个区域，12个月）：
region,month,revenue,cost,units_sold,category
North,2025-01,125000,82000,450,Electronics
North,2025-02,132000,85000,480,Electronics
North,2025-03,118000,79000,420,Electronics
North,2025-04,145000,91000,520,Electronics
North,2025-05,156000,95000,560,Electronics
North,2025-06,168000,102000,600,Electronics
North,2025-07,142000,88000,510,Electronics
North,2025-08,138000,86000,495,Electronics
North,2025-09,151000,93000,540,Electronics
North,2025-10,162000,98000,580,Electronics
North,2025-11,175000,105000,625,Electronics
North,2025-12,198000,118000,710,Electronics
South,2025-01,98000,65000,380,Electronics
South,2025-02,105000,68000,400,Electronics
South,2025-03,92000,62000,355,Electronics
South,2025-04,112000,72000,430,Electronics
South,2025-05,119000,75000,455,Electronics
South,2025-06,128000,80000,490,Electronics
South,2025-07,115000,73000,440,Electronics
South,2025-08,110000,71000,425,Electronics
South,2025-09,121000,76000,465,Electronics
South,2025-10,130000,81000,500,Electronics
South,2025-11,140000,86000,535,Electronics
South,2025-12,158000,95000,605,Electronics
East,2025-01,85000,58000,320,Home
East,2025-02,89000,60000,335,Home
East,2025-03,82000,56000,310,Home
East,2025-04,95000,63000,360,Home
East,2025-05,102000,67000,385,Home
East,2025-06,110000,71000,415,Home
East,2025-07,98000,65000,370,Home
East,2025-08,94000,63000,355,Home
East,2025-09,101000,66000,380,Home
East,2025-10,108000,70000,408,Home
East,2025-11,116000,74000,438,Home
East,2025-12,132000,83000,498,Home
West,2025-01,72000,50000,280,Home
West,2025-02,76000,52000,295,Home
West,2025-03,68000,48000,265,Home
West,2025-04,82000,55000,320,Home
West,2025-05,88000,58000,342,Home
West,2025-06,95000,62000,370,Home
West,2025-07,85000,57000,330,Home
West,2025-08,81000,55000,315,Home
West,2025-09,87000,57500,338,Home
West,2025-10,93000,60500,362,Home
West,2025-11,100000,64000,390,Home
West,2025-12,115000,72000,448,Home
Central,2025-01,65000,45000,250,Fashion
Central,2025-02,68000,47000,262,Fashion
Central,2025-03,62000,43000,240,Fashion
Central,2025-04,74000,49000,288,Fashion
Central,2025-05,79000,52000,308,Fashion
Central,2025-06,86000,56000,335,Fashion
Central,2025-07,76000,50000,295,Fashion
Central,2025-08,73000,49000,282,Fashion
Central,2025-09,78000,51500,302,Fashion
Central,2025-10,84000,54500,326,Fashion
Central,2025-11,91000,58000,353,Fashion
Central,2025-12,104000,65000,403,Fashion

请输出：
1. 一份完整的HTML分析报告（单个HTML文件），包含：
   - 数据总览表格
   - 各区域月度趋势图（使用Chart.js或Canvas）
   - 收入vs成本对比图
   - 关键发现和建议
2. 一份文字摘要（summary），包含：
   - 总收入、总成本、总利润
   - 最佳/最差区域
   - 季节性趋势
   - 增长率分析

技术约束：
- HTML报告为单个文件，可直接在浏览器打开
- 使用CDN引入Chart.js（不依赖本地文件）
- 文字摘要在HTML页面底部"""

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
    text, tokens, elapsed = call_llm(client, "你是一个资深数据分析师。请直接完成用户要求的数据分析任务。", TASK_PROMPT, model=cfg_local["model"])
    html = extract_html(text)
    result = {"condition": "A", "run": run_id, "tokens": tokens, "time": round(elapsed, 1), "html_length": len(html)}
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_condition_B(client, run_id, provider, cfg_local):
    d = Path(__file__).parent / provider / "condition_B" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    sp = "你是一个资深数据分析师。请根据用户要求改进分析报告，输出完整可运行的HTML文件。"
    rounds = [
        "请实现上述数据分析任务的基础版本，输出完整可运行的HTML报告。",
        "基于以下已有报告进行改进：增加更多图表类型，优化数据可视化。",
        "基于以下已有报告进行改进：增加同比/环比分析，优化排版。",
        "基于以下已有报告进行改进：增加异常值检测，改善交互体验。",
        "基于以下已有报告进行改进：增加预测趋势线，优化移动端适配。",
        "基于以下已有报告进行改进：完善所有分析维度，修复Bug。",
        "基于以下已有报告进行最终改进：确保所有功能正常，输出最终版本。",
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
    fd, t = step("frontend_dev", "前端实现", "frontend_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现前端UI和图表。只输出你负责的部分。"); total_tokens += t
    ip, t = step("image_processing_dev", "数据处理", "image_processing_dev", f"需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n请实现数据分析算法和统计计算。只输出你负责的部分。"); total_tokens += t
    tr, t = step("tester", "测试审查", "tester", f"前端代码：\n{cc(fd)}\n\n数据处理代码：\n{cc(ip)}\n\n请审查代码。", 2000); total_tokens += t
    fi_raw, t = step("coordinator", "最终整合", "coordinator",
        f"请整合为完整HTML报告：\n\n需求：\n{cc(rd)}\n\n架构：\n{cc(ad)}\n\n前端：\n{cc(fd)}\n\n数据处理：\n{cc(ip)}\n\n测试报告：\n{cc(tr)}\n\n任务：\n{TASK_PROMPT}\n\n直接输出HTML代码。", 8000); total_tokens += t

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
    _, t = step("image_processing_dev", "数据处理", "image_processing_dev"); total_tokens += t
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
        print(f"Task2 Data Analysis | Provider: {provider} | Run {run_id}/{NUM_RUNS}")
        print(f"{'='*60}")

        for cond, func in [("A", run_condition_A), ("B", run_condition_B), ("C", run_condition_C), ("D", run_condition_D)]:
            print(f"  Condition {cond}...", end=" ", flush=True)
            result = func(client, run_id, provider, cfg_local)
            all_results[cond].append(result)
            print(f"tokens={result['tokens']}, time={result['time']}s")

    out_dir = Path(__file__).parent / provider
    (out_dir / "all_runs.json").write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")

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

    from scipy import stats as sp_stats
    def do_t_test(a_vals, b_vals, label):
        t_stat, p_val = sp_stats.ttest_ind(a_vals, b_vals)
        return {"label": label, "t_stat": round(t_stat, 4), "p_value": round(p_val, 6), "significant_005": bool(p_val < 0.05)}

    t_tests = []
    t_tests.append(do_t_test(stats["C"]["values"], stats["B"]["values"], "C_vs_B"))
    t_tests.append(do_t_test(stats["C"]["values"], stats["D"]["values"], "C_vs_D"))

    summary = {
        "provider": provider,
        "model": cfg_local["model"],
        "task": "data_analysis",
        "timestamp": datetime.now().isoformat(),
        "num_runs": NUM_RUNS,
        "stats": stats,
        "t_tests": t_tests,
    }
    (out_dir / "stats_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Task2 Results for {provider}")
    print(f"{'='*60}")
    for cond in ["A", "B", "C", "D"]:
        s = stats[cond]
        print(f"  {cond}: mean={s['mean']:,.0f} std={s['std']:,.0f}")
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

    csv_lines = ["provider,condition,mean_tokens,std_tokens,min_tokens,max_tokens,n"]
    for p, s in all_summaries.items():
        for cond in ["A", "B", "C", "D"]:
            st = s["stats"][cond]
            csv_lines.append(f"{p},{cond},{st['mean']},{st['std']},{st['min']},{st['max']},{st['n']}")
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
