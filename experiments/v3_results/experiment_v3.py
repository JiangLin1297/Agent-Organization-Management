"""
AOM-Lite V3 大规模对比实验：AOM-DT vs ST

核心改进：
- 4个异质Agent（新手/成长期/资深/专家）
- 9个任务（低/中/高不确定性各3个）
- 多Agent协作模式（1协调者 + 3工作者）
- 每任务重复5次
- 重点收集效率数据（时间、Token、协调开销）

实验规模：9任务 × 2条件 × 5重复 = 90次实验
每次实验 = 4次LLM调用（1协调 + 3工作）= 360次API调用

作者：AOM Research
日期：2026-06-01
"""

import json
import os
import csv
import time
import sys
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# ============================================================================
# 0. 环境配置
# ============================================================================

API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")

if not API_KEY:
    print("ERROR: OPENAI_API_KEY not set")
    sys.exit(1)


# ============================================================================
# 1. Agent 定义（4个异质Agent）
# ============================================================================

AGENTS = {
    "A": {
        "id": "agent_A",
        "name": "新手Agent",
        "htsr": 0.20,
        "confidence": 0.30,
        "readiness": 0.6 * 0.20 + 0.4 * 0.30,  # = 0.24
        "desc": "刚加入团队的新手，经验有限，需要详细指导"
    },
    "B": {
        "id": "agent_B",
        "name": "成长期Agent",
        "htsr": 0.50,
        "confidence": 0.60,
        "readiness": 0.6 * 0.50 + 0.4 * 0.60,  # = 0.54
        "desc": "有一定经验，正在快速成长，需要引导和鼓励"
    },
    "C": {
        "id": "agent_C",
        "name": "资深Agent",
        "htsr": 0.85,
        "confidence": 0.90,
        "readiness": 0.6 * 0.85 + 0.4 * 0.90,  # = 0.87
        "desc": "经验丰富，能力全面，可以自主决策"
    },
    "D": {
        "id": "agent_D",
        "name": "专家Agent",
        "htsr": 0.95,
        "confidence": 0.95,
        "readiness": 0.6 * 0.95 + 0.4 * 0.95,  # = 0.95
        "desc": "领域专家，可完全自主工作，适合做协调者"
    }
}

# 工作者列表（协调者固定为Agent D）
WORKERS = ["A", "B", "C"]
COORDINATOR = "D"


# ============================================================================
# 2. 任务定义（9个任务）
# ============================================================================

TASKS = [
    # 低不确定性（封闭式，信息检索）
    {
        "id": "L1", "uncertainty": 0.1, "level": "low",
        "desc": "2025年获得A轮融资的中国AI Agent公司有哪些？请列出至少3家及其融资金额。"
    },
    {
        "id": "L2", "uncertainty": 0.1, "level": "low",
        "desc": "Python 3.12中新增的type语句的具体语法是什么？请给出代码示例。"
    },
    {
        "id": "L3", "uncertainty": 0.1, "level": "low",
        "desc": "Docker和Kubernetes的区别是什么？请用一句话概括各自的核心功能。"
    },
    # 中不确定性（半开放式，分析比较）
    {
        "id": "M1", "uncertainty": 0.5, "level": "medium",
        "desc": "比较AutoGen和CrewAI在Agent协作设计上的主要区别，从架构、灵活性、易用性三个维度分析。"
    },
    {
        "id": "M2", "uncertainty": 0.5, "level": "medium",
        "desc": "分析RAG（检索增强生成）技术的优缺点，以及它在企业知识管理中的适用场景。"
    },
    {
        "id": "M3", "uncertainty": 0.5, "level": "medium",
        "desc": "评估当前AI代码生成工具（Copilot、Cursor、Claude）的成熟度，从准确性、安全性、集成度三个维度打分。"
    },
    # 高不确定性（开放式，综合判断与创造）
    {
        "id": "H1", "uncertainty": 0.9, "level": "high",
        "desc": "设计一套基于多Agent协作的在线教育平台架构，需要包含课程推荐、学习路径规划、自动答疑三个子系统。"
    },
    {
        "id": "H2", "uncertainty": 0.9, "level": "high",
        "desc": "设计一个基于多Agent协作的智慧城市交通管理系统，包括架构设计、Agent角色定义、通信协议和异常处理机制。"
    },
    {
        "id": "H3", "uncertainty": 0.9, "level": "high",
        "desc": "提出一个AI Agent伦理治理框架，涵盖责任归属、透明度要求、偏见检测和人类监督四个层面。"
    }
]


# ============================================================================
# 3. 领导风格映射
# ============================================================================

STYLE_MAP = {
    "S1": {
        "name": "S1_TELLING",
        "system": "你是一个执行严格指令的助手。请按照给定的步骤逐一执行，不要偏离指令。每步完成后进行验证。",
        "autonomy": "low"
    },
    "S2": {
        "name": "S2_SELLING",
        "system": "你是一个专业的分析助手。请理解任务目标后按计划执行，同时解释你的推理过程。如有疑问请提出。",
        "autonomy": "medium-low"
    },
    "S3": {
        "name": "S3_PARTICIPATING",
        "system": "你是一个协作型助手。任务目标已明确，但执行路径由你自主决定。请在关键决策点说明你的推理。",
        "autonomy": "medium-high"
    },
    "S4": {
        "name": "S4_DELEGATING",
        "system": "你是一个高度自主的专家助手。目标明确，实现方式由你全权决定。只需提交高质量的最终结果。",
        "autonomy": "high"
    }
}


def get_style_for_readiness(readiness):
    """根据准备度选择领导风格"""
    if readiness < 0.25:
        return "S1"
    elif readiness < 0.50:
        return "S2"
    elif readiness < 0.75:
        return "S3"
    else:
        return "S4"


def get_worker_prompt(style_key, task_desc, sub_task, agent_name):
    """根据风格生成工作者的提示词"""
    style = STYLE_MAP[style_key]

    if style_key == "S1":
        return (
            f"你是{agent_name}，负责执行以下子任务。\n\n"
            f"主任务：{task_desc}\n\n"
            f"你的子任务：{sub_task}\n\n"
            f"执行要求：\n"
            f"1. 严格按照子任务要求执行\n"
            f"2. 不要偏离指定范围\n"
            f"3. 输出结构化、简洁的结果\n"
            f"4. 如有不确定，标注[待确认]"
        )
    elif style_key == "S2":
        return (
            f"你是{agent_name}，负责执行以下子任务。\n\n"
            f"主任务：{task_desc}\n\n"
            f"你的子任务：{sub_task}\n\n"
            f"执行要求：\n"
            f"1. 理解子任务的背景和目的\n"
            f"2. 按计划执行，同时说明你的推理过程\n"
            f"3. 如有不同见解，请提出\n"
            f"4. 输出有深度的分析结果"
        )
    elif style_key == "S3":
        return (
            f"你是{agent_name}，负责以下子任务。执行路径由你自主决定。\n\n"
            f"主任务：{task_desc}\n\n"
            f"你的子任务：{sub_task}\n\n"
            f"要求：在关键决策点说明你的推理，输出高质量的分析。"
        )
    else:  # S4
        return (
            f"你是{agent_name}，负责以下子任务。具体方法由你全权决定。\n\n"
            f"主任务：{task_desc}\n\n"
            f"你的子任务：{sub_task}\n\n"
            f"要求：只需提交高质量的最终结果。"
        )


# ============================================================================
# 4. LLM 调用函数
# ============================================================================

def call_llm(client, system_prompt, user_prompt, max_tokens=1500):
    """调用LLM，返回(输出文本, token数, 耗时)"""
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            timeout=120.0
        )
        elapsed = time.time() - start
        text = resp.choices[0].message.content or ""
        tokens = resp.usage.total_tokens if resp.usage else 0
        return text, tokens, elapsed
    except Exception as e:
        elapsed = time.time() - start
        return "", 0, elapsed


def call_coordinator(client, task_desc):
    """协调者调用：分析任务并制定分配计划"""
    system_prompt = (
        "你是一个多Agent团队的协调者。你的职责是：\n"
        "1. 分析复杂任务\n"
        "2. 将任务分解为3个子任务\n"
        "3. 为每个子任务分配给不同能力水平的Agent\n\n"
        "输出格式（严格JSON）：\n"
        '{"subtasks": [\n'
        '  {"agent": "A", "task": "子任务描述", "focus": "重点"},\n'
        '  {"agent": "B", "task": "子任务描述", "focus": "重点"},\n'
        '  {"agent": "C", "task": "子任务描述", "focus": "重点"}\n'
        '], "synthesis_plan": "如何整合三个子任务的结果"}'
    )
    user_prompt = f"请分析以下任务并制定分配计划：\n\n{task_desc}"

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=800)

    # 尝试解析JSON
    try:
        # 提取JSON部分
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            plan = json.loads(text[json_start:json_end])
        else:
            raise ValueError("No JSON found")
    except:
        # 回退计划
        plan = {
            "subtasks": [
                {"agent": "A", "task": f"收集{task_desc}的基础信息和背景", "focus": "信息检索"},
                {"agent": "B", "task": f"分析{task_desc}的关键要素和关系", "focus": "分析推理"},
                {"agent": "C", "task": f"综合{task_desc}的分析结果并提出结论", "focus": "综合判断"}
            ],
            "synthesis_plan": "整合三个Agent的输出，形成完整回答"
        }

    return plan, tokens, elapsed


def synthesize_result(client, task_desc, sub_results):
    """协调者整合最终结果"""
    system_prompt = "你是一个多Agent团队的协调者。请整合以下三个子任务的结果，生成一份完整、高质量的最终回答。"
    parts = [f"主任务：{task_desc}\n"]
    for r in sub_results:
        parts.append(f"--- {r['agent_name']}的贡献 ---\n{r['output']}\n")
    user_prompt = "\n".join(parts)

    text, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=1500)
    return text, tokens, elapsed


# ============================================================================
# 5. 单次实验执行
# ============================================================================

def run_single_trial(client, task, condition, trial_id):
    """
    执行单次实验

    参数:
        task: 任务字典
        condition: "ST" 或 "AOM-DT"
        trial_id: 试次编号

    返回:
        dict: 包含所有指标的实验结果
    """
    result = {
        "task_id": task["id"],
        "uncertainty_level": task["level"],
        "uncertainty_value": task["uncertainty"],
        "task_description": task["desc"],
        "condition": condition,
        "trial_id": trial_id,
        "timestamp": datetime.now().isoformat(),
    }

    total_tokens = 0
    total_time = 0.0
    agent_details = []

    # ---- Step 1: 协调者分配任务 ----
    coord_plan, coord_tokens, coord_time = call_coordinator(client, task["desc"])
    total_tokens += coord_tokens
    total_time += coord_time

    result["coordinator_tokens"] = coord_tokens
    result["coordinator_time"] = round(coord_time, 2)

    # ---- Step 2: 三个工作者并行执行 ----
    def execute_worker(i, worker_key):
        agent = AGENTS[worker_key]
        sub_task_info = coord_plan["subtasks"][i] if i < len(coord_plan["subtasks"]) else {
            "task": f"分析{task['desc']}的相关方面",
            "focus": "综合分析"
        }
        sub_task = sub_task_info.get("task", f"分析任务的第{i+1}部分")

        if condition == "ST":
            style_key = "S1"
        else:
            style_key = get_style_for_readiness(agent["readiness"])

        system_prompt = STYLE_MAP[style_key]["system"]
        user_prompt = get_worker_prompt(style_key, task["desc"], sub_task, agent["name"])

        output, tokens, elapsed = call_llm(client, system_prompt, user_prompt, max_tokens=1200)
        return {
            "agent_key": worker_key,
            "agent_name": agent["name"],
            "readiness": agent["readiness"],
            "style": STYLE_MAP[style_key]["name"],
            "tokens": tokens,
            "time": round(elapsed, 2),
            "output": output,
            "output_length": len(output)
        }

    worker_results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(execute_worker, i, wk): wk for i, wk in enumerate(WORKERS)}
        for future in as_completed(futures):
            wr = future.result()
            worker_results.append(wr)
            total_tokens += wr["tokens"]
            total_time += wr["time"]
            agent_details.append(wr)
    # Sort by agent key to maintain consistent order
    worker_results.sort(key=lambda x: x["agent_key"])

    # ---- Step 3: 协调者整合结果 ----
    synthesis_text, synth_tokens, synth_time = synthesize_result(client, task["desc"], worker_results)
    total_tokens += synth_tokens
    total_time += synth_time

    result["synthesis_tokens"] = synth_tokens
    result["synthesis_time"] = round(synth_time, 2)

    # ---- 汇总 ----
    result["total_tokens"] = total_tokens
    result["total_time"] = round(total_time, 2)
    result["coordination_overhead_tokens"] = coord_tokens + synth_tokens
    result["coordination_overhead_pct"] = round(
        (coord_tokens + synth_tokens) / total_tokens * 100, 1
    ) if total_tokens > 0 else 0

    # 工作者详情
    for wr in worker_results:
        prefix = f"worker_{wr['agent_key']}"
        result[f"{prefix}_style"] = wr["style"]
        result[f"{prefix}_tokens"] = wr["tokens"]
        result[f"{prefix}_time"] = wr["time"]
        result[f"{prefix}_output_length"] = wr["output_length"]

    # 成功判定
    final_output = synthesis_text if synthesis_text else worker_results[-1]["output"] if worker_results else ""
    result["final_output_length"] = len(final_output)
    result["success"] = len(final_output.strip()) > 50

    # 质量评估（基于输出特征的启发式评分）
    result["quality_score"] = evaluate_quality_heuristic(final_output, task["desc"])

    return result


def evaluate_quality_heuristic(output, task_desc):
    """
    启式质量评估（1-5分）
    避免额外API调用，基于输出特征评估
    """
    if not output or len(output.strip()) < 30:
        return 1

    score = 3  # 基准分

    # 长度加分
    if len(output) > 500:
        score += 0.5
    if len(output) > 1000:
        score += 0.5

    # 结构化加分
    if any(marker in output for marker in ["##", "###", "**", "- ", "1.", "2.", "3."]):
        score += 0.3

    # 关键信息覆盖（简单检查）
    task_words = set(task_desc.replace("？", "").replace("。", "").replace("，", "").split())
    output_words = set(output.replace("？", "").replace("。", "").replace("，", "").split())
    overlap = len(task_words & output_words) / max(len(task_words), 1)
    if overlap > 0.3:
        score += 0.2

    return min(5, max(1, round(score)))


# ============================================================================
# 6. 主实验流程
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              AOM-Lite V3 大规模对比实验                              ║
║              AOM-DT vs ST | 多Agent协作 | 效率优先                    ║
║                                                                      ║
║  4 Agents x 9 Tasks x 2 Conditions x 5 Trials = 90 Experiments      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=120.0)
    print(f"LLM Client: {MODEL} @ {BASE_URL}")

    # 打印Agent配置
    print("\n--- Agent Configuration ---")
    for key, agent in AGENTS.items():
        role = "Coordinator" if key == COORDINATOR else "Worker"
        style = get_style_for_readiness(agent["readiness"])
        print(f"  Agent {key} ({agent['name']}): HTSR={agent['htsr']}, "
              f"Conf={agent['confidence']}, Readiness={agent['readiness']:.2f}, "
              f"AOM-DT Style={style}, Role={role}")

    # 实验参数
    conditions = ["ST", "AOM-DT"]
    trials_per = 5
    total = len(TASKS) * len(conditions) * trials_per
    print(f"\nTotal experiments: {total}")
    print(f"API calls per experiment: 5 (1 coord + 3 workers + 1 synthesis)")
    print(f"Total API calls: {total * 5}")

    # 执行实验
    results = []
    count = 0
    global_start = time.time()

    for task in TASKS:
        for condition in conditions:
            for trial in range(1, trials_per + 1):
                count += 1
                elapsed_min = (time.time() - global_start) / 60
                print(f"\n[{count}/{total}] Task={task['id']} ({task['level']}) "
                      f"Condition={condition} Trial={trial} "
                      f"[{elapsed_min:.1f}min elapsed]")

                r = run_single_trial(client, task, condition, trial)
                results.append(r)

                status = "OK" if r["success"] else "FAIL"
                print(f"  => {status} | Tokens={r['total_tokens']} "
                      f"Time={r['total_time']:.1f}s "
                      f"Quality={r['quality_score']}/5 "
                      f"CoordOverhead={r['coordination_overhead_pct']:.0f}%")

                # 保存中间结果（每5次保存一次）
                if count % 5 == 0:
                    save_results(results, "experiment_v3_results_partial.csv")
                    print(f"  [Checkpoint saved: {count} results]")

                # 避免限流
                time.sleep(0.5)

    # 保存最终结果
    total_time = time.time() - global_start
    output_file = "experiment_v3_results.csv"
    save_results(results, output_file)

    # 打印汇总
    print_summary(results, total_time, output_file)


def save_results(results, filepath):
    """保存实验结果到CSV"""
    if not results:
        return

    fieldnames = [
        "task_id", "uncertainty_level", "uncertainty_value", "task_description",
        "condition", "trial_id", "timestamp",
        "total_tokens", "total_time",
        "coordinator_tokens", "coordinator_time",
        "synthesis_tokens", "synthesis_time",
        "coordination_overhead_tokens", "coordination_overhead_pct",
        "worker_A_style", "worker_A_tokens", "worker_A_time", "worker_A_output_length",
        "worker_B_style", "worker_B_tokens", "worker_B_time", "worker_B_output_length",
        "worker_C_style", "worker_C_tokens", "worker_C_time", "worker_C_output_length",
        "final_output_length", "success", "quality_score"
    ]

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)


def print_summary(results, total_time, output_file):
    """打印实验汇总"""
    print(f"\n{'='*70}")
    print(f"V3 EXPERIMENT COMPLETE")
    print(f"{'='*70}")
    print(f"Total experiments: {len(results)}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Results saved to: {output_file}")

    for condition in ["ST", "AOM-DT"]:
        subset = [r for r in results if r["condition"] == condition]
        if not subset:
            continue

        n = len(subset)
        success = sum(1 for r in subset if r["success"])
        tokens = [r["total_tokens"] for r in subset if r["total_tokens"] > 0]
        times = [r["total_time"] for r in subset if r["total_time"] > 0]
        qualities = [r["output_quality"] for r in subset] if "output_quality" in subset[0] else [r["quality_score"] for r in subset]
        coord_pcts = [r["coordination_overhead_pct"] for r in subset]

        print(f"\n--- {condition} ---")
        print(f"  Success: {success}/{n} ({success/n*100:.1f}%)")
        print(f"  Avg Tokens: {np.mean(tokens):.0f} (std={np.std(tokens):.0f})")
        print(f"  Avg Time: {np.mean(times):.1f}s (std={np.std(times):.1f}s)")
        print(f"  Avg Quality: {np.mean(qualities):.2f}/5")
        print(f"  Avg Coord Overhead: {np.mean(coord_pcts):.1f}%")

        # 按不确定性水平
        for level in ["low", "medium", "high"]:
            level_subset = [r for r in subset if r["uncertainty_level"] == level]
            if not level_subset:
                continue
            lt = [r["total_tokens"] for r in level_subset]
            ltime = [r["total_time"] for r in level_subset]
            lq = [r["quality_score"] for r in level_subset]
            print(f"    {level:6s}: tokens={np.mean(lt):.0f}, time={np.mean(ltime):.1f}s, quality={np.mean(lq):.2f}")

    # 效率对比
    print(f"\n--- EFFICIENCY COMPARISON ---")
    for level in ["low", "medium", "high"]:
        st = [r for r in results if r["condition"] == "ST" and r["uncertainty_level"] == level]
        dt = [r for r in results if r["condition"] == "AOM-DT" and r["uncertainty_level"] == level]
        if not st or not dt:
            continue

        st_tok = np.mean([r["total_tokens"] for r in st])
        dt_tok = np.mean([r["total_tokens"] for r in dt])
        st_time = np.mean([r["total_time"] for r in st])
        dt_time = np.mean([r["total_time"] for r in dt])

        tok_diff = (dt_tok - st_tok) / st_tok * 100 if st_tok > 0 else 0
        time_diff = (dt_time - st_time) / st_time * 100 if st_time > 0 else 0

        print(f"  {level:6s}: Token diff={tok_diff:+.1f}%, Time diff={time_diff:+.1f}%")


if __name__ == "__main__":
    main()
