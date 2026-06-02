"""
V4 实验 - 实验组：有组织管理的多Agent协作
============================================
模拟AOM框架下的协作方式：
- 6个Agent按组织职能分工（产品经理、架构师、前端开发、游戏逻辑开发、测试、协调者）
- 明确的汇报关系（科层制）
- 结构化的协作流程（需求→设计→并行开发→测试→整合）

用法：
    cd aom-lite/v4_experiment/experimental_group
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

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# ── 配置 ──────────────────────────────────────────────────────────────────────

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")

if not API_KEY:
    print("错误：请设置环境变量 OPENAI_API_KEY")
    print("  export OPENAI_API_KEY=your_key")
    sys.exit(1)

# ── 任务描述 ──────────────────────────────────────────────────────────────────

TASK_PROMPT = """请制作一个贪吃蛇网页游戏，要求：

1. 外观美观，UI设计有现代感
2. 包含开始界面、游戏界面和结束界面
3. 有计分系统
4. 蛇的移动速度适中，操控流畅
5. 支持键盘方向键操控
6. 游戏结束后显示得分，并提供重新开始按钮
7. 适配桌面端和移动端
8. 代码为单个HTML文件，包含CSS和JS，可直接在浏览器中打开"""

# ── Prompt加载 ────────────────────────────────────────────────────────────────

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name):
    """加载角色prompt文件"""
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.exists():
        print(f"错误：找不到prompt文件 {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


# ── API调用 ───────────────────────────────────────────────────────────────────

def call_llm(client, system_prompt, user_prompt, max_tokens=8000):
    """调用LLM，返回 (输出文本, token消耗, 耗时秒数)"""
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
    """从LLM输出中提取HTML代码"""
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


# ── 协作流程 ──────────────────────────────────────────────────────────────────

def step_coordinator_decompose(client, log_details):
    """步骤1：协调者分解任务"""
    print("[1/7] 协调者：分解任务...")
    system_prompt = load_prompt("coordinator")
    user_prompt = f"以下是开发任务，请进行任务分解：\n\n{TASK_PROMPT}"

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 1, "agent": "coordinator", "phase": "任务分解",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_product_manager(client, task_decomposition, log_details):
    """步骤2：产品经理定义需求"""
    print("[2/7] 产品经理：定义需求...")
    system_prompt = load_prompt("product_manager")
    user_prompt = (
        f"协调者已将任务分解如下：\n\n{task_decomposition}\n\n"
        f"原始任务描述：\n{TASK_PROMPT}\n\n"
        f"请根据以上信息，输出结构化的产品需求文档。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 2, "agent": "product_manager", "phase": "需求定义",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_architect(client, requirements_doc, log_details):
    """步骤3：架构师设计技术方案"""
    print("[3/7] 架构师：设计技术架构...")
    system_prompt = load_prompt("architect")
    user_prompt = (
        f"产品经理的需求文档如下：\n\n{requirements_doc}\n\n"
        f"请根据需求文档，输出技术架构设计。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 3, "agent": "architect", "phase": "架构设计",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_frontend_dev(client, requirements_doc, arch_doc, log_details):
    """步骤4a：前端开发实现界面"""
    print("[4/7] 前端开发：实现界面...")
    system_prompt = load_prompt("frontend_dev")
    user_prompt = (
        f"产品经理的需求文档：\n\n{requirements_doc}\n\n"
        f"架构师的技术设计：\n\n{arch_doc}\n\n"
        f"请实现前端界面部分的代码。只输出你负责的代码，不要输出游戏逻辑。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=4000)
    log_details.append({
        "step": 4, "agent": "frontend_dev", "phase": "前端实现",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_game_logic_dev(client, requirements_doc, arch_doc, log_details):
    """步骤4b：游戏逻辑开发实现核心逻辑"""
    print("[5/7] 游戏逻辑开发：实现核心逻辑...")
    system_prompt = load_prompt("backend_dev")
    user_prompt = (
        f"产品经理的需求文档：\n\n{requirements_doc}\n\n"
        f"架构师的技术设计：\n\n{arch_doc}\n\n"
        f"请实现游戏核心逻辑部分的代码。只输出你负责的代码，不要输出HTML结构和CSS样式。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=4000)
    log_details.append({
        "step": 5, "agent": "game_logic_dev", "phase": "游戏逻辑实现",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_tester(client, frontend_code, logic_code, requirements_doc, log_details):
    """步骤5：测试审查代码"""
    print("[6/7] 测试：审查代码...")
    system_prompt = load_prompt("tester")
    user_prompt = (
        f"产品经理的验收标准：\n\n{requirements_doc}\n\n"
        f"前端开发的产出：\n\n{frontend_code}\n\n"
        f"游戏逻辑开发的产出：\n\n{logic_code}\n\n"
        f"请对以上代码进行全面测试审查，输出测试报告。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=2000)
    log_details.append({
        "step": 6, "agent": "tester", "phase": "测试审查",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


def step_coordinator_integrate(
    client, requirements_doc, arch_doc, frontend_code, logic_code, test_report, log_details
):
    """步骤6：协调者整合最终产出"""
    print("[7/7] 协调者：整合最终产出...")
    system_prompt = load_prompt("coordinator")
    user_prompt = (
        f"所有角色已完成各自工作。请整合以下产出为一个完整的HTML文件。\n\n"
        f"=== 产品经理的需求文档 ===\n{requirements_doc}\n\n"
        f"=== 架构师的技术设计 ===\n{arch_doc}\n\n"
        f"=== 前端开发的代码 ===\n{frontend_code}\n\n"
        f"=== 游戏逻辑开发的代码 ===\n{logic_code}\n\n"
        f"=== 测试报告 ===\n{test_report}\n\n"
        f"请整合以上所有产出，输出一个完整的、可直接在浏览器中运行的HTML文件。\n"
        f"修复测试报告中发现的阻断性问题。\n"
        f"直接输出HTML代码，不要任何解释。"
    )

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=8000)
    log_details.append({
        "step": 7, "agent": "coordinator", "phase": "最终整合",
        "tokens": tokens, "time_seconds": round(elapsed, 1),
        "output_length": len(text),
        "summary": text[:200] + "..." if len(text) > 200 else text,
    })
    print(f"    Token: {tokens}, 耗时: {elapsed:.1f}s, 输出: {len(text)}字符")
    return text


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("V4 实验 - 实验组：有组织管理的多Agent协作")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"API:  {BASE_URL}")
    print(f"组织结构: 6角色科层制（协调者→PM/架构师→前端/游戏逻辑→测试）")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 确保输出目录存在
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # 记录开始时间
    total_start = time.time()
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_details = []

    # ── 协作流程 ──────────────────────────────────────────────────────────────

    # 步骤1：协调者分解任务
    task_decomposition = step_coordinator_decompose(client, log_details)

    # 步骤2：产品经理定义需求
    requirements_doc = step_product_manager(client, task_decomposition, log_details)

    # 步骤3：架构师设计技术方案
    arch_doc = step_architect(client, requirements_doc, log_details)

    # 步骤4&5：前端开发和游戏逻辑开发并行实现
    # 注意：由于是串行API调用，这里依次调用，但逻辑上是并行的
    frontend_code = step_frontend_dev(client, requirements_doc, arch_doc, log_details)
    logic_code = step_game_logic_dev(client, requirements_doc, arch_doc, log_details)

    # 步骤6：测试审查
    test_report = step_tester(client, frontend_code, logic_code, requirements_doc, log_details)

    # 步骤7：协调者整合
    final_html_raw = step_coordinator_integrate(
        client, requirements_doc, arch_doc, frontend_code, logic_code, test_report, log_details
    )

    total_elapsed = time.time() - total_start

    # ── 保存产出 ──────────────────────────────────────────────────────────────

    if not final_html_raw:
        print("错误：协调者未返回有效内容")
        sys.exit(1)

    # 提取并保存HTML
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

    # 计算汇总数据
    total_tokens = sum(d["tokens"] for d in log_details)
    total_api_calls = len(log_details)

    # 保存日志
    log = {
        "experiment": "V4 Experimental Group",
        "condition": "multi_agent_with_organization",
        "model": MODEL,
        "timestamp": run_timestamp,
        "task": "贪吃蛇网页游戏",
        "organization": {
            "structure": "科层制（Hierarchical）",
            "roles": ["协调者", "产品经理", "架构师", "前端开发", "游戏逻辑开发", "测试"],
            "reporting_lines": "协调者→{产品经理,架构师,前端开发,游戏逻辑开发,测试}",
            "collaboration_flow": "需求→设计→并行开发→测试→整合",
        },
        "total_api_calls": total_api_calls,
        "total_tokens": total_tokens,
        "total_time_seconds": round(total_elapsed, 1),
        "html_length": len(html_code),
        "details": log_details,
    }
    log_path = output_dir / "experiment_log.json"
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 打印摘要 ──────────────────────────────────────────────────────────────

    print()
    print("=" * 60)
    print("实验组实验完成")
    print("=" * 60)
    print(f"  总API调用次数: {total_api_calls}")
    print(f"  总Token消耗:   {total_tokens}")
    print(f"  总耗时:        {total_elapsed:.1f}秒")
    print(f"  HTML代码长度:  {len(html_code)} 字符")
    print(f"  输出文件:      {game_path}")
    print(f"  各阶段产出:    {artifacts_dir}/")
    print(f"  日志文件:      {log_path}")
    print()
    print("各Agent消耗明细：")
    for d in log_details:
        print(f"  [{d['step']}] {d['agent']:20s} ({d['phase']:8s}): "
              f"Token={d['tokens']:5d}, 耗时={d['time_seconds']:5.1f}s")
    print()
    print("请在浏览器中打开 output/game.html 查看效果。")
    print("各阶段的中间产出保存在 output/artifacts/ 目录下。")


if __name__ == "__main__":
    main()
