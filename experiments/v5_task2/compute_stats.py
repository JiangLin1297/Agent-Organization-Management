"""Compute statistics for Task 2 from saved data."""
import json, statistics
from pathlib import Path
from scipy import stats as sp_stats

base = Path(__file__).parent

def compute_for_provider(provider):
    data_file = base / provider / "all_runs.json"
    if not data_file.exists():
        return None
    data = json.loads(data_file.read_text(encoding="utf-8"))
    stats_out = {}
    for cond in ["A", "B", "C", "D"]:
        tokens = [r["tokens"] for r in data[cond]]
        stats_out[cond] = {
            "mean": round(statistics.mean(tokens), 1),
            "std": round(statistics.stdev(tokens), 1) if len(tokens) > 1 else 0,
            "min": min(tokens), "max": max(tokens), "n": len(tokens), "values": tokens,
        }
    def t_test(a_vals, b_vals, label):
        t_stat, p_val = sp_stats.ttest_ind(a_vals, b_vals)
        cohens_d = (statistics.mean(a_vals) - statistics.mean(b_vals)) / (
            ((statistics.stdev(a_vals)**2 + statistics.stdev(b_vals)**2) / 2) ** 0.5)
        return {"label": label, "t_stat": round(t_stat, 4), "p_value": round(p_val, 6),
                "cohens_d": round(cohens_d, 4), "significant_005": bool(p_val < 0.05)}
    tests = [
        t_test(stats_out["C"]["values"], stats_out["B"]["values"], "C_vs_B"),
        t_test(stats_out["C"]["values"], stats_out["D"]["values"], "C_vs_D"),
    ]
    return {"stats": stats_out, "t_tests": tests}

for provider in ["deepseek", "mimo"]:
    print(f"\n{'='*60}")
    print(f"Task2 Data Analysis | {provider}")
    print(f"{'='*60}")
    result = compute_for_provider(provider)
    if not result:
        print("  No data available")
        continue
    for cond in ["A", "B", "C", "D"]:
        s = result["stats"][cond]
        print(f"  {cond}: mean={s['mean']:>10,.1f}  std={s['std']:>8,.1f}  n={s['n']}")
    print()
    for t in result["t_tests"]:
        sig = "***" if t["p_value"] < 0.001 else "**" if t["p_value"] < 0.01 else "*" if t["p_value"] < 0.05 else "n.s."
        print(f"  {t['label']}: t={t['t_stat']:>7.3f}  p={t['p_value']:.6f} {sig}  d={t['cohens_d']:.3f}")
    b_mean = result["stats"]["B"]["mean"]
    c_mean = result["stats"]["C"]["mean"]
    d_mean = result["stats"]["D"]["mean"]
    print(f"  C/B ratio: {b_mean/c_mean:.2f}x")
    print(f"  D/C ratio: {d_mean/c_mean:.2f}x")

# Save CSV
all_results = {}
for p in ["deepseek", "mimo"]:
    r = compute_for_provider(p)
    if r:
        all_results[p] = r

csv_lines = ["provider,condition,mean_tokens,std_tokens,min_tokens,max_tokens,n"]
for p_name, p_data in all_results.items():
    for cond in ["A", "B", "C", "D"]:
        s = p_data["stats"][cond]
        csv_lines.append(f"{p_name},{cond},{s['mean']},{s['std']},{s['min']},{s['max']},{s['n']}")
csv_lines.append("")
csv_lines.append("provider,comparison,t_stat,p_value,cohens_d,significant_005")
for p_name, p_data in all_results.items():
    for t in p_data["t_tests"]:
        csv_lines.append(f"{p_name},{t['label']},{t['t_stat']},{t['p_value']},{t['cohens_d']},{t['significant_005']}")

(base / "results_summary.csv").write_text("\n".join(csv_lines), encoding="utf-8")
print(f"\nCSV saved to {base / 'results_summary.csv'}")
