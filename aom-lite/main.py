"""
AOM-Lite MVP: 情境领导风格动态切换原型
Agent Organizational Management - Lightweight Minimum Viable Product

==========================================================================
⚠️ 注意：此程序为纯模拟版本，所有执行结果均为随机生成的模拟数据。
⚠️ 未调用任何真实 LLM API，仅用于展示 AOM 的决策流程。
==========================================================================

论文参考：智能体组织管理学 V2.0, §5.2.1
作者：江皓然
日期：2026-05-30

运行方式：
    cd aom-lite
    pip install -r requirements.txt
    python main.py
"""

import json
import random
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum


# ============================================================================
# 1. 定义领导风格枚举
# ============================================================================

class LeadershipStyle(Enum):
    """
    赫塞-布兰查德情境领导模型的四种风格
    Hersey-Blanchard Situational Leadership Model

    S1: TELLING（告知式）- 高任务行为，低关系行为
    S2: SELLING（推销式）- 高任务行为，高关系行为
    S3: PARTICIPATING（参与式）- 低任务行为，高关系行为
    S4: DELEGATING（授权式）- 低任务行为，低关系行为
    """
    S1_TELLING = "S1_TELLING"
    S2_SELLING = "S2_SELLING"
    S3_PARTICIPATING = "S3_PARTICIPATING"
    S4_DELEGATING = "S4_DELEGATING"


# ============================================================================
# 2. 定义数据类
# ============================================================================

@dataclass
class Agent:
    """
    Agent 类：代表一个 AI 智能体

    属性：
        agent_id: 唯一标识符
        name: Agent 名称
        htsr: 历史任务成功率 (Historical Task Success Rate)
        confidence: 自我报告的能力置信度 [0, 1]
        capability_description: 能力描述
    """
    agent_id: str
    name: str
    htsr: float  # Historical Task Success Rate, 范围 [0, 1]
    confidence: float  # Self-reported confidence, 范围 [0, 1]
    capability_description: str = ""

    def get_readiness(self, gamma: float = 0.6) -> float:
        """
        计算准备度 (Readiness Score)

        公式：readiness = gamma * HTSR + (1 - gamma) * Confidence

        参数:
            gamma: HTSR 的权重，(1-gamma) 为 Confidence 的权重
                   gamma > 0.5 表示更重视历史表现

        返回:
            float: 准备度分数，范围 [0, 1]
        """
        readiness = gamma * self.htsr + (1 - gamma) * self.confidence
        return np.clip(readiness, 0.0, 1.0)


@dataclass
class Task:
    """
    Task 类：代表一个待执行的任务

    属性：
        task_id: 唯一标识符
        description: 任务描述
        uncertainty: 任务不确定性水平 [0, 1]
                    0 = 完全确定
                    1 = 高度不确定
    """
    task_id: str
    description: str
    uncertainty: float


@dataclass
class ExecutionResult:
    """
    执行结果类

    属性：
        success: 是否成功
        tokens_consumed: 消耗的 token 数
        style_used: 使用的领导风格
        readiness_score: 准备度分数
        task_uncertainty: 任务不确定性
        instruction_template: 使用的指令模板
        execution_log: 执行日志
    """
    success: bool
    tokens_consumed: int
    style_used: LeadershipStyle
    readiness_score: float
    task_uncertainty: float
    instruction_template: Dict
    execution_log: str


# ============================================================================
# 3. 风格选择函数
# ============================================================================

def select_leadership_style(
    readiness: float,
    task_uncertainty: float,
    thresholds: Dict
) -> LeadershipStyle:
    """
    根据准备度选择领导风格

    决策逻辑：
    根据 readiness 分数和配置阈值确定风格

    参数:
        readiness: Agent 的准备度分数 [0, 1]
        task_uncertainty: 任务不确定性 [0, 1]（当前未使用）
        thresholds: 阈值配置

    返回:
        LeadershipStyle: 选择的领导风格
    """
    if readiness < 0.25:
        return LeadershipStyle.S1_TELLING
    elif readiness < 0.50:
        return LeadershipStyle.S2_SELLING
    elif readiness < 0.75:
        return LeadershipStyle.S3_PARTICIPATING
    else:
        return LeadershipStyle.S4_DELEGATING


def get_instruction_template(style: LeadershipStyle, task_description: str) -> Dict:
    """
    根据领导风格和实际任务描述，动态生成指令模板

    参数:
        style: 领导风格
        task_description: 任务描述

    返回:
        Dict: 指令模板
    """
    if style == LeadershipStyle.S1_TELLING:
        return {
            "type": "direct_command",
            "format": "明确指定任务目标、步骤、约束条件和验收标准",
            "detail_level": "high",
            "autonomy_level": "low",
            "instruction": {
                "task": task_description,
                "steps": [
                    f"1. 明确「{task_description}」的数据来源和范围",
                    f"2. 按照标准流程执行数据采集与清洗",
                    f"3. 完成核心分析并生成可视化图表",
                    f"4. 整合结果并输出结构化报告"
                ],
                "constraints": [
                    "必须严格按照上述步骤顺序执行",
                    "每步完成后进行数据校验",
                    "如有异常立即上报，不得自行变更方案"
                ],
                "acceptance_criteria": [
                    "报告内容完整覆盖任务描述的所有要求",
                    "可视化图表清晰、准确",
                    "数据来源可追溯、结果可复现"
                ]
            }
        }
    elif style == LeadershipStyle.S2_SELLING:
        return {
            "type": "guided_explanation",
            "format": "解释任务背景和原因，提供详细指导，鼓励提问",
            "detail_level": "medium-high",
            "autonomy_level": "low-medium",
            "instruction": {
                "task": task_description,
                "background": f"「{task_description}」是当前业务决策的重要支撑，分析结果将直接影响后续策略制定",
                "why": "高质量的数据分析和可视化能够帮助团队快速洞察趋势、发现问题并做出精准决策",
                "guidance": [
                    f"建议先梳理「{task_description}」的关键指标体系",
                    "数据清洗阶段注意异常值和缺失值的处理",
                    "可视化设计要兼顾美观性和信息密度"
                ],
                "encouragement": "你已经具备完成这项任务的基础能力，遇到不确定的地方随时讨论",
                "open_questions": [
                    "你认为哪些维度的分析对业务最有价值？",
                    "对于可视化呈现方式，你有什么偏好？"
                ]
            }
        }
    elif style == LeadershipStyle.S3_PARTICIPATING:
        return {
            "type": "collaborative_discussion",
            "format": "提供目标和约束，与Agent讨论方案，共同决策",
            "detail_level": "medium-low",
            "autonomy_level": "medium-high",
            "instruction": {
                "task": task_description,
                "objective": f"完成「{task_description}」，确保分析结论具有业务洞察力",
                "discussion_points": [
                    f"对于「{task_description}」，你计划采用什么样的分析框架？",
                    "数据维度和指标选取方面，你有哪些想法？",
                    "可视化方案倾向于哪种风格？交互式还是静态报告？"
                ],
                "decision": "我们将共同讨论后确定最终的分析方案和呈现方式"
            }
        }
    else:  # S4_DELEGATING
        return {
            "type": "full_delegation",
            "format": "仅提供高层目标，由Agent自主决定执行方式",
            "detail_level": "low",
            "autonomy_level": "high",
            "instruction": {
                "task": task_description,
                "objective": f"完成「{task_description}」",
                "success_metrics": [
                    "报告内容准确、结论有业务价值",
                    "可视化清晰直观",
                    "按时交付"
                ],
                "note": "具体分析方法、工具选择、呈现方式均由你全权决定"
            }
        }


# ============================================================================
# 4. 模拟执行函数
# ============================================================================

def execute_task(
    agent: Agent,
    task: Task,
    style: LeadershipStyle,
    config: Dict
) -> ExecutionResult:
    """
    模拟执行任务

    ⚠️ 注意：此函数为模拟实现，所有结果均为随机生成。
    ⚠️ 真实部署时，应替换为 LLM API 调用。

    模拟逻辑：
    1. 根据 Agent 准备度和领导风格计算基础成功率
    2. 加入随机扰动
    3. 生成随机的 token 消耗

    参数:
        agent: 执行任务的 Agent
        task: 待执行的任务
        style: 选择的领导风格
        config: 配置参数

    返回:
        ExecutionResult: 执行结果
    """
    # 模拟数据，未调用真实 LLM
    print(f"\n{'='*60}")
    print(f"📋 模拟执行任务: {task.description}")
    print(f"{'='*60}")

    # 获取指令模板（根据风格和实际任务动态生成）
    instruction_template = get_instruction_template(style, task.description)

    # 计算准备度
    gamma = config["readiness_calculation"]["gamma"]
    readiness = agent.get_readiness(gamma)

    # 打印决策日志
    print(f"\n📊 决策日志:")
    print(f"   Agent: {agent.name} ({agent.agent_id})")
    print(f"   - HTSR (历史成功率): {agent.htsr:.2%}")
    print(f"   - Confidence (置信度): {agent.confidence:.2%}")
    print(f"   - Readiness (准备度): {readiness:.2%}")
    print(f"   - Task Uncertainty (不确定性): {task.uncertainty:.2%}")
    print(f"\n🎯 风格选择: {style.value}")

    # 打印指令模板
    print(f"\n📝 指令模板:")
    print(f"   类型: {instruction_template['type']}")
    print(f"   详细程度: {instruction_template['detail_level']}")
    print(f"   自主程度: {instruction_template['autonomy_level']}")
    print(f"\n   指令内容:")
    example = instruction_template['instruction']
    for key, value in example.items():
        if isinstance(value, list):
            print(f"   {key}:")
            for item in value[:3]:  # 只显示前3项
                print(f"     - {item}")
            if len(value) > 3:
                print(f"     - ... (共{len(value)}项)")
        else:
            print(f"   {key}: {value}")

    # 模拟执行结果
    # 基础成功率 = 0.5 + 0.4 * readiness + 0.1 * (1 - task_uncertainty)
    base_success_rate = 0.5 + 0.4 * readiness + 0.1 * (1 - task.uncertainty)

    # 添加风格匹配度调整
    # 高准备度 + 低指导性风格 = 更高成功率
    style_bonus = {
        LeadershipStyle.S1_TELLING: -0.05,
        LeadershipStyle.S2_SELLING: 0.0,
        LeadershipStyle.S3_PARTICIPATING: 0.05,
        LeadershipStyle.S4_DELEGATING: 0.1
    }

    # 风格匹配度：如果高准备度用高指导性风格，反而降低效率
    if readiness > 0.7 and style in [LeadershipStyle.S1_TELLING, LeadershipStyle.S2_SELLING]:
        style_match_penalty = -0.1
    elif readiness < 0.4 and style in [LeadershipStyle.S3_PARTICIPATING, LeadershipStyle.S4_DELEGATING]:
        style_match_penalty = -0.15
    else:
        style_match_penalty = 0.0

    # 最终成功率
    success_rate = np.clip(
        base_success_rate + style_bonus[style] + style_match_penalty + random.uniform(-0.1, 0.1),
        0.0, 1.0
    )

    # 模拟数据，未调用真实 LLM
    success = random.random() < success_rate
    tokens_consumed = random.randint(
        config["simulation_settings"]["token_range"][0],
        config["simulation_settings"]["token_range"][1]
    )

    # 生成执行日志
    execution_log = f"""
模拟执行日志 (SIMULATED - NOT REAL LLM CALL):
----------------------------------------------
Agent: {agent.name}
Task: {task.description}
Style: {style.value}
Readiness: {readiness:.2%}
Success Rate (calculated): {success_rate:.2%}
Result: {'SUCCESS' if success else 'FAILURE'}
Tokens Consumed: {tokens_consumed}
----------------------------------------------
⚠️ 以上数据为模拟生成，未调用真实LLM API
"""

    print(f"\n📈 执行结果:")
    print(f"   成功率计算: {success_rate:.2%}")
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    print(f"   Token 消耗: {tokens_consumed}")

    return ExecutionResult(
        success=success,
        tokens_consumed=tokens_consumed,
        style_used=style,
        readiness_score=readiness,
        task_uncertainty=task.uncertainty,
        instruction_template=instruction_template,
        execution_log=execution_log
    )


# ============================================================================
# 5. 主函数
# ============================================================================

def main():
    """
    AOM-Lite MVP 主函数

    演示流程：
    1. 加载配置
    2. 创建多个不同能力的 Agent
    3. 创建一个任务
    4. 对每个 Agent 计算准备度、选择风格、模拟执行
    5. 输出完整的决策日志
    """
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    AOM-Lite MVP 演示                            ║
║        情境领导风格动态切换原型 (模拟版本)                        ║
║                                                                  ║
║  ⚠️  所有执行结果均为模拟数据，未调用真实 LLM API                 ║
╚══════════════════════════════════════════════════════════════════╝
""")

    # 加载配置
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)["aom_lite_config"]
        print("✅ 配置文件加载成功\n")
    except FileNotFoundError:
        print("❌ 错误：未找到 config.json 文件")
        print("请确保 config.json 与 main.py 在同一目录下")
        return

    # 创建不同能力水平的 Agent
    # 模拟数据，未调用真实 LLM
    agents = [
        Agent(
            agent_id="agent_001",
            name="新手Agent",
            htsr=0.2,          # 历史成功率低
            confidence=0.3,     # 自信度低
            capability_description="刚加入团队的新手，经验有限"
        ),
        Agent(
            agent_id="agent_002",
            name="成长期Agent",
            htsr=0.5,          # 历史成功率中等
            confidence=0.6,     # 自信度中等
            capability_description="有一定经验，正在快速成长"
        ),
        Agent(
            agent_id="agent_003",
            name="资深Agent",
            htsr=0.85,         # 历史成功率高
            confidence=0.9,     # 自信度高
            capability_description="经验丰富，能力全面"
        ),
        Agent(
            agent_id="agent_004",
            name="专家Agent",
            htsr=0.95,         # 历史成功率很高
            confidence=0.95,    # 自信度很高
            capability_description="领域专家，可完全自主工作"
        ),
    ]

    # 创建任务
    # 模拟数据，未调用真实 LLM
    task = Task(
        task_id="task_001",
        description="分析用户行为数据并生成可视化报告",
        uncertainty=0.4  # 中等不确定性
    )

    print(f"📋 任务信息:")
    print(f"   ID: {task.task_id}")
    print(f"   描述: {task.description}")
    print(f"   不确定性: {task.uncertainty:.2%}")
    print(f"\n👥 Agent 列表: {len(agents)} 个")

    # 对每个 Agent 执行任务
    results = []
    for agent in agents:
        # 计算准备度
        gamma = config["readiness_calculation"]["gamma"]
        readiness = agent.get_readiness(gamma)

        # 选择领导风格
        style = select_leadership_style(
            readiness,
            task.uncertainty,
            config["readiness_thresholds"]
        )

        # 执行任务
        result = execute_task(agent, task, style, config)
        results.append((agent, result))

    # 输出汇总报告
    print("\n" + "=" * 70)
    print("📊 汇总报告")
    print("=" * 70)
    print(f"\n⚠️  以下数据均为模拟生成，未调用真实 LLM API\n")
    print(f"{'Agent':<15} {'Readiness':<12} {'Style':<18} {'Result':<10} {'Tokens':<10}")
    print("-" * 65)

    for agent, result in results:
        print(f"{agent.name:<15} "
              f"{result.readiness_score:<12.2%} "
              f"{result.style_used.value:<18} "
              f"{'✅ 成功' if result.success else '❌ 失败':<10} "
              f"{result.tokens_consumed:<10}")

    # 统计
    success_count = sum(1 for _, r in results if r.success)
    total_tokens = sum(r.tokens_consumed for _, r in results)

    print("-" * 65)
    print(f"总计: {success_count}/{len(results)} 成功, "
          f"消耗 {total_tokens} tokens")

    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)

    print("""
📌 下一步改进方向：

1. 替换为真实 LLM API 调用：
   - 在 execute_task() 函数中，将随机结果替换为实际的 API 调用
   - 示例（使用 OpenAI API）：

     from openai import OpenAI
     client = OpenAI()

     response = client.chat.completions.create(
         model="gpt-4",
         messages=[
             {"role": "system", "content": "你是一个专业的数据分析助手"},
             {"role": "user", "content": f"请执行以下任务：{task.description}"}
         ]
     )

     result = response.choices[0].message.content
     tokens = response.usage.total_tokens

2. 实现 HTSR 的实际计算：
   - 记录每次任务的执行结果
   - 计算滑动窗口内的成功率

3. 添加 LangGraph 集成：
   - 将风格选择逻辑集成到 LangGraph 的状态机中
   - 实现动态的风格切换

4. 添加持久化：
   - 将执行日志保存到数据库
   - 支持历史查询和分析
""")


# ============================================================================
# 6. 程序入口
# ============================================================================

if __name__ == "__main__":
    main()
