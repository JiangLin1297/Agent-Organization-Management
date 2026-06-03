# 智能体组织管理学（Agent Organizational Management, AOM）

**当多智能体系统遇上管理理论**

*不是用 AI 管人，是用管理学管 AI。*

预印本 | Foundational Preprint | Version 5.2 | 2026-06-03

> 📖 [Read this in English](README_EN.md)

---

## 🆕 V5.2 Released (2026-06-03)

**V5.2 核心升级：机制分解 — 跨模型验证 — ICIS/AAAI投稿就绪**

核心变化：论文从"方法论文"升级为"机制论文"，通过跨模型实验验证机制分解。

### 关键更新

1. **机制分解**：效率增益分解为主驱动（CDE，~75%）和次级机制（Context Controller，~25%）
2. **跨模型验证**：在 DeepSeek 和 MiMo 两个异质模型上复现实验
3. **双任务验证**：贪吃蛇（code-heavy, single-chain）+ 拼豆图生成器（vision+layout, multi-interface）
4. **核心发现**：效率增益主要来自重构计算结构（restructuring computation），而非减少上下文（reducing context）
5. **新实验章节**：7.1 Tasks, 7.2 Conditions, 7.3 Results, 7.4 Mechanism Decomposition, 7.5 CAE Validation, 7.6 Cross-Model Robustness, 7.7 IRC Evidence
6. **四点贡献**：(1) CAE识别 (2) 机制分解 (3) OIMAC协议 (4) 跨模型验证

### 实验结果（V5.2）

| 条件 | DeepSeek | MiMo | 均值 |
|------|----------|------|------|
| A（单Agent） | 6,587 | 8,251 | 7,419 |
| B（迭代7轮） | 88,494 | 102,105 | 95,300 |
| C（OIMAC+CC） | 43,321 | 49,285 | 46,303 |
| D（OIMAC-CC） | 58,718 | 63,050 | 60,884 |

- **C/B = 0.49**：OIMAC 降低迭代成本约 51%
- **D/C = 1.32**：Context Controller 提供约 24% 额外节省
- **CDE 贡献**：~75%（主驱动）
- **CC 贡献**：~25%（次级机制）
- **跨模型一致**：DeepSeek 和 MiMo 趋势一致，结论 model-agnostic

---

## V5.0 Released (2026-06-02)

**V5.0 核心内容：机制-算法-系统三层整合**

1. **机制层**：形式化五个结构性效率机制（CAE/CDE/IRC/COS/AVT），含假设、因果链、边界条件
2. **成本模型**：TotalCost = ComputationCost + CoordinationCost + CommunicationCost，含最优团队大小k*推导
3. **OIMAC算法**：完整7-Phase伪代码，含可计算决策规则（SPLIT/MERGE/CENTRALIZE/STYLE_DOWNGRADE/CONTEXT_LIMIT）
4. **系统架构**：九模块可实现设计，CAE避免机制
5. **CAE命题强化**：加入显式边界条件(a)(b)，证明逻辑链更严格
6. **机制隔离论证强化**：明确定义自变量（上下文传递架构）和因变量（Token消耗）
7. **理论贡献强化**：情境领导理论/韦伯科层制/法约尔原则统一为(a)(b)(c)(d)结构
8. **文件夹重构**：paper/archive/存放V1-V4，paper/figures/按实验分类，experiments/独立存放
9. **主论文整合**：paper/main/AOM_paper_v5.2.docx 为最新主论文

---

## V4.0 Released (2026-06-02)

**V4.0 核心新增内容：三组对照实验——证明组织管理学的实证价值**

1. **三组对照实验设计**：对照组A（单Agent单次）、对照组B（单Agent迭代7轮）、实验组（6角色组织团队）
2. **核心发现——组织管理的双重价值**：实验组以42,166 Token完成任务，迭代方案消耗124,280 Token（3:1优势），同时代码质量更优
3. **Token膨胀根因分析**：迭代方案的Token成本呈指数增长——每轮改进必须嵌入前一版完整代码，形成正反馈循环
4. **测试环节的实证价值**：测试角色发现了四个由前端与游戏逻辑开发者接口不一致导致的阻断性Bug
5. **V4三组对照实验完整代码**：`aom-lite/v4_experiment/` 包含完整可运行脚本和Prompt文件

---

## V3.0 Released (2026-06-01)

1. **大规模真实实验（N=90）**：4个异质Agent × 9任务 × 2条件 × 5重复
2. **重要发现——自主性-冗长度权衡**：AOM-DT消耗更多Token但保持同等成功率和质量
3. **AOM最终愿景**：让每个人都能像管理公司一样管理自己的AI Agent团队

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

本文首次系统性地提出并界定智能体组织管理学（Agent Organizational Management, AOM）——一个将管理学理论计算化地实例化并压力测试为多智能体系统协作协议的交叉学科领域。

**V5.2 核心发现（机制分解）：**

效率增益可分解为：
- **主驱动（~75%）**：流水线式组织分解（CDE）结构性避免上下文积累效应
- **次级机制（~25%）**：Context Controller 提供有界上下文优化

跨模型验证：在 DeepSeek 和 MiMo 两个异质模型与两个异质任务中均一致成立。

**核心论断**：效率增益主要来自重构计算结构，而非减少上下文。

---

## 核心贡献 / Core Contributions

**V5.2 贡献（机制分解 + 跨模型验证）：**
- (1) CAE 识别：形式化证明迭代式 LLM 自我改进存在 Omega(n^2) 成本陷阱，跨模型验证
- (2) 机制分解：实证证明效率增益分解为 CDE（~75%）和 Context Controller（~25%）
- (3) OIMAC 作为可执行协议：完整多智能体协调算法，将迭代成本从 Omega(n^2) 降至 O(k)
- (4) 组织原则的跨模型验证：压力测试管理理论，提出领域特定修正

**V5.2 实验数据（DeepSeek / MiMo）：**
- 条件A：6,587 / 8,251 tokens
- 条件B：88,494 / 102,105 tokens
- 条件C：43,321 / 49,285 tokens
- 条件D：58,718 / 63,050 tokens
- C/B 比率：2.04x / 2.07x（OIMAC ~2x 优势）
- D/C 比率：1.36x / 1.28x（CC ~1.3x 额外节省）

**V1-V4 贡献：**
- 首次提出智能体组织管理学（AOM）的完整概念与研究纲领
- 将法约尔14项原则、韦伯科层制、明茨伯格构型理论映射为Agent拓扑设计
- V3大规模实验（N=90）：发现自主性-冗长度权衡
- V4三组对照实验：组织团队42,166 Token vs 迭代方案124,280 Token（3:1优势）

---

## 文件结构 / Repository Structure

```
├── README.md                           # 本文件（中文）
├── README_EN.md                        # 英文版 README
├── LICENSE
│
├── paper/
│   ├── main/
│   │   ├── AOM_paper_v5.2.docx        # V5.2 主论文（中英混合）
│   │   ├── AOM_paper_v5.2_en.docx     # V5.2 纯英文版
│   │   ├── AOM_paper_v5.2_HICSS.docx  # V5.2 HICSS格式英文版
│   │   └── AOM_paper_v5.docx          # V5.0/V5.1 存档
│   ├── sections/
│   │   └── section7_experiments.docx   # 第7节单独文档
│   ├── supplementary.zip              # 补充材料压缩包
│   ├── figures/
│   ├── supplement/
│   └── archive/                        # V1-V4 存档
│
├── experiment/                         # V5.2 跨模型实验
│   ├── config.py                       # 实验配置（需设置环境变量）
│   ├── run_all.py                      # 统一运行脚本
│   ├── REPORT.md                       # 实验分析报告
│   ├── deepseek/                       # DeepSeek 实验结果
│   │   ├── condition_A-D/              # 四个条件
│   │   └── summary.json
│   └── mimo/                           # MiMo 实验结果
│       ├── condition_A-D/
│       └── summary.json
│
├── algorithm/
│   └── OIMAC_Framework.docx            # OIMAC算法框架
│
├── system/
│   ├── architecture_spec.docx          # 系统架构规范
│   └── module_spec.docx                # 机制-模块映射表
│
├── aom-lite/                           # AOM-Lite MVP 原型代码
│   ├── main.py
│   ├── config.json
│   └── v4_experiment/                  # V4三组对照实验
│
└── experiments/                        # V3-V4 历史实验数据
    ├── v3_results/
    └── v4_results/
```

---

## 快速开始 / Quick Start

### 运行 V5.2 跨模型实验

```bash
cd experiment

# 设置环境变量
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# 运行 DeepSeek 实验（4个条件）
python run_all.py deepseek

# 运行 MiMo 实验（4个条件）
python run_all.py mimo

# 查看结果
cat deepseek/summary.json
cat mimo/summary.json
```

### 运行 AOM-Lite MVP

```bash
cd aom-lite
pip install -r requirements.txt
python main.py
```

---

## 如何引用 / How to Cite

### 中文引用格式

> 江皓然. (2026). 智能体组织管理学：当多智能体系统遇上管理理论 (Version 5.2). 奠基性预印本. GitHub.

### 英文引用格式

> Jiang, H. (2026). Agent Organizational Management: When Multi-Agent Systems Meet Management Theory (Version 5.2). Foundational Preprint. GitHub.

### BibTeX

```bibtex
@unpublished{jiang2026aom,
  author    = {Haoran Jiang},
  title     = {Agent Organizational Management: When Multi-Agent Systems Meet Management Theory},
  note      = {Foundational Preprint, Version 5.2},
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
