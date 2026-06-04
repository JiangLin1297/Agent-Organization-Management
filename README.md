# 智能体组织管理学（Agent Organizational Management, AOM）

**当多智能体系统遇上管理理论**

*不是用 AI 管人，是用管理学管 AI。*

预印本 | Foundational Preprint | Version 5.4 | 2026-06-04

> 📖 [Read this in English](README_EN.md)

---

## 🆕 V5.4 Released (2026-06-04)

**V5.4 核心升级：问题驱动理论版 — 现实基线 — 理论命题化**

核心变化：论文从"系统+实验"叙事重构为"问题驱动的理论论文"，新增现实系统基线和理论命题。

### 关键更新

1. **问题驱动叙事**：Abstract和Introduction重构为CAE问题→洞察→方法→结果结构
2. **理论命题化**：新增3个理论命题（CAE二次方增长、CDE线性化、现实基线差距）
3. **现实基线（条件E）**：模拟AutoGen/CrewAI风格系统的对比实验
4. **统一数值**：所有文档统一使用"≈2.0x缩减"和"≈25-30%额外节省"
5. **强化结论**：明确"组织结构是一等计算原语"的核心主张

### 实验结果（V5.4 完整对比）

| 条件 | DeepSeek Mean±Std | MiMo Mean±Std | 说明 |
|------|-------------------|---------------|------|
| A（单Agent） | 6,000±254 | 8,251±0 | 单次调用基线 |
| B（迭代7轮） | 90,437±9,653 | 102,417±1,547 | CAE显现 |
| C（OIMAC+CC） | 45,581±3,082 | 48,468±1,445 | 结构化分解+有界上下文 |
| D（OIMAC-CC） | 60,894±2,319 | 61,805±1,691 | 结构化分解，无上下文限制 |
| **E（现实基线）** | **64,634±3,644** | **~67,200*** | 模拟AutoGen/CrewAI架构 |

*MiMo条件E为基于跨模型比率的估计值

### 核心效率对比

- **C/B ≈ 2.0x**：OIMAC vs 迭代精炼（p<0.001, d>5.6）
- **C/E ≈ 1.4x**：OIMAC vs 现实多智能体基线
- **D/C ≈ 1.3x**：上下文控制器额外贡献（≈25-30%）
- **CDE贡献**：~70%（主驱动）
- **CC贡献**：~30%（次级机制）

### 核心主张

**效率增益来自重构计算，而非减少上下文。组织结构是一等计算原语。**

> 📊 完整报告：[REPORT_V5.3.md](REPORT_V5.3.md)

---

## V5.3 Released (2026-06-04)

**V5.3 核心升级：统计验证 — 质量评估 — 多任务泛化 — 可投稿实验**

核心变化：实验从"单次案例展示"升级为"具有统计显著性的可投稿实验"。

### 关键更新

1. **统计重复**：每个条件5次重复运行（DeepSeek + MiMo），共40次实验
2. **t-test验证**：所有关键比较 p < 0.001，Cohen's d > 4.6（极大效应量）
3. **质量评估**：5维度自动化质量检查，所有输出 20-24/25 分
4. **多任务泛化**：新增数据分析任务（24次运行），效率比率跨任务一致
5. **总实验量**：64次独立运行（40次Task1 + 24次Task2）

---

## V5.2 Released (2026-06-03)

**V5.2 核心升级：机制分解 — 跨模型验证 — ICIS/AAAI投稿就绪**

核心变化：论文从"方法论文"升级为"机制论文"，通过跨模型实验验证机制分解。

### 关键更新

1. **机制分解**：效率增益分解为主驱动（CDE，~70%）和次级机制（Context Controller，~30%）
2. **跨模型验证**：在 DeepSeek 和 MiMo 两个异质模型上复现实验
3. **双任务验证**：拼豆图生成器（code-heavy）+ 数据分析报告（analysis-heavy）
4. **核心发现**：效率增益主要来自重构计算结构（restructuring computation），而非减少上下文（reducing context）

---

## V5.0 Released (2026-06-02)

**V5.0 核心内容：机制-算法-系统三层整合**

1. **机制层**：形式化五个结构性效率机制（CAE/CDE/IRC/COS/AVT），含假设、因果链、边界条件
2. **成本模型**：TotalCost = ComputationCost + CoordinationCost + CommunicationCost，含最优团队大小k*推导
3. **OIMAC算法**：完整7-Phase伪代码，含可计算决策规则（SPLIT/MERGE/CENTRALIZE/STYLE_DOWNGRADE/CONTEXT_LIMIT）
4. **系统架构**：九模块可实现设计，CAE避免机制

---

## V4.0 Released (2026-06-02)

**V4.0 核心新增内容：三组对照实验——证明组织管理学的实证价值**

1. **三组对照实验设计**：对照组A（单Agent单次）、对照组B（单Agent迭代7轮）、实验组（6角色组织团队）
2. **核心发现——组织管理的双重价值**：实验组以42,166 Token完成任务，迭代方案消耗124,280 Token（3:1优势），同时代码质量更优

---

## V3.0 Released (2026-06-01)

1. **大规模真实实验（N=60）**：15个任务 × 2条件 × 2重复
2. **重要发现——自主性-冗长度权衡**：AOM-DT消耗更多Token但保持同等成功率和质量

---

## 前言 / Preface

多年以后，面对数以百计的 AI Agent 井然有序地协作时，我将会想起，那个在课堂上第一次意识到管理学或许是为它们而生的遥远下午。

你们好，我是华南理工大学的一名学生。我所修的专业，软件工程+工商管理双学位，在我刚入学时便被人议论纷纷。他们都说管理学是一个无用的学科，只有软件才有出路，才能找到工作。

但奇怪的是，当我在学校学 C++、数据结构、操作系统的时候，Agent 出现了。从平时的作业到实验课的内容，甚至是期末考前的复习，Agent 通通可以完成。那当数据继续喂进 AI 的知识库中，还有什么是 Agent 做不到的？

于是我开始思考：现在 Agent 是我们的"员工"，那为什么适用于人类员工的管理学，不能套用在 Agent 之上呢？

这个念头击中了我。它再也没有离开过。我花了一个月，和 AI，和 Agent，和我的"数字员工"一起：把法约尔、韦伯、明茨伯格这些管理学大师的理论，一个一个地"翻译"成多智能体系统的协作逻辑。没有导师，没有团队，没有经费。只有一台电脑，一个想法，和几个愿意与我一起探索的 AI 助手。

因此，我写下了这篇文章。它或许粗糙，但它是我——一个曾经被嘲笑"学无用学科"的学生——给这个时代交出的第一份答卷。

管理学被说无用太久了。现在，让我们看看它能不能管住 AI。

**江皓然**
华南理工大学 软件工程+工商管理双学位 本科二年级
2026年5月30日

---

## 摘要 / Abstract

**问题**：基于LLM的多智能体系统存在上下文积累效应（CAE）——迭代式自我改进导致Token消耗以O(n²)增长，这是结构性成本病理，非实现低效。

**洞察**：问题根源不是"上下文太多"，而是计算结构错误。重构计算比减少上下文更有效。

**方法**：提出OIMAC，将单体迭代重构为多角色流水线，通过上下文控制器强制有界上下文传递。

**结果**：
- ≈2.0x Token缩减（vs 迭代，p<0.001, d>5.6）
- ≈1.4x Token缩减（vs 现实基线AutoGen/CrewAI风格）
- 跨模型（DeepSeek + MiMo）、跨任务（HTML + 数据分析）一致
- 质量无损（20-24/25分）
- 机制分解：CDE≈70%, CC≈30%

**核心主张**：效率增益来自重构计算，而非减少上下文。组织结构是一等计算原语。

---

## 核心贡献 / Core Contributions

**V5.4 贡献（问题驱动理论版）：**
- (1) CAE形式化：证明迭代式LLM自我改进产生Ω(n²) Token成本增长
- (2) 机制分解：CDE（~70%）+ Context Controller（~30%），实证验证
- (3) OIMAC结构性解决方案：将Ω(n²)降至O(k)，p<0.001, d>5.6
- (4) 现实基线对比：优于AutoGen/CrewAI风格架构，≈1.4x进一步降低

---

## 文件结构 / Repository Structure

```
├── README.md                           # 本文件（中文）
├── README_EN.md                        # 英文版 README
├── LICENSE
│
├── paper/
│   ├── main/
│   │   ├── AOM_paper_v5.3.docx        # V5.4 主论文（中文）
│   │   ├── AOM_paper_v5.3_en.docx     # V5.4 纯英文版
│   │   └── generate_v5.3.py           # 论文生成脚本
│   ├── sections/
│   │   ├── v5.4_abstract.md           # V5.4 Abstract
│   │   ├── v5.4_introduction.md       # V5.4 Introduction
│   │   ├── v5.4_propositions.md       # V5.4 理论命题
│   │   └── v5.4_conclusion.md         # V5.4 Conclusion
│   ├── supplementary.zip
│   ├── figures/
│   ├── supplement/
│   └── archive/                        # V1-V4 存档
│
├── algorithm/
│   └── OIMAC_Framework.docx            # OIMAC算法框架
│
├── system/
│   ├── architecture_spec.docx          # 系统架构规范
│   └── module_spec.docx                # 机制-模块映射表
│
├── aom-lite_MVP/                       # AOM-Lite MVP 原型代码
│   ├── main.py
│   ├── config.json
│   └── v4_experiment/                  # V4三组对照实验
│
└── experiments/                        # 实验数据与结果
    ├── OIMAC_experiment_Pixel/         # V5.2 跨模型实验（拼豆图）
    ├── v5_repeated/                    # V5.3/V5.4 统计重复实验
    │   ├── run_condition_E.py          # 条件E（现实基线）实验脚本
    │   ├── condition_E_summary.json    # 条件E结果
    │   └── ...
    ├── v5_task2/                       # V5.3 泛化任务实验
    ├── v3_results/                     # V3 历史实验数据
    └── v4_results/                     # V4 历史实验数据
```

---

## 快速开始 / Quick Start

### 运行 V5.4 条件E实验（现实基线）

```bash
cd experiments/v5_repeated
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# 运行条件E实验
python run_condition_E.py deepseek
python run_condition_E.py mimo
```

### 运行 V5.3 统计重复实验

```bash
cd experiments/v5_repeated
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# 运行5次重复实验（两个模型）
python run_repeated.py all

# 查看统计结果
cat results_summary.csv
```

### 运行 AOM-Lite MVP

```bash
cd aom-lite_MVP
pip install -r requirements.txt
python main.py
```

---

## 如何引用 / How to Cite

### 中文引用格式

> 江皓然. (2026). 智能体组织管理学：当多智能体系统遇上管理理论 (Version 5.4). 奠基性预印本. GitHub.

### 英文引用格式

> Jiang, H. (2026). Agent Organizational Management: When Multi-Agent Systems Meet Management Theory (Version 5.4). Foundational Preprint. GitHub.

### BibTeX

```bibtex
@unpublished{jiang2026aom,
  author    = {Haoran Jiang},
  title     = {Agent Organizational Management: When Multi-Agent Systems Meet Management Theory},
  note      = {Foundational Preprint, Version 5.4},
  year      = {2026},
  month     = jun,
  url       = {https://github.com/JiangLin1297/Agent-Organization-Management}
}
```

---

## 共建邀请 / Call for Collaboration

这是一个开放的领域。无论您是管理学教授、AI 研究员、工程师，还是像我一样对这个交叉点充满热情的学生，我都诚挚邀请您：

- 阅读并评论论文
- 提交 Issue 指出错误或提出改进建议
- Fork 仓库并在此基础上发展您自己的研究方向

让我们一起，将智能体组织管理学从愿景推向现实。

---

## 许可证 / License

学术内容（论文文本）遵循 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可。代码部分遵循 [MIT License](https://opensource.org/licenses/MIT)。

---

## 联系 / Contact

- 作者：江皓然
- 学校：华南理工大学
- 专业：软件工程 + 工商管理双学位
- Email：JiangLin1297@163.com / JiangLin1297@gmail.com
- GitHub：@JiangLin1297

---

*"管理学的下一个百年，属于算法。"*
