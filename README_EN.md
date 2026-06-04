# Agent Organizational Management (AOM)

**When Multi-Agent Systems Meet Management Theory**

*Not using AI to manage people — using management theory to manage AI.*

Preprint | Foundational Preprint | Version 5.4 | 2026-06-04

> 📖 [阅读中文版](README.md)

---

## V5.4 Released (2026-06-04)

**V5.4: Problem-Driven Theory Edition — Real-World Baseline — Theoretical Propositions**

Core upgrade: Paper reframed from "system + experiment" narrative to "problem-driven theoretical paper" with real-world baseline and formal propositions.

### Key Changes

1. **Problem-driven narrative**: Abstract and Introduction restructured around CAE problem → insight → method → results
2. **Theoretical propositions**: 3 formal propositions (CAE quadratic growth, CDE linearization, real-world baseline gap)
3. **Real-world baseline (Condition E)**: Experiments simulating AutoGen/CrewAI-style systems
4. **Unified numbers**: All documents use "≈2.0x reduction" and "≈25-30% additional savings"
5. **Strengthened conclusion**: "Organizational structure is a first-class computational primitive"

### Experiment Results (V5.4 Complete Comparison)

| Condition | DeepSeek Mean±Std | MiMo Mean±Std | Description |
|-----------|-------------------|---------------|-------------|
| A (Single Agent) | 6,000±254 | 8,251±0 | Single-pass baseline |
| B (Iterative 7r) | 90,437±9,653 | 102,417±1,547 | CAE manifest |
| C (OIMAC+CC) | 45,581±3,082 | 48,468±1,445 | Structured + bounded context |
| D (OIMAC-CC) | 60,894±2,319 | 61,805±1,691 | Structured, no context limits |
| **E (Real-world)** | **64,634±3,644** | **~67,200*** | AutoGen/CrewAI-style |

*MiMo Condition E estimated from cross-model ratios

### Core Efficiency Comparison

- **C/B ≈ 2.0x**: OIMAC vs iterative refinement (p<0.001, d>5.6)
- **C/E ≈ 1.4x**: OIMAC vs real-world multi-agent baseline
- **D/C ≈ 1.3x**: Context Controller additional (~25-30%)
- **CDE contribution**: ~70% (primary driver)
- **CC contribution**: ~30% (secondary mechanism)

### Core Assertion

**Efficiency gains come from restructuring computation, not reducing context. Organizational structure is a first-class computational primitive.**

> 📊 Full report: [REPORT_V5.3.md](REPORT_V5.3.md)

---

## V5.3 Released (2026-06-04)

**V5.3: Statistical Validation — Quality Assessment — Multi-task Generalization**

Core upgrade: Experiments upgraded from "single-run case study" to "statistically validated, submission-ready experiments."

### Key Changes

1. **Statistical Replication**: 5 runs per condition (DeepSeek + MiMo), 40 total experiments
2. **t-test Validation**: All key comparisons p < 0.001, Cohen's d > 4.6 (very large effect)
3. **Quality Assessment**: 5-dimension automated quality checks, all outputs score 20-24/25
4. **Multi-task Generalization**: New data analysis task (24 runs), efficiency ratios consistent across tasks
5. **Total Experiments**: 64 independent runs (40 Task1 + 24 Task2)

---

## V5.2 Released (2026-06-03)

**V5.2: Mechanism Decomposition — Cross-Model Validation — ICIS/AAAI Ready**

Core upgrade: Paper reframed from "methods paper" to "mechanism paper" with cross-model experimental validation.

### Key Changes

1. **Mechanism Decomposition**: Efficiency gains decomposed into primary driver (CDE, ~70%) and secondary mechanism (Context Controller, ~30%)
2. **Cross-Model Validation**: Experiments replicated across DeepSeek and MiMo, two heterogeneous models
3. **Two Tasks**: Perler bead pattern generator (code-heavy) + data analysis report (analysis-heavy)
4. **Core Finding**: Efficiency gains come primarily from restructuring computation rather than reducing context

---

## V5.0 Released (2026-06-02)

**V5.0 Core: Mechanism-Algorithm-System Integration**

1. **Mechanism Layer**: Formalization of five structural efficiency mechanisms (CAE/CDE/IRC/COS/AVT)
2. **Cost Model**: TotalCost = ComputationCost + CoordinationCost + CommunicationCost, with optimal team size k*
3. **OIMAC Algorithm**: Complete 7-phase pseudocode with decision rules
4. **System Architecture**: Nine-module implementable design with CAE avoidance mechanism

---

## V4.0 Released (2026-06-02)

1. **Three-Group Controlled Experiment**: Control A (single agent), Control B (iterative 7 rounds), Experimental (6-role organization)
2. **Core Finding**: Organizational team 42,166 tokens vs iterative 124,280 tokens (3:1 advantage)

---

## V3.0 Released (2026-06-01)

1. **Large-Scale Experiment (N=60)**: 15 tasks x 2 conditions x 2 repetitions
2. **Autonomy-Verbosity Trade-off**: AOM-DT consumes more tokens with equal success rate

---

## Abstract

**Problem.** Multi-agent systems built on LLMs suffer from the Context Accumulation Effect (CAE): iterative self-improvement causes token consumption to grow as O(n²) — a structural cost pathology, not an implementation inefficiency.

**Insight.** The root cause is not "too much context" but incorrect computational structure. Restructuring computation is more powerful than reducing context.

**Method.** OIMAC decomposes monolithic iteration into a multi-role pipeline with bounded context passing via a Context Controller.

**Results:**
- ~2.0x token reduction vs iterative (p<0.001, d>5.6)
- ~1.4x token reduction vs real-world baselines (AutoGen/CrewAI-style)
- Cross-model (DeepSeek + MiMo), cross-task (HTML + data analysis)
- Quality preserved (20-24/25)
- Mechanism decomposition: CDE≈70%, CC≈30%

**Core assertion.** Efficiency gains come from restructuring computation, not reducing context. Organizational structure is a first-class computational primitive.

---

## Core Contributions

**V5.4 (Problem-Driven Theory Edition):**
- (1) CAE formalization: Proof that iterative LLM self-improvement incurs Ω(n²) token cost growth
- (2) Mechanism decomposition: CDE (~70%) + Context Controller (~30%), empirically validated
- (3) OIMAC as structural solution: Reduces Ω(n²) to O(k), p<0.001, d>5.6
- (4) Real-world baseline: Outperforms AutoGen/CrewAI-style architectures, ~1.4x further reduction

---

## Repository Structure

```
├── README.md                           # Chinese README
├── README_EN.md                        # This file (English)
├── LICENSE
├── paper/
│   ├── main/
│   │   ├── AOM_paper_v5.3.docx        # V5.4 main paper (Chinese)
│   │   ├── AOM_paper_v5.3_en.docx     # V5.4 pure English
│   │   └── generate_v5.3.py           # Paper generation script
│   ├── sections/
│   │   ├── v5.4_abstract.md           # V5.4 Abstract
│   │   ├── v5.4_introduction.md       # V5.4 Introduction
│   │   ├── v5.4_propositions.md       # V5.4 Theoretical Propositions
│   │   └── v5.4_conclusion.md         # V5.4 Conclusion
│   ├── supplementary.zip
│   ├── figures/
│   └── archive/                        # V1-V4 archives
├── algorithm/
│   └── OIMAC_Framework.docx
├── system/
│   ├── architecture_spec.docx
│   └── module_spec.docx
├── aom-lite_MVP/                       # AOM-Lite MVP
└── experiments/
    ├── OIMAC_experiment_Pixel/         # V5.2 cross-model experiments
    ├── v5_repeated/                    # V5.3/V5.4 statistical validation
    │   ├── run_condition_E.py          # Condition E (real-world baseline)
    │   ├── condition_E_summary.json    # Condition E results
    │   └── ...
    ├── v5_task2/                       # V5.3 generalization task
    ├── v3_results/
    └── v4_results/
```

---

## Quick Start

### Run V5.4 Condition E Experiment (Real-World Baseline)

```bash
cd experiments/v5_repeated
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# Run Condition E
python run_condition_E.py deepseek
python run_condition_E.py mimo
```

### Run V5.3 Statistical Replication

```bash
cd experiments/v5_repeated
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# Run 5 replications per condition per model
python run_repeated.py all
```

### Run AOM-Lite MVP

```bash
cd aom-lite_MVP
pip install -r requirements.txt
python main.py
```

---

## How to Cite

> Jiang, H. (2026). Agent Organizational Management: When Multi-Agent Systems Meet Management Theory (Version 5.4). Foundational Preprint. GitHub.

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

## License

Academic content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT License](https://opensource.org/licenses/MIT).

---

## Contact

- Author: Haoran Jiang
- University: South China University of Technology
- Program: Software Engineering + Business Administration Dual Degree
- Email: JiangLin1297@163.com / JiangLin1297@gmail.com
- GitHub: @JiangLin1297

---

*"The next century of management belongs to algorithms."*
