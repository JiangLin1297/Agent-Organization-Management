# Agent Organizational Management (AOM): When Multi-Agent Systems Meet Management Theory

> **Not managing humans with AI — managing AI with the wisdom of management science.**
>
> Foundational Preprint | Version 3.0 | 2026-06-01

> 📖 [阅读中文版](README.md)

---

## 🆕 V3.0 Released (2026-06-01)

**V3.0 Key additions: Large-Scale Efficiency Experiment with Honest Findings**

1. **Large-scale real experiment (N=90)**: 4 heterogeneous agents × 9 tasks × 2 conditions × 5 repetitions = 90 experiments, 360 LLM calls
2. **Deep efficiency analysis**: Systematic measurement of token consumption, completion time, and coordination overhead
3. **Key finding — Autonomy-Verbosity Trade-off**: AOM-DT uses more tokens (+5–11%) but achieves equal success rate and quality
4. **Academic honesty**: Counter-intuitive results analyzed transparently with improvement directions
5. **Complete visualizations**: Token comparison, time comparison, agent token distribution charts
6. **V3 paper (DOCX)**: Includes efficiency analysis, autonomy-verbosity trade-off discussion, and improvement pathways

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

- ✅ First complete definition and research agenda for **Agent Organizational Management (AOM)**
- ✅ **Precise mapping** of Fayol's 14 Principles, Weber's bureaucracy, and Mintzberg's configurations to agent topology design
- ✅ **Engineering implementation** of Situational Leadership Theory as a dynamic style-switching algorithm, with computable "readiness" metrics
- ✅ **Compilation** of Management by Objectives (MBO) and Expectancy Theory into objective functions and resource allocation mechanisms
- ✅ **Bidirectional empowerment** pathway: using agent simulation as a "particle collider" for management science
- ✅ Candid discussion of **boundary conditions**, identifying the fundamental tension between control and emergence
- ✅ **Product vision**: the Management-Architecture-Based Agent Workbench (MAW)
- ✅ **[v2.0 New]** Related work positioning: systematic comparison with COT, MARL, Scalable Oversight, and ONA
- ✅ **[v2.0 New]** Theoretical innovation: AOM-original hypotheses including the "Control-Emergence Balance Conjecture"
- ✅ **[v2.0 New]** Minimum viable experiment design: 1,900 simulated experiments validating dynamic topology advantages
- ✅ **[v2.0 New]** Systematic limitations analysis: 10 identified limitations with mitigation paths
- ✅ **[v2.0 New]** Minimum product prototype: AOM-Lite Weekend Hackathon MVP design

---

## Repository Structure

```
├── README.md                        # Chinese README
├── README_EN.md                     # This file (English README)
├── paper/
│   ├── agent_organizational_management_v3.docx    # Full paper (Preprint v3.0) 🆕
│   ├── agent_organizational_management_v2.docx    # Full paper (Preprint v2.0)
│   ├── agent_organizational_management_v2_en.docx # Full paper English version (Preprint v2.0)
│   ├── agent_organizational_management_v1.docx    # Full paper (Preprint v1.0)
│   ├── generate_v3_paper.py                       # V3 paper generation script 🆕
│   └── v1_supplement_five_dimensions.md           # v2.0 supplement materials
├── simulations/
│   ├── control_emergence_plot.py    # Control-Emergence Balance Conjecture simulation
│   ├── control_emergence_surface.png  # 3D surface plot
│   └── control_emergence_contour.png  # 2D contour plot
├── aom-lite/
│   ├── main.py                      # AOM-Lite MVP main program
│   ├── experiment_v3.py             # V3 large-scale experiment script 🆕
│   ├── generate_v3_charts.py        # V3 visualization script 🆕
│   ├── experiment_v3_results.csv    # V3 experiment results (90 trials) 🆕
│   ├── config.json                  # Configuration file
│   ├── requirements.txt             # Dependencies
│   └── RUN_RESULT.md                # AOM-Lite run result log
├── LICENSE                          # CC BY 4.0
└── assets/
    ├── v3_token_comparison.png      # Token comparison bar chart 🆕
    ├── v3_time_comparison.png       # Time comparison bar chart 🆕
    └── v3_agent_token_distribution.png  # Agent token distribution scatter 🆕
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

> Jiang, H. (2026). *Agent Organizational Management: When Multi-Agent Systems Meet Management Theory* (Version 3.0) [Foundational Preprint]. Retrieved from https://github.com/JiangLin1297/Agent-Organization-Management

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
