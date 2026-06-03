# Agent Organizational Management (AOM)

**When Multi-Agent Systems Meet Management Theory**

*Not using AI to manage people — using management theory to manage AI.*

Preprint | Foundational Preprint | Version 5.2 | 2026-06-03

> 📖 [阅读中文版](README.md)

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

1. **Mechanism Layer**: Formalization of five structural efficiency mechanisms (CAE/CDE/IRC/COS/AVT)
2. **Cost Model**: TotalCost = ComputationCost + CoordinationCost + CommunicationCost, with optimal team size k*
3. **OIMAC Algorithm**: Complete 7-phase pseudocode with decision rules
4. **System Architecture**: Nine-module implementable design with CAE avoidance mechanism
5. **Theory Contribution**: Stress-testing of situational leadership, Weber's bureaucracy, Fayol's principles

---

## V4.0 Released (2026-06-02)

1. **Three-Group Controlled Experiment**: Control A (single agent), Control B (iterative 7 rounds), Experimental (6-role organization)
2. **Core Finding**: Organizational team 42,166 tokens vs iterative 124,280 tokens (3:1 advantage)
3. **Interface Bug Discovery**: Testing role found 4 blocking bugs from frontend-game logic interface mismatch
4. **Complete Experiment Code**: `aom-lite/v4_experiment/`

---

## V3.0 Released (2026-06-01)

1. **Large-Scale Experiment (N=90)**: 4 heterogeneous Agents x 9 tasks x 2 conditions x 5 repetitions
2. **Autonomy-Verbosity Trade-off**: AOM-DT consumes more tokens with equal success rate
3. **AOM Vision**: Enable everyone to manage AI Agent teams like managing a company

---

## Abstract

This paper presents Agent Organizational Management (AOM) — a field that computationally instantiates and stress-tests management theory as multi-agent coordination protocols.

**V5.2 Core Findings (Mechanism Decomposition):**

Efficiency gains decompose into:
- **Primary driver (~75%)**: Pipeline-based decomposition (CDE) structurally avoids CAE
- **Secondary mechanism (~25%)**: Context Controller provides bounded context optimization

**Core assertion**: Efficiency gains come primarily from restructuring computation rather than reducing context.

---

## Core Contributions

**V5.2 (Mechanism Decomposition + Cross-Model Validation):**
- (1) Identification of CAE: Formal proof of Omega(n^2) cost trap, validated across two models
- (2) Mechanism decomposition: CDE (~75%) + Context Controller (~25%)
- (3) OIMAC as executable protocol: Complete algorithm reducing Omega(n^2) to O(k)
- (4) Cross-model validation: Stress-testing management theories with domain-specific repairs

**V1-V4:**
- First proposal of AOM complete concept and research agenda
- Mapping Fayol's 14 principles, Weber's bureaucracy, Mintzberg's configuration theory to Agent topology
- V3 large-scale experiment (N=90): Autonomy-verbosity trade-off
- V4 three-group experiment: 3:1 advantage of organizational structure

---

## Repository Structure

```
├── README.md                           # Chinese README
├── README_EN.md                        # This file (English)
├── LICENSE
├── paper/
│   ├── main/
│   │   ├── AOM_paper_v5.2.docx        # V5.2 main paper (Chinese+English)
│   │   ├── AOM_paper_v5.2_en.docx     # V5.2 pure English
│   │   ├── AOM_paper_v5.2_HICSS.docx  # V5.2 HICSS formatted
│   │   └── AOM_paper_v5.docx          # V5.0/V5.1 archive
│   ├── sections/
│   │   └── section7_experiments.docx
│   ├── supplementary.zip
│   ├── figures/
│   └── archive/                        # V1-V4 archives
├── experiment/                         # V5.2 cross-model experiments
│   ├── config.py                       # Config (set env vars for API keys)
│   ├── run_all.py                      # Unified runner
│   ├── REPORT.md
│   ├── deepseek/
│   └── mimo/
├── algorithm/
│   └── OIMAC_Framework.docx
├── system/
│   ├── architecture_spec.docx
│   └── module_spec.docx
├── aom-lite/                           # AOM-Lite MVP
└── experiments/                        # V3-V4 historical data
```

---

## Quick Start

### Run V5.2 Experiments

```bash
cd experiment

# Set environment variables
export DEEPSEEK_API_KEY=your_deepseek_key
export MIMO_API_KEY=your_mimo_key

# Run all 4 conditions with DeepSeek
python run_all.py deepseek

# Run all 4 conditions with MiMo
python run_all.py mimo
```

### Run AOM-Lite MVP

```bash
cd aom-lite
pip install -r requirements.txt
python main.py
```

---

## How to Cite

> Jiang, H. (2026). Agent Organizational Management: When Multi-Agent Systems Meet Management Theory (Version 5.2). Foundational Preprint. GitHub.

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
