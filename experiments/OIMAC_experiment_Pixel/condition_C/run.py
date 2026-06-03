"""
条件C：OIMAC（有Context Controller）
====================================
结构：6个Agent，流水线执行，Context Controller启用
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

PROMPTS_DIR = Path(__file__).parent / "prompts"
THETA_SPLIT = 8000  # Context Controller上限

def load_prompt(name):
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")

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

def apply_context_controller(text, max_chars=24000):
    """Rule 2: 限制context大小（约8000 tokens ≈ 24000字符）"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...内容已截断，超过Context Controller限制...]"

def main():
    print("=" * 60)
    print("条件C：OIMAC（有Context Controller）")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"组织结构: 6角色科层制")
    print(f"Context Controller: 启用（Rule 1/2/3）")
    print()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    total_start = time.time()
    log_details = []
    context_log = []

    # Step 1: Coordinator - Task Decomposition
    print("[1/7] 协调者：分解任务...")
    sp = load_prompt("coordinator")
    up = f"以下是开发任务，请进行任务分解：\n\n{TASK_PROMPT}"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=2000)
    task_decomposition = text
    log_details.append({"step": 1, "agent": "coordinator", "phase": "任务分解", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 1, "agent": "coordinator", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 2: Product Manager - Requirements
    print("[2/7] 产品经理：定义需求...")
    sp = load_prompt("product_manager")
    # Rule 1: 只传递直接依赖（协调者输出）
    up = f"协调者已将任务分解如下：\n\n{apply_context_controller(task_decomposition)}\n\n原始任务：\n{TASK_PROMPT}\n\n请输出结构化产品需求文档。"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=2000)
    requirements_doc = text
    log_details.append({"step": 2, "agent": "product_manager", "phase": "需求定义", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 2, "agent": "product_manager", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 3: Architect - System Design
    print("[3/7] 架构师：设计技术架构...")
    sp = load_prompt("architect")
    # Rule 1: 只传递直接依赖（需求文档）
    # Rule 3: 接口过滤（只传接口信息）
    up = f"产品需求文档：\n\n{apply_context_controller(requirements_doc)}\n\n原始任务：\n{TASK_PROMPT}\n\n请输出技术架构设计。"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=2000)
    arch_doc = text
    log_details.append({"step": 3, "agent": "architect", "phase": "架构设计", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 3, "agent": "architect", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 4: Frontend Dev - UI Implementation
    print("[4/7] 前端开发：实现界面...")
    sp = load_prompt("frontend_dev")
    # Rule 1: 只传递直接依赖（需求+架构）
    up = f"产品需求：\n\n{apply_context_controller(requirements_doc)}\n\n技术架构：\n\n{apply_context_controller(arch_doc)}\n\n请实现前端UI代码。只输出你负责的部分。"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=4000)
    frontend_code = text
    log_details.append({"step": 4, "agent": "frontend_dev", "phase": "前端实现", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 4, "agent": "frontend_dev", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 5: Image Processing Dev - Core Algorithms
    print("[5/7] 图像处理开发：实现核心算法...")
    sp = load_prompt("image_processing_dev")
    # Rule 1: 只传递直接依赖（需求+架构，不传前端代码）
    up = f"产品需求：\n\n{apply_context_controller(requirements_doc)}\n\n技术架构：\n\n{apply_context_controller(arch_doc)}\n\n请实现图像处理核心算法。只输出你负责的部分。"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=4000)
    image_code = text
    log_details.append({"step": 5, "agent": "image_processing_dev", "phase": "图像处理", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 5, "agent": "image_processing_dev", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 6: Tester - Code Review
    print("[6/7] 测试：审查代码...")
    sp = load_prompt("tester")
    # Rule 1: 只传递直接依赖（前端+图像处理代码）
    # Rule 3: 接口过滤
    up = f"前端代码：\n\n{apply_context_controller(frontend_code)}\n\n图像处理代码：\n\n{apply_context_controller(image_code)}\n\n请审查以上代码，检查接口兼容性和潜在问题。"
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=2000)
    test_report = text
    log_details.append({"step": 6, "agent": "tester", "phase": "测试审查", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 6, "agent": "tester", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    # Step 7: Coordinator - Integration
    print("[7/7] 协调者：整合最终产出...")
    sp = load_prompt("coordinator")
    # Rule 1: 传递所有直接依赖的输出
    up = (
        f"所有角色已完成工作。请整合以下产出为一个完整HTML文件：\n\n"
        f"需求文档：\n{apply_context_controller(requirements_doc)}\n\n"
        f"架构设计：\n{apply_context_controller(arch_doc)}\n\n"
        f"前端代码：\n{apply_context_controller(frontend_code)}\n\n"
        f"图像处理代码：\n{apply_context_controller(image_code)}\n\n"
        f"测试报告：\n{apply_context_controller(test_report)}\n\n"
        f"原始任务：\n{TASK_PROMPT}\n\n"
        f"请输出完整可运行的HTML代码，修复测试报告中的问题。直接输出代码，不要解释。"
    )
    ctx_len = len(up)
    text, tokens, elapsed = call_llm(client, sp, up, max_tokens=8000)
    final_html_raw = text
    log_details.append({"step": 7, "agent": "coordinator", "phase": "最终整合", "tokens": tokens, "time_seconds": round(elapsed, 1), "output_length": len(text), "context_length": ctx_len})
    context_log.append({"step": 7, "agent": "coordinator", "context_length": ctx_len})
    print(f"    Token={tokens}, 上下文={ctx_len:,}字符")

    total_time = time.time() - total_start

    # Save output
    html_code = extract_html(final_html_raw)
    (output_dir / "index.html").write_text(html_code, encoding="utf-8")

    # Save artifacts
    artifacts_dir = output_dir / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    (artifacts_dir / "01_task_decomposition.md").write_text(task_decomposition, encoding="utf-8")
    (artifacts_dir / "02_requirements.md").write_text(requirements_doc, encoding="utf-8")
    (artifacts_dir / "03_architecture.md").write_text(arch_doc, encoding="utf-8")
    (artifacts_dir / "04_frontend_code.txt").write_text(frontend_code, encoding="utf-8")
    (artifacts_dir / "05_image_processing.txt").write_text(image_code, encoding="utf-8")
    (artifacts_dir / "06_test_report.md").write_text(test_report, encoding="utf-8")

    total_tokens = sum(d["tokens"] for d in log_details)
    max_context = max(d["context_length"] for d in log_details)

    # Save logs
    log = {
        "experiment": "Perler Bead Pattern Generator - Condition C",
        "condition": "oimac_with_context_controller",
        "model": MODEL,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "organization": {"structure": "科层制", "roles": ["coordinator", "product_manager", "architect", "frontend_dev", "image_processing_dev", "tester"]},
        "context_controller": {"enabled": True, "rules": ["Rule 1: 只传直接依赖", "Rule 2: 上限8000 tokens", "Rule 3: 接口过滤"]},
        "total_tokens": total_tokens,
        "api_calls": 7,
        "total_time_seconds": round(total_time, 1),
        "output_length": len(html_code),
        "max_context_size": max_context,
        "context_growth": context_log,
        "details": log_details
    }
    (logs_dir / "token_usage.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(logs_dir / "context_growth.txt", "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n条件C Context Growth Log\n" + "=" * 60 + "\n\n")
        for entry in context_log:
            f.write(f"Step {entry['step']} [{entry['agent']:25s}]: 上下文 = {entry['context_length']:>10,} 字符\n")
        f.write(f"\n最大上下文: {max_context:,} 字符\n总Token: {total_tokens:,}\n")

    print(f"\n{'='*60}")
    print(f"完成! 总Token={total_tokens}, 最大上下文={max_context:,}, 耗时={total_time:.1f}s")

if __name__ == "__main__":
    main()
