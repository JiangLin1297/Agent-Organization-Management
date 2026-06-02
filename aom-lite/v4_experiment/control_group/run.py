"""
V4 实验 - 对照组：单Agent无组织管理
======================================
模拟普通人使用AI的方式：一个聊天窗口，丢任务进去，等结果。
没有角色分工、没有协作、没有组织结构。

用法：
    cd aom-lite/v4_experiment/control_group
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
8. 代码为单个HTML文件，包含CSS和JS，可直接在浏览器中打开

请直接输出完整的HTML代码，不要分段，不要解释，只要代码。"""

SYSTEM_PROMPT = """你是一个全栈开发工程师。用户会给你一个开发任务，请直接输出完整可运行的代码。
不要输出任何解释、分步骤说明或markdown标记，只要纯代码。
代码必须完整、可直接运行，包含所有必要的HTML、CSS和JavaScript。"""

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
        print(f"  API调用失败: {e}")
        return "", 0, elapsed


def extract_html(text):
    """从LLM输出中提取HTML代码"""
    # 尝试提取 ```html ... ``` 块
    if "```html" in text:
        start = text.index("```html") + 7
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        # 跳过语言标记行
        nl = text.index("\n", start)
        start = nl + 1
        end = text.index("```", start)
        return text[start:end].strip()
    # 检查是否直接以 <html 或 <!DOCTYPE 开头
    stripped = text.strip()
    if stripped.startswith("<!DOCTYPE") or stripped.startswith("<html"):
        return stripped
    # 尝试找到第一个 < 标签
    idx = text.find("<")
    if idx >= 0:
        return text[idx:].strip()
    return text.strip()


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("V4 实验 - 对照组：单Agent无组织管理")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"API:  {BASE_URL}")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 确保输出目录存在
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # 记录开始时间
    total_start = time.time()
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("[1/1] 单Agent生成贪吃蛇游戏...")
    print("  调用LLM（这可能需要1-3分钟）...")

    html_raw, tokens, elapsed = call_llm(client, SYSTEM_PROMPT, TASK_PROMPT, max_tokens=8000)

    total_elapsed = time.time() - total_start

    if not html_raw:
        print("  错误：LLM未返回有效内容")
        sys.exit(1)

    # 提取并保存HTML
    html_code = extract_html(html_raw)
    game_path = output_dir / "game.html"
    game_path.write_text(html_code, encoding="utf-8")
    print(f"  游戏已保存: {game_path}")

    # 保存原始输出
    raw_path = output_dir / "raw_output.txt"
    raw_path.write_text(html_raw, encoding="utf-8")

    # 保存日志
    log = {
        "experiment": "V4 Control Group",
        "condition": "single_agent_no_organization",
        "model": MODEL,
        "timestamp": run_timestamp,
        "task": "贪吃蛇网页游戏",
        "total_api_calls": 1,
        "total_tokens": tokens,
        "total_time_seconds": round(total_elapsed, 1),
        "html_length": len(html_code),
        "details": [
            {
                "agent": "single_agent",
                "role": "全栈开发（无分工）",
                "tokens": tokens,
                "time_seconds": round(elapsed, 1),
                "output_length": len(html_raw),
            }
        ],
    }
    log_path = output_dir / "experiment_log.json"
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # 打印摘要
    print()
    print("=" * 60)
    print("对照组实验完成")
    print("=" * 60)
    print(f"  总API调用次数: 1")
    print(f"  总Token消耗:   {tokens}")
    print(f"  总耗时:        {total_elapsed:.1f}秒")
    print(f"  HTML代码长度:  {len(html_code)} 字符")
    print(f"  输出文件:      {game_path}")
    print(f"  日志文件:      {log_path}")
    print()
    print("请在浏览器中打开 output/game.html 查看效果。")


if __name__ == "__main__":
    main()
