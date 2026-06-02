# Agent Organizational Management (AOM): When Multi-Agent Systems Meet Management Theory

> **Not managing humans with AI — managing AI with the wisdom of management science.**
>
> Foundational Preprint | Version 5.0 | 2026-06-02

> 📖 [阅读中文版](README.md)

---

## 🆕 V5.0 Released (2026-06-02)

**V5.0 Key additions: Mechanism-Algorithm-System Integration**

1. **Mechanism Layer**: Five structural efficiency mechanisms formalized (CAE/CDE/IRC/COS/AVT) with assumptions, causal chains, boundary conditions
2. **Cost Model**: TotalCost = ComputationCost + CoordinationCost + CommunicationCost, with optimal team size k* derivation
3. **OIMAC Algorithm**: Complete 7-phase pseudocode with computable decision rules (SPLIT/MERGE/CENTRALIZE/STYLE_DOWNGRADE/CONTEXT_LIMIT)
4. **System Architecture**: Nine-module implementable design; Context Controller architecturally breaks CAE conditions via three rules
5. **CAE Proposition Strengthened**: Explicit boundary conditions (a)(b), tighter proof sketch, new boundary conditions section
6. **Mechanism Isolation Strengthened**: Explicit IV (context passing architecture) and DV (token consumption) definitions
7. **Theory Contribution Strengthened**: Situational Leadership / Weber / Fayol unified into (a)(b)(c)(d) structure
8. **Folder Restructured**: paper/archive/ for V1-V4, paper/figures/ by experiment, experiments/ independent
9. **Main Paper Consolidated**: paper/main/AOM_paper_v5.docx is the single main paper

---

## V4.0 Released (2026-06-02)

**V4.0 Key additions: Three-Group Controlled Experiment — Proving the Empirical Value of Organizational Management**

1. **Three-group controlled experiment**: Condition A (single agent, single call), Condition B (single agent, 7 iterative rounds), Condition C (6-role organizational team) — same task, comparable budgets
2. **Core finding — Dual value of organizational management**: AOM team completes with 42,166 tokens; iterative approach consumes 124,280 tokens (3:1 advantage), while achieving superior code quality
3. **Token inflation root cause analysis**: Iterative approach suffers exponential token growth — each improvement round must embed the full previous code, creating a positive feedback loop; organizational decomposition avoids this through role-based context splitting
4. **Testing role's empirical value**: Tester caught four blocking bugs caused by frontend/game-logic interface inconsistencies — bugs invisible to single-agent workflows
5. **V4 paper (DOCX)**: Section 3 fully rewritten with V4 experiment as core evidence — 6 data tables, code quality multi-dimensional comparison, token inflation formula analysis
6. **V3↔V4 complementarity**: V3 showed style matching has limited efficiency benefit; V4 showed organizational structure has significant quality and efficiency benefits — AOM should prioritize structural principles over stylistic adaptation
7. **V4 experiment code**: `aom-lite/v4_experiment/` contains complete runnable scripts and prompt files for all three conditions
8. **Bilingual papers**: V4 Chinese and English versions updated in sync

---

## V3.0 Released (2026-06-01)

**V3.0 Key additions: Large-Scale Efficiency Experiment with Honest Findings**

1. **Large-scale real experiment (N=90)**: 4 heterogeneous agents × 9 tasks × 2 conditions × 5 repetitions
2. **Key finding — Autonomy-Verbosity Trade-off**: AOM-DT uses more tokens but achieves equal success rate and quality
3. **Theoretical Solutions (§2.5)**: Four prompt design principles from management theory
4. **AOM Ultimate Vision**: Empowering every individual to manage their own AI Agent team

---

## V2.0 Released (2026-05-30)

**Key additions in V2.0:**

1. **Related Work & Field Positioning (§1.3)**: Systematic comparison with Chain-of-Thought, MARL, Scalable Oversight, and ONA, clarifying AOM's unique value proposition
2. **Emergent Theoretical Observations from Mapping (§2.4)**: AOM-original hypotheses including the "Control-Emergence Balance Conjecture," providing mathematically verifiable propositions for management science
3. **Experimental Validation Framework & Simulated Data (§3)**: 1,900 simulated experiments validating dynamic topology advantages across multiple task scenarios
4. **Systematic Limitations Inventory (§4)**: Candid enumeration of 10 field limitations with corresponding mitigation paths
5. **AOM-Lite MVP Immediate Action Plan (§5.2)**: A Situational Leadership style-switching prototype design buildable within 48 hours

---

## Foreword

Many years from now, as I watch hundreds of AI agents collaborate in seamless order, I will recall that distant afternoon in a classroom when I first realized that management theory might have been made for them all along.

I am a sophomore at South China University of Technology, pursuing a dual degree in Software Engineering and Business Administration. From the day I enrolled, people talked. They said management was a useless degree — that only software engineering could lead anywhere, could land you a real job.

But something strange happened. While I was taking classes in C++, data structures, and operating systems, AI agents appeared. They handled my homework. My lab assignments. Even my exam prep. And as more data kept feeding into their knowledge bases, a question began to nag at me: *What won't they be able to do?*

So I started thinking: if agents are now our "employees," then why shouldn't the management theories designed for human employees apply to them too?

That thought hit me and never left. I spent a month working alongside AI, alongside agents, alongside my "digital employees" — translating the theories of Fayol, Weber, Mintzberg, and other management giants into collaboration logic for multi-agent systems. No advisor. No team. No funding. Just a laptop, an idea, and a few AI assistants willing to explore with me.

This paper is the result. It may be rough. But it is my first answer to an era that once laughed at the discipline I chose to study.

Management has been called useless for too long. Now let's see if it can govern AI.

**Haoran Jiang**
South China University of Technology
B.S. Software Engineering & B.B.A. Business Administration, Class of 2028
May 30, 2026

---

## Abstract

When AI agents evolve from isolated tools into "digital employees," the optimal way to manage them is no longer programming — it is management itself. Current mainstream multi-agent frameworks (AutoGen, CrewAI, LangGraph, etc.) suffer from a fundamental flaw: a **management vacuum**. Collaboration flows are hardcoded as static topologies, incapable of adapting to task complexity, environmental uncertainty, or agent capability heterogeneity.

This paper, for the first time, systematically defines and proposes a new interdisciplinary field: **Agent Organizational Management (AOM)**. Its core thesis: a century of accumulated wisdom in management science — on organizational structure, leadership, and motivation — can be precisely "compiled" into native collaboration protocols for multi-agent systems. The paper constructs a systematic mapping framework: Weber's bureaucracy and Mintzberg's organizational configurations are mapped to agent topology and role design; Hersey-Blanchard's Situational Leadership is engineered into a dynamic control logic for agent coordinators; Drucker's Management by Objectives and Vroom's Expectancy Theory are transformed into objective functions and attention allocation mechanisms.

The paper further argues that AOM is not merely "using management to govern AI." It opens a reverse path of empowerment: through large-scale agent simulation, management science gains, for the first time, the ability to conduct controlled, reproducible, large-scale experiments — enabling it to test and advance its own theories. The paper candidly defines the boundaries of the field's applicability and outlines a ten-year vision for AOM as both an academic discipline and a product category.

**The central thesis of this paper: in the age of AI, management is no longer merely the study of human organization — it is the engineering science of designing agent societies.**

---

## Core Contributions

**V5 Core Contributions (Mechanism-Algorithm-System Integration):**
- ✅ Identification and formalization of the **Context Accumulation Effect (CAE)** — Omega(n^2) cost trap in iterative LLM self-improvement
- ✅ **OIMAC algorithm** — reduces iterative cost from Omega(n^2) to O(k), with complete pseudocode and complexity analysis
- ✅ **Nine-module system architecture** — Context Controller architecturally breaks CAE conditions
- ✅ Five structural efficiency mechanisms formalized (CAE/CDE/IRC/COS/AVT) with assumptions, causal chains, boundary conditions
- ✅ **Unified cost model**: TotalCost = ComputationCost + CoordinationCost + CommunicationCost
- ✅ **Stress-testing** of Situational Leadership / Weber / Fayol with boundary conditions and domain-specific repairs

**V1-V4 Contributions:**
- ✅ First complete definition and research agenda for **Agent Organizational Management (AOM)**
- ✅ **Precise mapping** of Fayol's 14 Principles, Weber's bureaucracy, and Mintzberg's configurations to agent topology design
- ✅ **Engineering implementation** of Situational Leadership Theory as a dynamic style-switching algorithm
- ✅ V3 large-scale experiment (N=90): discovery of the Autonomy-Verbosity Trade-off
- ✅ V4 three-group experiment: organizational team 42,166 tokens vs iterative 124,280 tokens (3:1 advantage)

---

## Repository Structure

```
├── README.md                        # Chinese README
├── README_EN.md                     # This file (English README)
├── LICENSE                          # CC BY 4.0
│
├── paper/
│   ├── main/
│   │   └── AOM_paper_v5.docx       # Main paper (V5 mechanism-algorithm-system integration)
│   ├── figures/
│   │   ├── v3_experiment/           # V3 experiment charts
│   │   └── simulations/             # Control-emergence balance simulation plots
│   ├── supplement/                  # Supplementary materials
│   └── archive/                     # Historical versions (V1-V4)
│
├── algorithm/
│   └── OIMAC_Framework.docx         # OIMAC algorithm framework (mechanisms + cost model + pseudocode)
│
├── system/
│   ├── architecture_spec.docx       # System architecture spec (9 modules + CAE breaking)
│   └── module_spec.docx             # Mechanism-to-module mapping table
│
├── experiments/
│   ├── v4_results/                  # V4 three-group experiment data
│   ├── v3_results/                  # V3 large-scale experiment data (N=90)
│   └── logs/                        # Run logs
│
├── aom-lite/                        # AOM-Lite MVP prototype code
│   ├── main.py
│   ├── config.json
│   └── requirements.txt
│
└── assets/                          # Original image resources
```

---

## Quick Start

### Run Control-Emergence Balance Conjecture Simulation

```bash
cd simulations
pip install matplotlib numpy scipy
python control_emergence_plot.py
```

### Run AOM-Lite MVP Prototype

```bash
cd aom-lite
pip install -r requirements.txt
python main.py
```

---

## How to Cite

If this paper informs your work, please cite it as follows:

### APA Style

> Jiang, H. (2026). *Agent Organizational Management: When Multi-Agent Systems Meet Management Theory* (Version 5.0) [Foundational Preprint]. Retrieved from https://github.com/JiangLin1297/Agent-Organization-Management

### BibTeX

```bibtex
@unpublished{jiang2026aom,
  author    = {Haoran Jiang},
  title     = {Agent Organizational Management: When Multi-Agent Systems Meet Management Theory},
  note      = {Foundational Preprint, Version 4.0},
  year      = {2026},
  month     = may,
  url       = {https://github.com/JiangLin1297/Agent-Organization-Management}
}
```

---

## Call for Collaboration

This is an open field. Whether you are a management professor, an AI researcher, an engineer, or a student as captivated by this intersection as I am, I warmly invite you to:

- 📖 Read and comment on the paper
- 🐛 Open an Issue to point out errors or suggest improvements
- 🔀 Fork the repository and develop your own research direction
- ✉️ Reach out via Discussions or email

Let us bring Agent Organizational Management from vision to reality, together.

---

## License

The academic content of this repository (the paper text) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Any code is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Contact

- **Author**: Haoran Jiang
- **Institution**: South China University of Technology
- **Program**: B.S. Software Engineering & B.B.A. Business Administration
- **Email**: JiangLin1297@163.com / JiangLin1297@gmail.com
- **GitHub**: @JiangLin1297

---

*"The next century of management belongs to algorithms."*
