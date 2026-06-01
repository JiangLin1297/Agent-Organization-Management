# 智能体组织管理学（Agent Organizational Management, AOM）

**当多智能体系统遇上管理理论**

*不是用 AI 管人，是用管理学管 AI。*

预印本 | Foundational Preprint | Version 3.0 | 2026-06-01

> 📖 [Read this in English](README_EN.md)

---

## 🆕 V3.0 Released (2026-06-01)

**V3.0 核心新增内容：大规模效率实验与诚实发现**

1. **大规模真实实验（N=90）**：4个异质Agent × 9任务 × 2条件 × 5重复 = 90次实验，360次LLM调用
2. **效率指标深度分析**：Token消耗、完成时间、协调开销的系统性测量
3. **重要发现——自主性-冗长度权衡**：AOM-DT消耗更多Token（+5~11%）但保持同等成功率和质量
4. **诚实的学术态度**：不回避反直觉结果，深入分析机制并提出改进方向
5. **完整可视化**：Token对比图、时间对比图、Agent Token分布散点图
6. **V3论文（DOCX格式）**：包含效率分析、自主性-冗长度权衡讨论、改进路径

---

## V2.0 Released (2026-05-30)

**V2.0 核心新增内容：**

1. **相关工作与领域定位（§1.3）**：与 Chain-of-Thought、MARL、可扩展监督、ONA 等主流方法的系统性对比，明确 AOM 的独特价值定位
2. **映射中涌现的新理论观察（§2.4）**：提出"控制-涌现平衡猜想"等 AOM 原创假设，为管理学提供可验证的数学命题
3. **实验验证框架与模拟数据（§3）**：1,900 次模拟实验设计，验证动态拓扑在多种任务场景下的优势
4. **系统性局限性清单（§4）**：坦诚列出 10 条学科局限性及对应的缓解路径
5. **AOM-Lite MVP 即刻行动计划（§5.2）**：48 小时可搭建的情境领导风格动态切换原型设计

---

## 前言 / Preface

多年以后，面对数以百计的 AI Agent 井然有序地协作时，我将会回想起，那个在课堂上第一次意识到管理学或许是为它们而生的遥远下午。

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

当人工智能代理（AI Agent）从孤立的工具演化为"数字员工"时，管理它们的最优解不再是编程，而是管理学本身。当前主流的多智能体框架（如 AutoGen、CrewAI、LangGraph）普遍存在"管理真空"——协作流程以静态拓扑硬编码，缺乏权变响应能力。

本文首次系统性地提出并界定一个全新的交叉学科领域——智能体组织管理学（Agent Organizational Management, AOM）。核心主张是：管理学百年来关于组织结构、领导力、激励机制的智慧，能被精确地"编译"为多智能体系统的原生协作协议。论文构建了完整的映射框架：将韦伯的科层制与明茨伯格的构型理论映射为 Agent 拓扑设计；将赫塞-布兰查德的情境领导理论工程化为动态控制逻辑；将德鲁克的目标管理与弗鲁姆的期望理论转化为目标函数与注意力分配机制。

本文进一步论证，AOM 不仅是"用管理学管 AI"，更开启了反向赋能路径：通过大规模 Agent 仿真，管理学首次获得可控、可重复的实验能力，从而检验并发展自身。最后，论文坦诚界定了学科边界，并描绘了学科与产品的十年愿景。

本文的核心论断是：AI 时代的管理学，不再仅是研究人的学问，更是设计智能体社会的工程科学。

---

## 核心贡献 / Core Contributions

- ✅ 首次提出智能体组织管理学（AOM）的完整概念与研究纲领
- ✅ 将法约尔 14 项原则、韦伯科层制、明茨伯格构型理论精确映射为 Agent 拓扑设计
- ✅ 将情境领导理论工程化为动态领导风格切换算法（包含可计算的"准备度"指标）
- ✅ 将目标管理（MBO）与期望理论编译为目标函数与资源分配机制
- ✅ 提出双向赋能路径：用 Agent 仿真作为管理学的"粒子对撞机"
- ✅ 坦诚界定学科适用边界，指出控制与涌现的根本张力
- ✅ 给出产品化愿景：基于管理架构的 Agent 工作台（MAW）
- ✅ **[v2.0 新增]** 相关工作定位：与 COT、MARL、可扩展监督、ONA 的系统性对比
- ✅ **[v2.0 新增]** 理论创新：提出"控制-涌现平衡猜想"等 AOM 原创假设
- ✅ **[v2.0 新增]** 最小可行性实验设计：1,900 次模拟实验验证动态拓扑优势
- ✅ **[v2.0 新增]** 系统性局限性分析：10 条局限性及缓解路径
- ✅ **[v2.0 新增]** 最小产品原型：AOM-Lite Weekend Hackathon MVP 设计

---

## 文件结构 / Repository Structure

```
├── README.md                                              # 本文件
├── README_EN.md                                           # 英文版 README
├── paper/
│   ├── agent_organizational_management_v3.docx            # 论文全文（预印本 v3.0）🆕
│   ├── agent_organizational_management_v2.docx            # 论文全文（预印本 v2.0）
│   ├── agent_organizational_management_v2_en.docx         # 论文英文版（预印本 v2.0）
│   ├── agent_organizational_management_v1.docx            # 论文全文（预印本 v1.0）
│   ├── generate_v3_paper.py                               # V3论文生成脚本 🆕
│   └── v1_supplement_five_dimensions.md                   # v2.0 五维度补充材料原文
├── simulations/
│   ├── control_emergence_plot.py                          # 控制-涌现平衡猜想数值模拟脚本
│   ├── control_emergence_surface.png                      # 三维曲面图
│   └── control_emergence_contour.png                      # 二维等高线图
├── aom-lite/
│   ├── main.py                                            # AOM-Lite MVP 主程序
│   ├── experiment_v3.py                                   # V3大规模实验脚本 🆕
│   ├── generate_v3_charts.py                              # V3可视化脚本 🆕
│   ├── experiment_v3_results.csv                          # V3实验结果（90次）🆕
│   ├── config.json                                        # 配置文件
│   ├── requirements.txt                                   # 依赖列表
│   └── RUN_RESULT.md                                      # AOM-Lite 运行结果日志
├── LICENSE                                                # 开源许可证
└── assets/
    ├── v3_token_comparison.png                            # Token对比柱状图 🆕
    ├── v3_time_comparison.png                             # 时间对比柱状图 🆕
    └── v3_agent_token_distribution.png                    # Agent Token分布散点图 🆕
```

---

## 快速开始 / Quick Start

### 运行控制-涌现平衡猜想模拟

```bash
cd simulations
pip install matplotlib numpy scipy
python control_emergence_plot.py
```

### 运行 AOM-Lite MVP 原型

```bash
cd aom-lite
pip install -r requirements.txt
python main.py
```

### 运行 V3 大规模实验

```bash
cd aom-lite
export OPENAI_API_KEY=your_key
export OPENAI_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
python experiment_v3.py        # 运行90次实验（约2小时）
python generate_v3_charts.py   # 生成可视化图表
```

---

## 如何引用 / How to Cite

若本文对您的研究有帮助，请按以下格式引用：

### 中文引用格式

> 江皓然. (2026). 智能体组织管理学：当多智能体系统遇上管理理论 (Version 3.0). 奠基性预印本. GitHub. URL: https://github.com/JiangLin1297/Agent-Organization-Management

### 英文引用格式

> Jiang, H. (2026). Agent Organizational Management: When Multi-Agent Systems Meet Management Theory (Version 2.0). Foundational Preprint. GitHub. URL: https://github.com/JiangLin1297/Agent-Organization-Management

### BibTeX

```bibtex
@unpublished{jiang2026aom,
  author    = {Haoran Jiang},
  title     = {Agent Organizational Management: When Multi-Agent Systems Meet Management Theory},
  note      = {Foundational Preprint, Version 2.0},
  year      = {2026},
  month     = may,
  url       = {https://github.com/JiangLin1297/Agent-Organization-Management}
}
```

---

## 共建邀请 / Call for Collaboration

这是一个开放的领域。无论您是管理学教授、AI 研究员、工程师，还是像我一样对这个交叉点充满热情的学生，我都诚挚邀请您：

- 📖 阅读并评论论文
- 🐛 提交 Issue 指出错误或提出改进建议
- 🔀 Fork 仓库并在此基础上发展您自己的研究方向
- ✉️ 通过 Discussions 或邮件与我联系

让我们一起，将智能体组织管理学从愿景推向现实。

---

## 许可证 / License

本仓库的学术内容（论文文本）遵循 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可。代码部分（如有）遵循 [MIT License](https://opensource.org/licenses/MIT)。

---

## 联系 / Contact

- 作者：江皓然
- 学校：华南理工大学
- 专业：软件工程 + 工商管理双学位
- Email：JiangLin1297@163.com / JiangLin1297@gmail.com
- GitHub：@JiangLin1297

---

*"管理学的下一个百年，属于算法。"*
