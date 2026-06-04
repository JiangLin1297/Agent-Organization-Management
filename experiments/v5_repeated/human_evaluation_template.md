# Human Evaluation Template — Perler Bead Pattern Generator

**Evaluator:** ____________________
**Date:** ____________________

## Instructions

For each output HTML file, open it in a browser, upload a test image (e.g., a simple 100x100 pixel photo), and rate the output on three dimensions using a 1–5 scale.

### Rating Scale

| Score | Description |
|-------|-------------|
| 5 | Excellent — fully functional, no issues |
| 4 | Good — works well with minor issues |
| 3 | Acceptable — works but with noticeable problems |
| 2 | Poor — significant functionality issues |
| 1 | Fails — core functionality broken or absent |

### Dimensions

1. **Correctness**: Does the color mapping accurately reflect the original image? Are the grid cells assigned correct colors?
2. **Usability**: Is the interface intuitive? Can a user upload an image and get a pattern without confusion?
3. **Visual Quality**: Is the rendered grid visually clear? Are colors distinguishable? Is the layout clean?

---

## DeepSeek — Condition A (Single Agent)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `deepseek/condition_A/run_1/output.html` | | | | |
| 2 | `deepseek/condition_A/run_2/output.html` | | | | |
| 3 | `deepseek/condition_A/run_3/output.html` | | | | |
| 4 | `deepseek/condition_A/run_4/output.html` | | | | |
| 5 | `deepseek/condition_A/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## DeepSeek — Condition B (Iterative 7 Rounds)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `deepseek/condition_B/run_1/output.html` | | | | |
| 2 | `deepseek/condition_B/run_2/output.html` | | | | |
| 3 | `deepseek/condition_B/run_3/output.html` | | | | |
| 4 | `deepseek/condition_B/run_4/output.html` | | | | |
| 5 | `deepseek/condition_B/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## DeepSeek — Condition C (OIMAC + CC)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `deepseek/condition_C/run_1/output.html` | | | | |
| 2 | `deepseek/condition_C/run_2/output.html` | | | | |
| 3 | `deepseek/condition_C/run_3/output.html` | | | | |
| 4 | `deepseek/condition_C/run_4/output.html` | | | | |
| 5 | `deepseek/condition_C/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## DeepSeek — Condition D (OIMAC - CC)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `deepseek/condition_D/run_1/output.html` | | | | |
| 2 | `deepseek/condition_D/run_2/output.html` | | | | |
| 3 | `deepseek/condition_D/run_3/output.html` | | | | |
| 4 | `deepseek/condition_D/run_4/output.html` | | | | |
| 5 | `deepseek/condition_D/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## DeepSeek — Condition E (Real-World Baseline)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `deepseek/condition_E/run_1/output.html` | | | | |
| 2 | `deepseek/condition_E/run_2/output.html` | | | | |
| 3 | `deepseek/condition_E/run_3/output.html` | | | | |
| 4 | `deepseek/condition_E/run_4/output.html` | | | | |
| 5 | `deepseek/condition_E/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## MiMo — Condition A (Single Agent)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `mimo/condition_A/run_1/output.html` | | | | |
| 2 | `mimo/condition_A/run_2/output.html` | | | | |
| 3 | `mimo/condition_A/run_3/output.html` | | | | |
| 4 | `mimo/condition_A/run_4/output.html` | | | | |
| 5 | `mimo/condition_A/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## MiMo — Condition B (Iterative 7 Rounds)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `mimo/condition_B/run_1/output.html` | | | | |
| 2 | `mimo/condition_B/run_2/output.html` | | | | |
| 3 | `mimo/condition_B/run_3/output.html` | | | | |
| 4 | `mimo/condition_B/run_4/output.html` | | | | |
| 5 | `mimo/condition_B/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## MiMo — Condition C (OIMAC + CC)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `mimo/condition_C/run_1/output.html` | | | | |
| 2 | `mimo/condition_C/run_2/output.html` | | | | |
| 3 | `mimo/condition_C/run_3/output.html` | | | | |
| 4 | `mimo/condition_C/run_4/output.html` | | | | |
| 5 | `mimo/condition_C/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## MiMo — Condition D (OIMAC - CC)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `mimo/condition_D/run_1/output.html` | | | | |
| 2 | `mimo/condition_D/run_2/output.html` | | | | |
| 3 | `mimo/condition_D/run_3/output.html` | | | | |
| 4 | `mimo/condition_D/run_4/output.html` | | | | |
| 5 | `mimo/condition_D/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## MiMo — Condition E (Real-World Baseline)

| Run | File Path | Correctness (1-5) | Usability (1-5) | Visual Quality (1-5) | Notes |
|-----|-----------|-------------------|-----------------|---------------------|-------|
| 1 | `mimo/condition_E/run_1/output.html` | | | | |
| 2 | `mimo/condition_E/run_2/output.html` | | | | |
| 3 | `mimo/condition_E/run_3/output.html` | | | | |
| 4 | `mimo/condition_E/run_4/output.html` | | | | |
| 5 | `mimo/condition_E/run_5/output.html` | | | | |
| **Mean** | | | | | |

---

## Summary Table (Fill After Completing All Ratings)

### DeepSeek

| Condition | Correctness | Usability | Visual Quality | Overall Mean |
|-----------|-------------|-----------|----------------|--------------|
| A (Single Agent) | | | | |
| B (Iterative) | | | | |
| C (OIMAC+CC) | | | | |
| D (OIMAC-CC) | | | | |
| E (Real-world) | | | | |

### MiMo

| Condition | Correctness | Usability | Visual Quality | Overall Mean |
|-----------|-------------|-----------|----------------|--------------|
| A (Single Agent) | | | | |
| B (Iterative) | | | | |
| C (OIMAC+CC) | | | | |
| D (OIMAC-CC) | | | | |
| E (Real-world) | | | | |

---

## Notes for Analysis

After completing the evaluation, the following comparisons are of interest:
- **C vs B**: Does OIMAC quality match iterative refinement despite ~50% cost reduction?
- **C vs E**: Does structured pipeline quality match shared-context architecture?
- **Cross-model**: Are quality patterns consistent across DeepSeek and MiMo?
