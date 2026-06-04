"""
Condition E: Real-World Baseline (AutoGen/CrewAI-style)
========================================================
Simulates a typical multi-agent system with:
- Multiple agents (same 6 roles as OIMAC)
- Global shared context (every agent sees ALL previous outputs)
- No pipeline structure (free-for-all collaboration)
- No Context Controller

This represents the default architecture of frameworks like AutoGen, CrewAI, etc.
Usage: python run_condition_E.py [deepseek|mimo|all]
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

NUM_RUNS = 5  # Full statistical validation (matching V5.3)
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

def run_condition_E(client, run_id, provider, cfg_local):
    """
    Condition E: AutoGen/CrewAI-style multi-agent with global shared context.
    - 6 agents, sequential execution
    - Each agent sees ALL previous agents' full outputs (no filtering, no compression)
    - No pipeline structure, no Context Controller
    """
    d = Path(__file__).parent / provider / "condition_E" / f"run_{run_id}"
    d.mkdir(parents=True, exist_ok=True)
    total_tokens = 0
    start = time.time()

    # Global shared context - accumulates ALL outputs
    global_context = []

    roles = [
        ("coordinator", "任务分解", "coordinator", 2000),
        ("product_manager", "需求定义", "product_manager", 2000),
        ("architect", "架构设计", "architect", 2000),
        ("frontend_dev", "前端实现", "frontend_dev", 4000),
        ("image_processing_dev", "图像处理", "image_processing_dev", 4000),
        ("tester", "测试审查", "tester", 2000),
        ("coordinator", "最终整合", "coordinator", 8000),
    ]

    for i, (agent, phase, sp_name, max_tok) in enumerate(roles):
        sp = load_prompt(sp_name)

        # Build global shared context - ALL previous outputs, NO filtering
        if global_context:
            ctx_parts = []
            for j, (prev_agent, prev_phase, prev_output) in enumerate(global_context):
                ctx_parts.append(f"=== {prev_agent} ({prev_phase}) ===\n{prev_output}")
            full_ctx = "\n\n".join(ctx_parts)
            up = f"以下是所有前序角色的完整产出（请仔细阅读并基于此完成你的工作）：\n\n{full_ctx}\n\n原始任务：\n{TASK_PROMPT}\n\n请完成【{phase}】阶段的工作。"
        else:
            up = f"原始任务：\n{TASK_PROMPT}\n\n请完成【{phase}】阶段的工作。"

        text, tokens, _ = call_llm(client, sp, up, max_tokens=max_tok, model=cfg_local["model"])
        total_tokens += tokens
        global_context.append((agent, phase, text))
        print(f"    [{i+1}/7] {agent} ({phase}): tokens={tokens}, ctx={len(up):,} chars")

    elapsed = time.time() - start
    # Last output is the final integration
    html = extract_html(global_context[-1][2])

    result = {
        "condition": "E",
        "run": run_id,
        "tokens": total_tokens,
        "time": round(elapsed, 1),
        "html_length": len(html),
        "max_context_chars": max(len(o) for _, _, o in global_context),
    }
    (d / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "output.html").write_text(html, encoding="utf-8")
    return result

def run_model(provider):
    global cfg
    cfg_local = get_config(provider)
    cfg = cfg_local
    client = anthropic.Anthropic(api_key=cfg_local["api_key"], base_url=cfg_local["base_url"])
    all_results = {"E": []}

    for run_id in range(1, NUM_RUNS + 1):
        print(f"\n{'='*60}")
        print(f"Provider: {provider} | Condition E | Run {run_id}/{NUM_RUNS}")
        print(f"{'='*60}")

        result = run_condition_E(client, run_id, provider, cfg_local)
        all_results["E"].append(result)
        print(f"  Total tokens={result['tokens']}, time={result['time']}s")

    # Save raw results
    out_dir = Path(__file__).parent / provider
    (out_dir / "condition_E_runs.json").write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")

    # Compute stats
    tokens_list = [r["tokens"] for r in all_results["E"]]
    stats = {
        "mean": round(statistics.mean(tokens_list), 1),
        "std": round(statistics.stdev(tokens_list), 1) if len(tokens_list) > 1 else 0,
        "min": min(tokens_list),
        "max": max(tokens_list),
        "n": len(tokens_list),
        "values": tokens_list,
    }

    print(f"\n{'='*60}")
    print(f"Condition E Results for {provider} ({cfg_local['model']})")
    print(f"{'='*60}")
    print(f"  E: mean={stats['mean']:,.0f} std={stats['std']:,.0f} min={stats['min']:,} max={stats['max']:,}")

    return {"stats": stats, "results": all_results}

def main():
    if PROVIDER == "all":
        providers = ["deepseek", "mimo"]
    else:
        providers = [PROVIDER]

    all_summaries = {}
    for p in providers:
        all_summaries[p] = run_model(p)

    # Print comparison with existing data
    print(f"\n{'='*60}")
    print("Comparison with existing conditions (from stats_summary.json)")
    print(f"{'='*60}")

    existing_path = Path(__file__).parent / "stats_summary.json"
    if existing_path.exists():
        existing = json.loads(existing_path.read_text(encoding="utf-8"))
        for p in providers:
            if p in existing:
                print(f"\n{p}:")
                for cond in ["A", "B", "C", "D"]:
                    s = existing[p]["stats"][cond]
                    print(f"  {cond}: mean={s['mean']:,.0f}")
                e_mean = all_summaries[p]["stats"]["mean"]
                print(f"  E: mean={e_mean:,.0f} (NEW)")
                if "B" in existing[p]["stats"]:
                    b_mean = existing[p]["stats"]["B"]["mean"]
                    print(f"  E/B ratio: {b_mean/e_mean:.2f}x")

    # Save summary
    summary = {
        "condition": "E",
        "description": "AutoGen/CrewAI-style multi-agent with global shared context",
        "timestamp": datetime.now().isoformat(),
        "num_runs": NUM_RUNS,
        "providers": {p: all_summaries[p]["stats"] for p in providers},
    }
    out_path = Path(__file__).parent / "condition_E_summary.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSummary saved to {out_path}")

if __name__ == "__main__":
    main()
