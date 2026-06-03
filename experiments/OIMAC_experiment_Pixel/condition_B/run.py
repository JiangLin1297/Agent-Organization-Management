"""
条件B：迭代架构（CAE条件）
==========================
结构：1个Agent，7轮迭代，每轮输入包含所有历史输出
"""
import json, os, sys, time
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("请先安装 openai: pip install openai")
    sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")

if not API_KEY:
    print("错误：请设置环境变量 OPENAI_API_KEY")
    sys.exit(1)

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

ROUND_PROMPTS = [
    "请实现上述任务的基础版本，输出完整可运行的HTML文件。",
    "基于以下已有代码进行改进：\n- 提升图像处理质量\n- 优化颜色量化算法\n- 改善UI美观度",
    "基于以下已有代码进行改进：\n- 优化拼豆网格渲染\n- 增加颜色统计的准确性\n- 改善交互体验",
    "基于以下已有代码进行改进：\n- 提升降色效果（使用更好的量化算法）\n- 增加网格大小选项\n- 优化移动端适配",
    "基于以下已有代码进行改进：\n- 增加放大/缩小功能\n- 优化Canvas渲染性能\n- 改善颜色显示效果",
    "基于以下已有代码进行改进：\n- 完善所有功能\n- 修复可能的Bug\n- 优化代码结构",
    "基于以下已有代码进行最终改进：\n- 确保所有功能正常运行\n- 优化用户体验\n- 输出最终版本",
]

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
            temperature=0.3,
            timeout=300.0,
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
    return text.strip()

def main():
    print("=" * 60)
    print("条件B：迭代架构（CAE条件）")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"迭代轮次: 7")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    system_prompt = "你是一个资深全栈开发者。请根据用户要求改进代码，输出完整可运行的HTML文件。"
    history_outputs = []
    context_log = []
    details = []
    total_start = time.time()

    for round_num in range(7):
        print(f"[Round {round_num+1}/7] ", end="")

        # Build context: full history accumulation (CAE condition)
        if round_num == 0:
            user_prompt = f"任务描述：\n{TASK_PROMPT}\n\n{ROUND_PROMPTS[round_num]}"
        else:
            # ★ CAE核心：拼接所有历史输出（不做删减）
            history_text = "\n\n".join([
                f"=== 第{i+1}轮输出 ===\n{out}" for i, out in enumerate(history_outputs)
            ])
            user_prompt = (
                f"任务描述：\n{TASK_PROMPT}\n\n"
                f"历史输出（共{len(history_outputs)}轮）：\n{history_text}\n\n"
                f"{ROUND_PROMPTS[round_num]}"
            )

        context_len = len(user_prompt)
        text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=8000)

        history_outputs.append(text)
        context_log.append({"round": round_num + 1, "context_length": context_len})
        details.append({
            "round": round_num + 1, "tokens": tokens,
            "time_seconds": round(elapsed, 1),
            "output_length": len(text), "context_length": context_len
        })

        print(f"Token={tokens}, 上下文={context_len:,}字符, 输出={len(text)}字符")

    total_time = time.time() - total_start

    # Save final output
    final_html = extract_html(history_outputs[-1])
    (output_dir / "index.html").write_text(final_html, encoding="utf-8")

    total_tokens = sum(d["tokens"] for d in details)
    max_context = max(d["context_length"] for d in details)

    # Save logs
    log = {
        "experiment": "Perler Bead Pattern Generator - Condition B",
        "condition": "iterative_self_refinement",
        "model": MODEL,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "total_tokens": total_tokens,
        "api_calls": 7,
        "total_time_seconds": round(total_time, 1),
        "output_length": len(final_html),
        "max_context_size": max_context,
        "context_growth": context_log,
        "details": details
    }
    (logs_dir / "token_usage.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # Context growth log
    with open(logs_dir / "context_growth.txt", "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n条件B Context Growth Log（验证CAE）\n" + "=" * 60 + "\n\n")
        for entry in context_log:
            f.write(f"Round {entry['round']}: 上下文 = {entry['context_length']:>10,} 字符\n")
        f.write(f"\n最大上下文: {max_context:,} 字符\n")
        f.write(f"总Token: {total_tokens:,}\n")
        f.write("\n增长分析:\n")
        for i in range(1, len(context_log)):
            prev = context_log[i-1]["context_length"]
            curr = context_log[i]["context_length"]
            ratio = curr / prev if prev > 0 else float("inf")
            f.write(f"  Round {i}→{i+1}: {prev:>10,} → {curr:>10,} ({ratio:.2f}x)\n")

    print(f"\n完成! 总Token={total_tokens}, 最大上下文={max_context:,}, 耗时={total_time:.1f}s")

if __name__ == "__main__":
    main()
