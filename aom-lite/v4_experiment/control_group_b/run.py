"""
V4 实验 - 对照组B：单Agent迭代（等预算）
==========================================
同一个Agent，最多7次API调用，Token总预算42,000。
模拟"一个聪明人反复打磨"的工作方式。

工作流程：
  第1次：生成初版贪吃蛇游戏
  第2次：自我审查，列出问题和改进点
  第3-6次：根据审查结果逐项改进
  第7次：最终整合和优化

用法：
    cd aom-lite/v4_experiment/control_group_b
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

MAX_CALLS = 7
TOKEN_BUDGET = 999999  # 不限制预算，跑满7轮

if not API_KEY:
    print("错误：请设置环境变量 OPENAI_API_KEY")
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

# ── 迭代Prompt ────────────────────────────────────────────────────────────────

PROMPT_ROUND1 = f"""你是一个全栈开发工程师。请完成以下开发任务：

{TASK_PROMPT}

要求：
- 直接输出完整的HTML代码
- 不要分段，不要解释，只要代码
- 代码必须完整、可直接运行
- 包含所有必要的HTML、CSS和JavaScript
- 追求高质量：模块化架构、精细的渲染效果、完善的移动端适配"""

PROMPT_REVIEW = """你是一个资深技术审查员。请仔细审查以下贪吃蛇游戏代码，从以下维度逐项评估：

1. **代码架构**：是否有清晰的模块划分？全局变量是否过多？
2. **渲染效果**：是否有网格线、食物高光、蛇头高光、结束动画等视觉效果？
3. **移动端适配**：是否有虚拟方向键？触屏滑动是否支持？WASD是否支持？
4. **功能完整度**：开始界面、计分、最高分记录（localStorage）、结束动画、重新开始是否都有？
5. **游戏循环**：是否使用requestAnimationFrame？速度机制是否合理？
6. **Bug检测**：是否有明显的逻辑错误或兼容性问题？

请输出：
### 问题清单（按严重程度排序）
| # | 维度 | 问题描述 | 严重程度 |
|---|------|---------|---------|
| 1 | ... | ... | 阻断/重要/建议 |

### 整体评价
一段话总结当前代码的质量水平。

### 代码
以下是待审查的代码：
"""

PROMPT_IMPROVE = """你是一个全栈开发工程师。你正在迭代改进一个贪吃蛇游戏。

**上一轮审查发现的问题：**
{review_result}

**当前版本的代码：**
```html
{current_code}
```

**要求：**
1. 修复审查报告中所有"阻断"和"重要"级别的问题
2. 尽量采纳"建议"级别的改进
3. 保持代码的完整性和可运行性
4. 输出完整的HTML代码，不要分段，不要解释
5. 如果某些问题已经修复，不需要再提"""

PROMPT_FINAL = """你是一个全栈开发工程师。这是贪吃蛇游戏的最终整合阶段。

**当前版本的代码：**
```html
{current_code}
```

**要求：**
1. 做最后的打磨和优化
2. 确保所有功能完整、UI美观、移动端适配良好
3. 消除所有冗余代码，确保结构清晰
4. 输出最终版本的完整HTML代码
5. 不要分段，不要解释，只要代码"""

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
    try:
        if "```html" in text:
            start = text.index("```html") + 7
            end = text.index("```", start) if "```" in text[start:] else len(text)
            return text[start:end].strip()
        if "```" in text:
            start = text.index("```") + 3
            nl = text.index("\n", start) if "\n" in text[start:] else start
            start = nl + 1
            end = text.index("```", start) if "```" in text[start:] else len(text)
            return text[start:end].strip()
    except (ValueError, IndexError):
        pass
    stripped = text.strip()
    if stripped.startswith("<!DOCTYPE") or stripped.startswith("<html"):
        return stripped
    idx = text.find("<")
    if idx >= 0:
        return text[idx:].strip()
    return text.strip()


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("V4 实验 - 对照组B：单Agent迭代（完整7轮）")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"API:  {BASE_URL}")
    print(f"最大调用次数: {MAX_CALLS}")
    print(f"Token预算: {TOKEN_BUDGET}")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    total_start = time.time()
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_details = []
    cumulative_tokens = 0
    current_code = ""
    review_result = ""

    # ── 第1次调用：生成初版 ───────────────────────────────────────────────────

    print(f"[1/{MAX_CALLS}] 生成初版...")
    text, tokens, elapsed = call_llm(client, "你是一个全栈开发工程师。", PROMPT_ROUND1, max_tokens=8000)
    cumulative_tokens += tokens
    current_code = extract_html(text)
    log_details.append({
        "round": 1, "phase": "生成初版", "tokens": tokens,
        "cumulative_tokens": cumulative_tokens,
        "time_seconds": round(elapsed, 1),
        "output_length": len(current_code),
    })
    print(f"    Token: {tokens} (累计: {cumulative_tokens}), 耗时: {elapsed:.1f}s, 代码: {len(current_code)}字符")

    if cumulative_tokens >= TOKEN_BUDGET:
        print("  Token预算已用完，停止迭代。")
    else:
        # ── 第2次调用：自我审查 ───────────────────────────────────────────────

        print(f"[2/{MAX_CALLS}] 自我审查...")
        review_prompt = PROMPT_REVIEW + "\n```html\n" + current_code + "\n```"
        text, tokens, elapsed = call_llm(client, "你是一个资深技术审查员。", review_prompt, max_tokens=3000)
        cumulative_tokens += tokens
        review_result = text
        log_details.append({
            "round": 2, "phase": "自我审查", "tokens": tokens,
            "cumulative_tokens": cumulative_tokens,
            "time_seconds": round(elapsed, 1),
            "output_length": len(text),
        })
        print(f"    Token: {tokens} (累计: {cumulative_tokens}), 耗时: {elapsed:.1f}s")

        # 保存审查报告
        (output_dir / "review_round2.md").write_text(review_result, encoding="utf-8")

    # ── 第3-6次调用：逐项改进 ─────────────────────────────────────────────────

    for round_num in range(3, 7):
        if cumulative_tokens >= TOKEN_BUDGET:
            print(f"  Token预算已用完（累计{cumulative_tokens}），停止迭代。")
            break

        if not review_result:
            print(f"  没有审查结果，跳过第{round_num}轮。")
            break

        print(f"[{round_num}/{MAX_CALLS}] 迭代改进...")
        improve_prompt = PROMPT_IMPROVE.format(
            review_result=review_result,
            current_code=current_code
        )
        text, tokens, elapsed = call_llm(client, "你是一个全栈开发工程师。", improve_prompt, max_tokens=8000)
        cumulative_tokens += tokens
        new_code = extract_html(text)

        if new_code and len(new_code) > 100:
            current_code = new_code

        log_details.append({
            "round": round_num, "phase": "迭代改进", "tokens": tokens,
            "cumulative_tokens": cumulative_tokens,
            "time_seconds": round(elapsed, 1),
            "output_length": len(current_code),
        })
        print(f"    Token: {tokens} (累计: {cumulative_tokens}), 耗时: {elapsed:.1f}s, 代码: {len(current_code)}字符")

        # 每次改进后做一次快速审查，为下一轮提供改进方向
        if round_num < 6 and cumulative_tokens < TOKEN_BUDGET:
            print(f"    快速审查...")
            quick_review_prompt = PROMPT_REVIEW + "\n```html\n" + current_code + "\n```"
            text, tokens, elapsed = call_llm(client, "你是一个资深技术审查员。", quick_review_prompt, max_tokens=2000)
            cumulative_tokens += tokens
            review_result = text
            log_details.append({
                "round": f"{round_num}b", "phase": "快速审查", "tokens": tokens,
                "cumulative_tokens": cumulative_tokens,
                "time_seconds": round(elapsed, 1),
                "output_length": len(text),
            })
            print(f"    Token: {tokens} (累计: {cumulative_tokens}), 耗时: {elapsed:.1f}s")

    # ── 第7次调用：最终整合 ───────────────────────────────────────────────────

    if cumulative_tokens < TOKEN_BUDGET and current_code:
        print(f"[{min(7, len(log_details)+1)}/{MAX_CALLS}] 最终整合...")
        final_prompt = PROMPT_FINAL.format(current_code=current_code)
        text, tokens, elapsed = call_llm(client, "你是一个全栈开发工程师。", final_prompt, max_tokens=8000)
        cumulative_tokens += tokens
        final_code = extract_html(text)
        if final_code and len(final_code) > 100:
            current_code = final_code
        log_details.append({
            "round": 7, "phase": "最终整合", "tokens": tokens,
            "cumulative_tokens": cumulative_tokens,
            "time_seconds": round(elapsed, 1),
            "output_length": len(current_code),
        })
        print(f"    Token: {tokens} (累计: {cumulative_tokens}), 耗时: {elapsed:.1f}s, 代码: {len(current_code)}字符")

    total_elapsed = time.time() - total_start

    # ── 保存产出 ──────────────────────────────────────────────────────────────

    if not current_code:
        print("错误：未生成有效代码")
        sys.exit(1)

    game_path = output_dir / "game.html"
    game_path.write_text(current_code, encoding="utf-8")
    print(f"\n游戏已保存: {game_path}")

    # 保存各轮产出
    artifacts_dir = output_dir / "iterations"
    artifacts_dir.mkdir(exist_ok=True)
    # 只保存最终版本
    (artifacts_dir / "final_code.html").write_text(current_code, encoding="utf-8")

    # 保存日志
    log = {
        "experiment": "V4 Control Group B",
        "condition": "single_agent_iterative",
        "model": MODEL,
        "timestamp": run_timestamp,
        "task": "贪吃蛇网页游戏",
        "max_calls": MAX_CALLS,
        "token_budget": TOKEN_BUDGET,
        "total_api_calls": len(log_details),
        "total_tokens": cumulative_tokens,
        "total_time_seconds": round(total_elapsed, 1),
        "html_length": len(current_code),
        "details": log_details,
    }
    log_path = output_dir / "experiment_log.json"
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 打印摘要 ──────────────────────────────────────────────────────────────

    print()
    print("=" * 60)
    print("对照组B实验完成")
    print("=" * 60)
    print(f"  总API调用次数: {len(log_details)}")
    print(f"  总Token消耗:   {cumulative_tokens} / {TOKEN_BUDGET} 预算")
    print(f"  总耗时:        {total_elapsed:.1f}秒")
    print(f"  HTML代码长度:  {len(current_code)} 字符")
    print(f"  输出文件:      {game_path}")
    print(f"  日志文件:      {log_path}")
    print()
    print("各轮消耗明细：")
    for d in log_details:
        print(f"  [第{d['round']}轮] {d['phase']:8s}: Token={d['tokens']:5d} (累计:{d['cumulative_tokens']:5d}), 耗时={d['time_seconds']:5.1f}s")
    print()
    print("请在浏览器中打开 output/game.html 查看效果。")


if __name__ == "__main__":
    main()
