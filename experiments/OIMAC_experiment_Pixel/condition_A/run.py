"""
条件A：单Agent基线（Single-Pass）
================================
结构：1个Agent，1次调用，无迭代
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
    print("条件A：单Agent基线（Single-Pass）")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    start = time.time()
    system_prompt = "你是一个资深全栈开发者。请直接实现用户要求的完整功能，输出可运行的HTML代码。"
    text, tokens, elapsed = call_llm(client, system_prompt, TASK_PROMPT, max_tokens=8000)
    total_time = time.time() - start

    if not text:
        print("错误：API未返回内容")
        sys.exit(1)

    html_code = extract_html(text)
    (output_dir / "index.html").write_text(html_code, encoding="utf-8")

    log = {
        "experiment": "Perler Bead Pattern Generator - Condition A",
        "condition": "single_agent_baseline",
        "model": MODEL,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "total_tokens": tokens,
        "api_calls": 1,
        "total_time_seconds": round(total_time, 1),
        "output_length": len(html_code),
        "details": [{"step": 1, "agent": "single", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text)}]
    }
    (logs_dir / "token_usage.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n完成! Token={tokens}, 耗时={total_time:.1f}s, HTML={len(html_code)}字符")
    print(f"输出: {output_dir / 'index.html'}")

if __name__ == "__main__":
    main()
