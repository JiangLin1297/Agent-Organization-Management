# Agent Organizational Management (AOM)

**When Multi-Agent Systems Meet Management Theory**

*Not using AI to manage people — using management theory to manage AI.*

Preprint | Foundational Preprint | Version 5.2 | 2026-06-03

> 📖 [Read this in English](README_EN.md)

---

## V5.2 Released (2026-06-03)

**V5.2: Mechanism Decomposition — Cross-Model Validation — ICIS/AAAI Ready**

Core upgrade: Paper reframed from "methods paper" to "mechanism paper" with cross-model experimental validation.

### Key Changes

1. **Mechanism Decomposition**: Efficiency gains decomposed into primary driver (CDE, ~75%) and secondary mechanism (Context Controller, ~25%)
2. **Cross-Model Validation**: Experiments replicated across DeepSeek and MiMo, two heterogeneous models
3. **Two Tasks**: Snake game (code-heavy, single-chain) + Perler bead pattern generator (vision+layout, multi-interface)
4. **Core Finding**: Efficiency gains come primarily from restructuring computation rather than reducing context
5. **New Experiment Section**: 7.1 Tasks, 7.2 Conditions, 7.3 Results, 7.4 Mechanism Decomposition, 7.5 CAE Validation, 7.6 Cross-Model Robustness, 7.7 IRC Evidence
6. **4-Point Contributions**: (1) CAE identification (2) Mechanism decomposition (3) OIMAC protocol (4) Cross-model validation

### Experiment Results (V5.2)

| Condition | DeepSeek | MiMo | Mean |
|-----------|----------|------|------|
| A (Single Agent) | 6,587 | 8,251 | 7,419 |
| B (Iterative 7 rounds) | 88,494 | 102,105 | 95,300 |
| C (OIMAC + CC) | 43,321 | 49,285 | 46,303 |
| D (OIMAC - CC) | 58,718 | 63,050 | 60,884 |

- **C/B = 0.49**: OIMAC reduces iterative cost by ~51%
- **D/C = 1.32**: Context Controller provides ~24% additional savings
- **CDE contribution**: ~75% of total efficiency gain
- **CC contribution**: ~25% of total efficiency gain
- **Model-agnostic**: Results consistent across DeepSeek and MiMo

---

## V5.0 Released (2026-06-02)

**V5.0 Core: Mechanism-Algorithm-System Integration**

1. **Mechanism Layer**: Formalization of five structural efficiency mechanisms (CAE/CDE/IRC/COS/AVT) with hypotheses, causal chains, boundary conditions
2. **Cost Model**: TotalCost = ComputationCost + CoordinationCost + CommunicationCost, with optimal team size k* derivation
3. **OIMAC Algorithm**: Complete 7-phase pseudocode with computable decision rules (SPLIT/MERGE/CENTRALIZE/STYLE_DOWNGRADE/CONTEXT_LIMIT)
4. **System Architecture**: Nine-module implementable design with CAE avoidance mechanism
5. **CAE Proposition**: Explicit boundary conditions (a)(b), strengthened proof logic
6. **Mechanism Isolation**: Clear definition of independent variable (context passing architecture) and dependent variable (Token consumption)
7. **Theory Contribution**: Situational leadership / Weber bureaucracy / Fayol principles unified as (a)(b)(c)(d) structure
8. **Folder Restructure**: paper/archive/ for V1-V4, paper/figures/ by experiment, experiments/ independent
9. **Main Paper**: paper/main/AOM_paper_v5.docx as single main paper

---

## V4.0 Released (2026-06-02)

**V4.0 Core: Three-Group Controlled Experiment — Proving Organizational Management Value**

1. **Three-Group Experiment**: Control Group A (single agent single call), Control Group B (single agent 7 iterations), Experimental Group (6-role organizational team)
2. **Core Finding — Dual Value of Organizational Management**: Experimental group completes task with 42,166 tokens, iterative approach consumes 124,280 tokens (3:1 advantage), while achieving superior code quality
3. **Token Explosion Root Cause**: Iterative approach shows exponential token growth — each improvement round must embed the complete previous code, forming a positive feedback loop; organizational decomposition avoids this structural defect through role specialization
4. **Empirical Value of Testing**: Testing role discovered 4 blocking bugs caused by frontend-game logic interface inconsistencies — impossible to discover in single-agent workflows
5. **V4 Paper (DOCX)**: Section 3 completely rewritten with V4 experiment as main body, including 6 data tables, code quality comparison, token explosion formula analysis
6. **V3→V4 Experiment Complementarity**: V3 proves style matching has limited efficiency gains, V4 proves organizational structure has significant quality and efficiency gains — AOM should prioritize structural principles over style adaptation
7. **V4 Experiment Code**: `aom-lite/v4_experiment/` contains complete runnable scripts and prompt files for all three conditions
8. **Bilingual Papers**: V4 Chinese and English versions updated simultaneously

---

## V3.0 Released (2026-06-01)

**V3.0 Core: Large-Scale Efficiency Experiment and Honest Findings**

1. **Large-Scale Real Experiment (N=90)**: 4 heterogeneous Agents × 9 tasks × 2 conditions × 5 repetitions
2. **Important Finding — Autonomy-Verbosity Trade-off**: AOM-DT consumes more tokens but maintains equal success rate and quality
3. **Version Evolution Analysis (S5.1.1)**: Systematic review of V1->V2->V3 evolution logic
4. **Theoretical Solution to Autonomy-Verbosity Trade-off (S2.5)**: Four prompt design principles
5. **AOM Ultimate Vision**: Enable everyone to manage their AI Agent team like managing a company

---

## V2.0 Released (2026-05-30)

**V2.0 Core Additions:**

1. **Related Work and Domain Positioning (S1.3)**: Systematic comparison with Chain-of-Thought, MARL, scalable supervision, ONA and other mainstream methods, clarifying AOM's unique value proposition
2. **New Theoretical Observations from Mapping (S2.4)**: Proposing "control-emergence balance conjecture" and other AOM-original hypotheses, providing verifiable mathematical propositions for management science
3. **Experimental Validation Framework and Simulation Data (S3)**: 1,900 simulation experiment design, validating dynamic topology advantages across multiple task scenarios
4. **Systematic Limitations List (S4)**: Honestly listing 10 disciplinary limitations with corresponding mitigation paths
5. **AOM-Lite MVP Immediate Action Plan (S5.2)**: 48-hour buildable situational leadership style dynamic switching prototype design

---

## Preface

Years later, facing hundreds of AI Agents collaborating in orderly fashion, I will recall the distant afternoon when I first realized that management science might have been designed for them.

Hello, I am a student from South China University of Technology. My dual degree in Software Engineering + Business Administration was often dismissed as useless — they said only software has a future, only software can find jobs.

But strangely, when I was learning C++, data structures, and operating systems, Agents appeared. From daily assignments to lab experiments, even final exam reviews, Agents could handle everything. So as data continues to feed into AI's knowledge base, what can't Agents do?

So I began to think: now Agents are our "employees," why can't management theory that applies to human employees be applied to Agents?

This thought struck me. It never left. I spent a month with AI, with Agents, with my "digital employees": translating the theories of Fayol, Weber, Mintzberg — these management masters — one by one into multi-agent system collaboration logic. No advisor, no team, no funding. Just a computer, an idea, and a few AI assistants willing to explore with me.

So I wrote this paper. It may be rough, but it is the first答卷 I, a student once mocked for studying a "useless discipline," submit to this era.

Management has been called useless for too long. Now, let's see if it can manage AI.

**Haoran Jiang**
South China University of Technology, Software Engineering + Business Administration Dual Degree, Second Year Undergraduate
May 30, 2026

---

## Abstract

When AI Agents evolve from isolated tools to "digital employees," the optimal solution for managing them is not programming — it is management itself. Current mainstream multi-agent frameworks (AutoGen, CrewAI, LangGraph) suffer from a "management vacuum" — collaboration workflows are hard-coded with static topologies, lacking contingency response capabilities.

This paper systematically proposes and defines a new interdisciplinary field — Agent Organizational Management (AOM). The core thesis is: the century of management wisdom about organizational structure, leadership, and incentive mechanisms can be precisely "compiled" into native collaboration protocols for multi-agent systems.

**V5.2 Core Findings (Mechanism Decomposition):**

The central finding is that efficiency gains in multi-agent workflows decompose into:
- **Primary driver (~75%)**: Pipeline-based decomposition (CDE) structurally avoids the Context Accumulation Effect
- **Secondary mechanism (~25%)**: Context Controller provides bounded context optimization

This decomposition is validated across two heterogeneous models (DeepSeek, MiMo) and two heterogeneous tasks (Snake game, Perler bead pattern), suggesting the gains are architecture-induced and model-agnostic.

**Core assertion**: Efficiency gains come primarily from restructuring computation rather than reducing context.

---

## Core Contributions

**V5.2 Contributions (Mechanism Decomposition + Cross-Model Validation):**
- (1) Identification of CAE: Formal proof that iterative LLM self-improvement incurs Omega(n^2) cost, validated across two models
- (2) Mechanism decomposition: Empirical demonstration that efficiency gains decompose into CDE (~75%) and Context Controller (~25%)
- (3) OIMAC as executable protocol: Complete algorithm reducing Omega(n^2) to O(k) with formal complexity analysis
- (4) Cross-model validation of organizational principles: Stress-testing management theories with domain-specific repairs

**V5.2 Experiment Data (DeepSeek / MiMo):**
- Condition A: 6,587 / 8,251 tokens
- Condition B: 88,494 / 102,105 tokens
- Condition C: 43,321 / 49,285 tokens
- Condition D: 58,718 / 63,050 tokens
- C/B ratio: 2.04x / 2.07x (OIMAC ~2x advantage)
- D/C ratio: 1.36x / 1.28x (CC ~1.3x additional savings)

**V1-V4 Contributions:**
- First proposal of AOM complete concept and research agenda
- Mapping of Fayol's 14 principles, Weber's bureaucracy, Mintzberg's configuration theory to Agent topology design
- Engineering of situational leadership theory into dynamic leadership style switching algorithm
- V3 large-scale experiment (N=90): Discovery of autonomy-verbosity trade-off
- V4 three-group experiment: Organizational team 42,166 tokens vs iterative 124,280 tokens (3:1 advantage)

---

## Repository Structure

```
├── README.md
├── README_EN.md
├── LICENSE
│
├── paper/
│   ├── main/
│   │   ├── AOM_paper_v5.2.docx              # V5.2 mechanism decomposition paper
│   │   ├── AOM_paper_v5.docx                # V5.1 backup
│   │   └── AOM_paper_v5.1_backup.docx       # V5.1 backup
│   ├── sections/
│   │   └── section7_experiments.docx         # Section 7 standalone
│   ├── figures/
│   │   ├── v3_experiment/
│   │   └── simulations/
│   ├── supplement/
│   └── archive/
│       ├── v1/
│       ├── v2/
│       ├── v3/
│       └── v4/
│
├── algorithm/
│   └── OIMAC_Framework.docx
│
├── system/
│   ├── architecture_spec.docx
│   └── module_spec.docx
│
├── experiments/
│   ├── deepseek/                             # V5.2 DeepSeek experiment results
│   │   ├── condition_A/
│   │   ├── condition_B/
│   │   ├── condition_C/
│   │   ├── condition_D/
│   │   └── summary.json
│   ├── mimo/                                 # V5.2 MiMo experiment results
│   │   ├── condition_A/
│   │   ├── condition_B/
│   │   ├── condition_C/
│   │   ├── condition_D/
│   │   └── summary.json
│   ├── REPORT.md                             # V5.2 experiment report
│   ├── v4_results/
│   ├── v3_results/
│   └── logs/
│
├── aom-lite/
│   ├── main.py
│   ├── config.json
│   └── requirements.txt
│
└── assets/
```

---

## Quick Start

### Run V5.2 Experiments

```bash
cd experiment

# Run all 4 conditions with DeepSeek
python run_all.py deepseek

# Run all 4 conditions with MiMo
python run_all.py mimo

# View results
cat deepseek/summary.json
cat mimo/summary.json
```

### Run Control-Emergence Balance Simulation

```bash
cd simulations
pip install matplotlib numpy scipy
python control_emergence_plot.py
```

### Run AOM-Lite MVP

```bash
cd aom-lite
pip install -r requirements.txt
python main.py
```

---

## How to Cite

### Chinese Citation

> 江皓然. (2026). 智能体组织管理学：当多智能体系统遇上管理理论 (Version 5.2). 奠基性预印本. GitHub.

### English Citation

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

## Call for Collaboration

This is an open field. Whether you are a management professor, AI researcher, engineer, or a student passionate about this intersection, I sincerely invite you to:

- Read and comment on the paper
- Submit Issues to report errors or suggest improvements
- Fork the repository and develop your own research directions
- Contact me via Discussions or email

Let us bring Agent Organizational Management from vision to reality together.

---

## License

Academic content (paper text) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code (if any) is licensed under [MIT License](https://opensource.org/licenses/MIT).

---

## Contact

- Author: Haoran Jiang
- University: South China University of Technology
- Program: Software Engineering + Business Administration Dual Degree
- Email: JiangLin1297@163.com / JiangLin1297@gmail.com
- GitHub: @JiangLin1297

---

*"The next century of management belongs to algorithms."*
