"""
AOM-Lite 对比实验：AOM-DT vs ST

实验设计：
- 对照组（ST）：所有Agent使用固定的 S1_TELLING 风格
- 实验组（AOM-DT）：使用情境领导动态切换逻辑

任务：3类不确定性 × 5个任务 × 2条件 × 2次 = 60次实验

作者：AOM Research
日期：2026-06-01
"""

import json
import os
import csv
import time
import random
import numpy as np
from datetime import datetime
from openai import OpenAI

# 导入 main.py 中的组件
from main import (
    Agent, Task, LeadershipStyle, ExecutionResult,
    select_leadership_style, get_instruction_template
)


# ============================================================================
# 1. 实验任务定义
# ============================================================================

TASKS = {
    "low": [
        {
            "id": "L1",
            "description": "2025年获得A轮融资的中国AI Agent公司有哪些？请列出至少3家及其融资金额。",
            "uncertainty": 0.1
        },
        {
            "id": "L2",
            "description": "GPT-4o支持的最大上下文窗口是多少tokens？请给出准确数字。",
            "uncertainty": 0.1
        },
        {
            "id": "L3",
            "description": "Python 3.12中新增的type语句的具体语法是什么？请给出代码示例。",
            "uncertainty": 0.1
        },
        {
            "id": "L4",
            "description": "Linux内核6.6版本的主要新特性有哪些？请列出至少3个。",
            "uncertainty": 0.1
        },
        {
            "id": "L5",
            "description": "Docker和Kubernetes的区别是什么？请用一句话概括各自的核心功能。",
            "uncertainty": 0.1
        }
    ],
    "medium": [
        {
            "id": "M1",
            "description": "比较AutoGen和CrewAI在Agent协作设计上的主要区别，从架构、灵活性、易用性三个维度分析。",
            "uncertainty": 0.5
        },
        {
            "id": "M2",
            "description": "AI Agent在医疗和金融两个行业的应用场景有何异同？从数据敏感性、监管要求、容错率三个角度分析。",
            "uncertainty": 0.5
        },
        {
            "id": "M3",
            "description": "分析RAG（检索增强生成）技术的优缺点，以及它在企业知识管理中的适用场景。",
            "uncertainty": 0.5
        },
        {
            "id": "M4",
            "description": "对比Transformer和Mamba架构在长序列处理上的性能差异，分析各自的适用场景。",
            "uncertainty": 0.5
        },
        {
            "id": "M5",
            "description": "评估当前AI代码生成工具（Copilot、Cursor、Claude）的成熟度，从准确性、安全性、集成度三个维度打分。",
            "uncertainty": 0.5
        }
    ],
    "high": [
        {
            "id": "H1",
            "description": "预测2026-2028年AI Agent技术对社会生产力的影响，考虑就业结构变化、产业升级、教育转型三个维度。",
            "uncertainty": 0.9
        },
        {
            "id": "H2",
            "description": "设计一个基于多Agent协作的智慧城市交通管理系统，包括架构设计、Agent角色定义、通信协议和异常处理机制。",
            "uncertainty": 0.9
        },
        {
            "id": "H3",
            "description": "提出一个AI Agent伦理治理框架，涵盖责任归属、透明度要求、偏见检测和人类监督四个层面。",
            "uncertainty": 0.9
        },
        {
            "id": "H4",
            "description": "设计一个去中心化的多Agent协作协议，使不同组织的Agent能够在无需中心化协调的情况下完成复杂任务。",
            "uncertainty": 0.9
        },
        {
            "id": "H5",
            "description": "提出一种新的Agent能力评估方法论，超越传统的任务成功率指标，考虑泛化能力、鲁棒性、可解释性等维度。",
            "uncertainty": 0.9
        }
    ]
}


# ============================================================================
# 2. Agent 配置
# ============================================================================

AGENTS = [
    Agent(
        agent_id="agent_001",
        name="新手Agent",
        htsr=0.2,
        confidence=0.3,
        capability_description="刚加入团队的新手"
    ),
    Agent(
        agent_id="agent_002",
        name="成长期Agent",
        htsr=0.5,
        confidence=0.6,
        capability_description="有一定经验"
    ),
    Agent(
        agent_id="agent_003",
        name="资深Agent",
        htsr=0.85,
        confidence=0.9,
        capability_description="经验丰富"
    ),
    Agent(
        agent_id="agent_004",
        name="专家Agent",
        htsr=0.95,
        confidence=0.95,
        capability_description="领域专家"
    )
]


# ============================================================================
# 3. 风格评估函数
# ============================================================================

def evaluate_output_quality(client, model, task_description, output_text):
    """
    使用 LLM 评估输出质量（1-5分）
    """
    if not output_text or len(output_text.strip()) < 20:
        return 1

    eval_prompt = f"""请评估以下AI回答的质量，评分标准：
1分：完全无关或拒绝回答
2分：相关但信息严重不足或有明显错误
3分：基本相关，有一定信息量但不够深入
4分：质量较好，信息准确且有一定深度
5分：优秀，信息准确、全面、有深度、结构清晰

任务：{task_description}

AI回答：
{output_text[:1500]}

请只输出一个数字（1-5），不要输出其他内容。"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": eval_prompt}],
            max_tokens=10,
            temperature=0.1
        )
        score_text = response.choices[0].message.content.strip()
        # 提取数字
        for char in score_text:
            if char.isdigit() and 1 <= int(char) <= 5:
                return int(char)
        return 3  # 默认
    except Exception:
        return 3  # 出错时给默认分


# ============================================================================
# 4. 单次实验执行
# ============================================================================

def run_single_experiment(task, condition, agent, client, model, config):
    """
    执行单次实验

    参数:
        task: 任务描述字典
        condition: "ST" 或 "AOM-DT"
        agent: Agent 对象
        client: LLM 客户端
        model: 模型名称
        config: 配置

    返回:
        dict: 实验结果
    """
    task_obj = Task(
        task_id=task["id"],
        description=task["description"],
        uncertainty=task["uncertainty"]
    )

    gamma = config["readiness_calculation"]["gamma"]
    readiness = agent.get_readiness(gamma)

    # 根据条件选择风格
    if condition == "ST":
        style = LeadershipStyle.S1_TELLING  # 固定风格
    else:  # AOM-DT
        style = select_leadership_style(
            readiness,
            task_obj.uncertainty,
            config["readiness_thresholds"]
        )

    # 获取指令模板
    instruction_template = get_instruction_template(style, task_obj.description)

    # 构建系统提示词
    style_descriptions = {
        LeadershipStyle.S1_TELLING: "你是一个执行严格指令的助手。请按照给定的步骤逐一执行，不要偏离指令。",
        LeadershipStyle.S2_SELLING: "你是一个专业的分析助手。请理解任务目标后按计划执行，同时解释你的推理过程。",
        LeadershipStyle.S3_PARTICIPATING: "你是一个协作型助手。任务目标已明确，但执行路径由你自主决定。",
        LeadershipStyle.S4_DELEGATING: "你是一个高度自主的专家助手。目标明确，实现方式由你全权决定。"
    }

    system_prompt = style_descriptions[style]
    instruction = instruction_template['instruction']

    user_prompt_parts = [f"任务：{task_obj.description}\n"]
    if 'steps' in instruction:
        user_prompt_parts.append("执行步骤：")
        for step in instruction['steps']:
            user_prompt_parts.append(f"  {step}")
    if 'constraints' in instruction:
        user_prompt_parts.append("\n约束条件：")
        for c in instruction['constraints']:
            user_prompt_parts.append(f"  - {c}")
    if 'acceptance_criteria' in instruction:
        user_prompt_parts.append("\n验收标准：")
        for a in instruction['acceptance_criteria']:
            user_prompt_parts.append(f"  - {a}")
    if 'background' in instruction:
        user_prompt_parts.append(f"\n背景：{instruction['background']}")
    if 'objective' in instruction:
        user_prompt_parts.append(f"\n目标：{instruction['objective']}")

    user_prompt = "\n".join(user_prompt_parts)

    # 执行 LLM 调用
    tokens_consumed = 0
    execution_time = 0.0
    output_text = ""
    error_message = ""
    success = False

    max_retries = 3
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7,
                timeout=120.0
            )
            end_time = time.time()

            execution_time = end_time - start_time
            output_text = response.choices[0].message.content or ""
            tokens_consumed = response.usage.total_tokens if response.usage else 0

            success = (
                len(output_text.strip()) > 30 and
                "抱歉" not in output_text[:100] and
                "无法" not in output_text[:100] and
                "I cannot" not in output_text[:100]
            )
            break

        except Exception as e:
            error_message = str(e)
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
            else:
                success = False

    # 评估输出质量
    quality_score = evaluate_output_quality(client, model, task_obj.description, output_text)

    return {
        "task_id": task["id"],
        "uncertainty_level": "low" if task["uncertainty"] < 0.3 else ("medium" if task["uncertainty"] < 0.7 else "high"),
        "uncertainty_value": task["uncertainty"],
        "task_description": task["description"],
        "condition": condition,
        "agent_id": agent.agent_id,
        "agent_name": agent.name,
        "readiness_score": round(readiness, 4),
        "selected_style": style.value,
        "execution_time_seconds": round(execution_time, 2),
        "token_consumed": tokens_consumed,
        "success": success,
        "output_quality": quality_score,
        "output_length": len(output_text),
        "error_message": error_message
    }


# ============================================================================
# 5. 主实验流程
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              AOM-Lite 对比实验：AOM-DT vs ST                    ║
║              使用真实 LLM API (MiMo-v2.5-pro)                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

    # 初始化
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
    model = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")

    if not api_key:
        print("❌ 请设置 OPENAI_API_KEY 环境变量")
        return

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=120.0)
    print(f"✅ LLM 客户端初始化成功 | 模型: {model}")

    # 加载配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)["aom_lite_config"]
    print("✅ 配置加载成功")

    # 收集所有任务
    all_tasks = []
    for level in ["low", "medium", "high"]:
        all_tasks.extend(TASKS[level])

    # 选择Agent（使用成长期Agent代表中等水平）
    test_agent = AGENTS[1]  # 成长期Agent

    # 实验参数
    runs_per_condition = 2  # 每个条件重复2次
    conditions = ["ST", "AOM-DT"]

    total_experiments = len(all_tasks) * len(conditions) * runs_per_condition
    print(f"\n📊 实验设计:")
    print(f"   任务数: {len(all_tasks)} (低/中/高 各5个)")
    print(f"   条件数: {len(conditions)} (ST, AOM-DT)")
    print(f"   重复次数: {runs_per_condition}")
    print(f"   总实验数: {total_experiments}")
    print(f"   Agent: {test_agent.name} (Readiness={test_agent.get_readiness():.2%})")

    # 执行实验
    results = []
    experiment_count = 0
    start_time = time.time()

    for task in all_tasks:
        for condition in conditions:
            for run in range(runs_per_condition):
                experiment_count += 1
                print(f"\n{'='*60}")
                print(f"🔬 实验 {experiment_count}/{total_experiments}")
                print(f"   任务: {task['id']} ({task['uncertainty']:.1%} 不确定性)")
                print(f"   条件: {condition}")
                print(f"   重复: {run+1}/{runs_per_condition}")
                print(f"{'='*60}")

                result = run_single_experiment(
                    task, condition, test_agent, client, model, config
                )
                result["run_id"] = run + 1
                results.append(result)

                # 打印结果摘要
                status = "✅" if result["success"] else "❌"
                print(f"   {status} 质量={result['output_quality']}/5 | "
                      f"时间={result['execution_time_seconds']:.1f}s | "
                      f"Token={result['token_consumed']}")

                # 保存中间结果
                if experiment_count % 10 == 0:
                    save_results(results, "experiment_results_partial.csv")

                # 避免API限流
                time.sleep(2)

    # 保存最终结果
    total_time = time.time() - start_time
    save_results(results, "experiment_results.csv")

    # 打印汇总
    print(f"\n{'='*70}")
    print(f"📊 实验完成汇总")
    print(f"{'='*70}")
    print(f"总实验数: {len(results)}")
    print(f"总耗时: {total_time/60:.1f} 分钟")

    st_results = [r for r in results if r["condition"] == "ST"]
    aom_results = [r for r in results if r["condition"] == "AOM-DT"]

    st_success = sum(1 for r in st_results if r["success"])
    aom_success = sum(1 for r in aom_results if r["success"])

    print(f"\nST 组: {st_success}/{len(st_results)} 成功 ({st_success/len(st_results)*100:.1f}%)")
    print(f"AOM-DT 组: {aom_success}/{len(aom_results)} 成功 ({aom_success/len(aom_results)*100:.1f}%)")

    st_quality = np.mean([r["output_quality"] for r in st_results])
    aom_quality = np.mean([r["output_quality"] for r in aom_results])
    print(f"\nST 平均质量: {st_quality:.2f}/5")
    print(f"AOM-DT 平均质量: {aom_quality:.2f}/5")

    st_tokens = np.mean([r["token_consumed"] for r in st_results if r["token_consumed"] > 0])
    aom_tokens = np.mean([r["token_consumed"] for r in aom_results if r["token_consumed"] > 0])
    print(f"\nST 平均Token: {st_tokens:.0f}")
    print(f"AOM-DT 平均Token: {aom_tokens:.0f}")

    print(f"\n✅ 结果已保存至: aom-lite/experiment_results.csv")


def save_results(results, filepath):
    """保存实验结果到CSV"""
    if not results:
        return

    fieldnames = [
        "task_id", "uncertainty_level", "uncertainty_value", "task_description",
        "condition", "agent_id", "agent_name", "readiness_score", "selected_style",
        "execution_time_seconds", "token_consumed", "success", "output_quality",
        "output_length", "error_message", "run_id"
    ]

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
