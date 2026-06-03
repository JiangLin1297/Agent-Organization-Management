"""
V4 消融实验 - 条件D：有组织但无Context Controller
==================================================
目的：验证Context Controller是否为因果变量（causal factor）

与条件C的唯一差异：
  条件C（有Controller）：每个Agent只接收 task_spec + 直接依赖输出 + 接口级信息
  条件D（无Controller）：每个Agent接收 ALL前序Agent的完整原始输出

即：context_D(role_i) = concat(all_outputs_of_roles_before_i)
而非：context_C(role_i) = local_deps + interface_only

严格禁止：摘要、截断、过滤、压缩

用法：
    cd aom-lite/v4_experiment/condition_d
    python run.py

环境变量：
    OPENAI_API_KEY   - API密钥
    OPENAI_BASE_URL  - API地址（默认 https://token-plan-cn.xiaomimimo.com/v1）
    LLM_MODEL        - 模型名（默认 mimo-v2.5-pro）
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("请先安装 openai: pip install openai")
    sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

# ── 配置 ──────────────────────────────────────────────────────────────────────

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")

if not API_KEY:
    print("错误：请设置环境变量 OPENAI_API_KEY")
    print("  export OPENAI_API_KEY=your_key")
    sys.exit(1)

# ── 任务描述（与条件C完全一致） ────────────────────────────────────────────────

TASK_PROMPT = """请制作一个贪吃蛇网页游戏，要求：

1. 外观美观，UI设计有现代感
2. 包含开始界面、游戏界面和结束界面
3. 有计分系统
4. 蛇的移动速度适中，操控流畅
5. 支持键盘方向键操控
6. 游戏结束后显示得分，并提供重新开始按钮
7. 适配桌面端和移动端
8. 代码为单个HTML文件，包含CSS和JS，可直接在浏览器中打开"""

# ── Prompt加载（与条件C完全一致） ──────────────────────────────────────────────

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name):
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.exists():
        print(f"错误：找不到prompt文件 {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


# ── API调用（与条件C完全一致） ────────────────────────────────────────────────

def call_llm(client, system_prompt, user_prompt, max_tokens=8000):
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            timeout=180.0,
        )
        elapsed = time.time() - start
        text = resp.choices[0].message.content or ""
        tokens = resp.usage.total_tokens if resp.usage else 0
        return text, tokens, elapsed
    except Exception as e:
        elapsed = time.time() - start
        print(f"    API调用失败: {e}")
        return "", 0, elapsed


def extract_html(text):
    if "```html" in text:
        start = text.index("```html") + 7
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        nl = text.index("\n", start)
        start = nl + 1
        end = text.index("```", start)
        return text[start:end].strip()
    stripped = text.strip()
    if stripped.startswith("<!DOCTYPE") or stripped.startswith("<html"):
        return stripped
    idx = text.find("<")
    if idx >= 0:
        return text[idx:].strip()
    return text.strip()


# ── Context Builder：无过滤的全量上下文累积 ───────────────────────────────────

def build_full_context(outputs_so_far, extra_label=""):
    """
    将所有前序Agent的完整原始输出拼接为一个上下文字符串。
    关键约束：不做摘要、不做截断、不做过滤、不压缩。
    """
    if not outputs_so_far:
        return ""
    sections = []
    for label, output in outputs_so_far:
        sections.append(f"=== {label} ===\n{output}\n")
    return "\n".join(sections)


# ── 协作流程（与条件C相同pipeline，唯一差异：上下文构造方式） ────────────────────

def step_coordinator_decompose(client, log_details, context_log):
    """步骤1：协调者分解任务（与条件C一致——此步无前序输出）"""
    print("[1/7] 协调者：分解任务...")
    system_prompt = load_prompt("coordinator")
    user_prompt = f"以下是开发任务，请进行任务分解：\n\n{TASK_PROMPT}"
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 1, "agent": "coordinator", "phase": "任务分解",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 1, "agent": "coordinator", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_product_manager(client, task_decomposition, log_details, context_log):
    """步骤2：产品经理定义需求（与条件C一致——接收协调者输出+原始任务）"""
    print("[2/7] 产品经理：定义需求...")
    system_prompt = load_prompt("product_manager")
    user_prompt = (
        f"协调者已将任务分解如下：\n\n{task_decomposition}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请根据以上信息，输出结构化的产品需求文档。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 2, "agent": "product_manager", "phase": "需求定义",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 2, "agent": "product_manager", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_architect(client, task_decomposition, requirements_doc, log_details, context_log):
    """
    步骤3：架构师设计技术方案
    条件C：只接收 requirements_doc
    条件D：接收 task_decomposition + requirements_doc + TASK_PROMPT（全量累积）
    """
    print("[3/7] 架构师：设计技术架构...")
    system_prompt = load_prompt("architect")

    # ★ 条件D核心差异：全量上下文累积
    all_outputs = [
        ("协调者-任务分解", task_decomposition),
        ("产品经理-需求文档", requirements_doc),
    ]
    full_context = build_full_context(all_outputs)
    user_prompt = (
        f"以下是所有前序角色的完整产出：\n\n{full_context}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请根据以上所有信息，输出技术架构设计。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 3, "agent": "architect", "phase": "架构设计",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 3, "agent": "architect", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_frontend_dev(client, task_decomposition, requirements_doc, arch_doc, log_details, context_log):
    """
    步骤4：前端开发实现界面
    条件C：只接收 requirements_doc + arch_doc
    条件D：接收 task_decomposition + requirements_doc + arch_doc + TASK_PROMPT（全量累积）
    """
    print("[4/7] 前端开发：实现界面...")
    system_prompt = load_prompt("frontend_dev")

    # ★ 条件D核心差异：全量上下文累积
    all_outputs = [
        ("协调者-任务分解", task_decomposition),
        ("产品经理-需求文档", requirements_doc),
        ("架构师-技术设计", arch_doc),
    ]
    full_context = build_full_context(all_outputs)
    user_prompt = (
        f"以下是所有前序角色的完整产出：\n\n{full_context}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请实现前端界面部分的代码。只输出你负责的代码，不要输出游戏逻辑。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=4000)
    log_details.append({
        "step": 4, "agent": "frontend_dev", "phase": "前端实现",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 4, "agent": "frontend_dev", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_game_logic_dev(client, task_decomposition, requirements_doc, arch_doc, frontend_code, log_details, context_log):
    """
    步骤5：游戏逻辑开发实现核心逻辑
    条件C：只接收 requirements_doc + arch_doc
    条件D：接收 task_decomposition + requirements_doc + arch_doc + frontend_code + TASK_PROMPT（全量累积）
    """
    print("[5/7] 游戏逻辑开发：实现核心逻辑...")
    system_prompt = load_prompt("backend_dev")

    # ★ 条件D核心差异：全量上下文累积
    all_outputs = [
        ("协调者-任务分解", task_decomposition),
        ("产品经理-需求文档", requirements_doc),
        ("架构师-技术设计", arch_doc),
        ("前端开发-界面代码", frontend_code),
    ]
    full_context = build_full_context(all_outputs)
    user_prompt = (
        f"以下是所有前序角色的完整产出：\n\n{full_context}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请实现游戏核心逻辑部分的代码。只输出你负责的代码，不要输出HTML结构和CSS样式。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=4000)
    log_details.append({
        "step": 5, "agent": "game_logic_dev", "phase": "游戏逻辑实现",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 5, "agent": "game_logic_dev", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_tester(client, task_decomposition, requirements_doc, arch_doc, frontend_code, logic_code, log_details, context_log):
    """
    步骤6：测试审查代码
    条件C：只接收 requirements_doc + frontend_code + logic_code
    条件D：接收 task_decomposition + requirements_doc + arch_doc + frontend_code + logic_code + TASK_PROMPT（全量累积）
    """
    print("[6/7] 测试：审查代码...")
    system_prompt = load_prompt("tester")

    # ★ 条件D核心差异：全量上下文累积
    all_outputs = [
        ("协调者-任务分解", task_decomposition),
        ("产品经理-需求文档", requirements_doc),
        ("架构师-技术设计", arch_doc),
        ("前端开发-界面代码", frontend_code),
        ("游戏逻辑开发-核心逻辑", logic_code),
    ]
    full_context = build_full_context(all_outputs)
    user_prompt = (
        f"以下是所有前序角色的完整产出：\n\n{full_context}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请对以上代码进行全面测试审查，输出测试报告。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 6, "agent": "tester", "phase": "测试审查",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 6, "agent": "tester", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


def step_coordinator_integrate(
    client, task_decomposition, requirements_doc, arch_doc, frontend_code, logic_code, test_report,
    log_details, context_log
):
    """
    步骤7：协调者整合最终产出
    条件C：接收 requirements_doc + arch_doc + frontend_code + logic_code + test_report
    条件D：接收 task_decomposition + requirements_doc + arch_doc + frontend_code + logic_code + test_report + TASK_PROMPT（全量累积）
    """
    print("[7/7] 协调者：整合最终产出...")
    system_prompt = load_prompt("coordinator")

    # ★ 条件D核心差异：全量上下文累积
    all_outputs = [
        ("协调者-任务分解", task_decomposition),
        ("产品经理-需求文档", requirements_doc),
        ("架构师-技术设计", arch_doc),
        ("前端开发-界面代码", frontend_code),
        ("游戏逻辑开发-核心逻辑", logic_code),
        ("测试-测试报告", test_report),
    ]
    full_context = build_full_context(all_outputs)
    user_prompt = (
        f"所有角色已完成各自工作。以下是所有前序角色的完整产出：\n\n{full_context}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请整合以上所有产出，输出一个完整的、可直接在浏览器中运行的HTML文件。\n"
        f"修复测试报告中发现的阻断性问题。\n"
        f"直接输出HTML代码，不要任何解释。"
    )
    context_len = len(user_prompt)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=8000)
    log_details.append({
        "step": 7, "agent": "coordinator", "phase": "最终整合",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text), "context_length": context_len,
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    context_log.append({"step": 7, "agent": "coordinator", "context_length": context_len})
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符, 上下文: {context_len}字符")
    return text


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("V4 消融实验 - 条件D：有组织但无Context Controller")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"API:  {BASE_URL}")
    print(f"组织结构: 6角色科层制（与条件C完全一致）")
    print(f"唯一差异: 全量上下文累积（无过滤/摘要/截断）")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    total_start = time.time()
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_details = []
    context_log = []

    # ── 协作流程（pipeline顺序与条件C完全一致） ──────────────────────────────

    # 步骤1：协调者分解任务
    task_decomposition = step_coordinator_decompose(client, log_details, context_log)

    # 步骤2：产品经理定义需求
    requirements_doc = step_product_manager(client, task_decomposition, log_details, context_log)

    # 步骤3：架构师设计技术方案（★ 差异开始：接收全量前序输出）
    arch_doc = step_architect(client, task_decomposition, requirements_doc, log_details, context_log)

    # 步骤4&5：前端开发和游戏逻辑开发（★ 差异：各自接收所有前序输出）
    frontend_code = step_frontend_dev(
        client, task_decomposition, requirements_doc, arch_doc, log_details, context_log
    )
    logic_code = step_game_logic_dev(
        client, task_decomposition, requirements_doc, arch_doc, frontend_code, log_details, context_log
    )

    # 步骤6：测试审查（★ 差异：接收所有前序输出）
    test_report = step_tester(
        client, task_decomposition, requirements_doc, arch_doc, frontend_code, logic_code,
        log_details, context_log
    )

    # 步骤7：协调者整合（★ 差异：接收所有前序输出）
    final_html_raw = step_coordinator_integrate(
        client, task_decomposition, requirements_doc, arch_doc, frontend_code, logic_code, test_report,
        log_details, context_log
    )

    total_elapsed = time.time() - total_start

    # ── 保存产出 ──────────────────────────────────────────────────────────────

    if not final_html_raw:
        print("错误：协调者未返回有效内容")
        sys.exit(1)

    html_code = extract_html(final_html_raw)
    game_path = output_dir / "game.html"
    game_path.write_text(html_code, encoding="utf-8")
    print(f"\n游戏已保存: {game_path}")

    # 保存各角色产出
    artifacts_dir = output_dir / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    (artifacts_dir / "01_task_decomposition.md").write_text(task_decomposition, encoding="utf-8")
    (artifacts_dir / "02_requirements.md").write_text(requirements_doc, encoding="utf-8")
    (artifacts_dir / "03_architecture.md").write_text(arch_doc, encoding="utf-8")
    (artifacts_dir / "04_frontend_code.html").write_text(frontend_code, encoding="utf-8")
    (artifacts_dir / "05_game_logic.html").write_text(logic_code, encoding="utf-8")
    (artifacts_dir / "06_test_report.md").write_text(test_report, encoding="utf-8")
    (artifacts_dir / "07_raw_final.html").write_text(final_html_raw, encoding="utf-8")

    # ── 汇总数据 ──────────────────────────────────────────────────────────────

    total_tokens = sum(d["tokens"] for d in log_details)
    total_api_calls = len(log_details)
    max_context_size = max(d["context_length"] for d in log_details)

    # ── 保存experiment_log.json ───────────────────────────────────────────────

    log = {
        "experiment": "V4 Ablation Study - Condition D",
        "condition": "multi_agent_organization_no_context_controller",
        "description": "有组织管理但无Context Controller：每个Agent接收所有前序Agent的完整原始输出",
        "ablation_variable": "上下文传递结构（Context Passing Strategy）",
        "diff_from_condition_c": "condition_c使用filtered context（仅直接依赖），condition_d使用full raw context（所有前序输出）",
        "model": MODEL,
        "timestamp": run_timestamp,
        "task": "贪吃蛇网页游戏",
        "organization": {
            "structure": "科层制（Hierarchical）",
            "roles": ["协调者", "产品经理", "架构师", "前端开发", "游戏逻辑开发", "测试"],
            "reporting_lines": "协调者→{产品经理,架构师,前端开发,游戏逻辑开发,测试}",
            "collaboration_flow": "需求→设计→并行开发→测试→整合",
            "note": "组织结构与条件C完全一致，唯一差异是上下文传递方式"
        },
        "total_api_calls": total_api_calls,
        "total_tokens": total_tokens,
        "total_time_seconds": round(total_elapsed, 1),
        "html_length": len(html_code),
        "max_context_size": max_context_size,
        "context_growth": context_log,
        "details": log_details,
    }
    log_path = logs_dir / "experiment_log.json"
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 保存context_growth.txt ────────────────────────────────────────────────

    ctx_path = logs_dir / "context_growth.txt"
    with open(ctx_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("条件D Context Growth Log（验证CAE）\n")
        f.write("=" * 60 + "\n")
        f.write(f"实验时间: {run_timestamp}\n")
        f.write(f"模型: {MODEL}\n")
        f.write(f"唯一变量: 上下文传递结构（全量累积 vs 过滤传递）\n")
        f.write("-" * 60 + "\n\n")
        for entry in context_log:
            f.write(f"Step {entry['step']} [{entry['agent']:20s}]: 上下文长度 = {entry['context_length']:>8,} 字符\n")
        f.write(f"\n{'=' * 60}\n")
        f.write(f"最大上下文长度: {max_context_size:,} 字符\n")
        f.write(f"总Token消耗: {total_tokens:,}\n")
        f.write(f"\n{'=' * 60}\n")
        f.write("Context Growth Analysis:\n")
        f.write("-" * 60 + "\n")
        for i in range(1, len(context_log)):
            prev = context_log[i - 1]["context_length"]
            curr = context_log[i]["context_length"]
            growth = curr - prev
            ratio = curr / prev if prev > 0 else float("inf")
            f.write(
                f"  Step {context_log[i-1]['step']}→{context_log[i]['step']}: "
                f"{prev:>8,} → {curr:>8,}  "
                f"(+{growth:>8,}, {ratio:.2f}x)\n"
            )

    # ── 打印摘要 ──────────────────────────────────────────────────────────────

    print()
    print("=" * 60)
    print("条件D实验完成")
    print("=" * 60)
    print(f"  总API调用次数: {total_api_calls}")
    print(f"  总Token消耗:   {total_tokens}")
    print(f"  总耗时:        {total_elapsed:.1f}秒")
    print(f"  HTML代码长度:  {len(html_code)} 字符")
    print(f"  最大上下文:    {max_context_size:,} 字符")
    print(f"  输出文件:      {game_path}")
    print(f"  各阶段产出:    {artifacts_dir}/")
    print(f"  日志文件:      {log_path}")
    print(f"  Context日志:   {ctx_path}")
    print()
    print("各Agent消耗明细：")
    for d in log_details:
        print(f"  [{d['step']}] {d['agent']:20s} ({d['phase']:8s}): "
              f"Token={d['tokens']:5d}, 上下文={d['context_length']:>8,}字符, 耗时={d['time_seconds']:5.1f}s")
    print()

    # ── 与条件C对比 ────────────────────────────────────────────────────────────

    condition_c_tokens = 42166
    ratio = total_tokens / condition_c_tokens
    print("=" * 60)
    print("消融实验对比分析")
    print("=" * 60)
    print(f"  条件C（有Context Controller）:  {condition_c_tokens:>8,} tokens")
    print(f"  条件D（无Context Controller）:  {total_tokens:>8,} tokens")
    print(f"  Token倍率 (D/C):               {ratio:>8.2f}x")
    print()

    if 1.3 <= ratio <= 1.7:
        print("  结论: 支持CAE + Context Controller因果作用（中等效应）")
        print("  → Context Controller的存在确实减少了Token消耗，但非唯一决定因素")
    elif ratio > 1.7:
        print("  结论: Context Controller是主要决定因素（强因果）")
        print("  → 无Controller时Token消耗显著增加，接近迭代模式")
    else:
        print("  结论: CAE机制或Controller假设需要修正")
        print("  → Token差异不显著，Context Controller可能非因果变量")

    print()
    print("请在浏览器中打开 output/game.html 查看效果。")


if __name__ == "__main__":
    main()
