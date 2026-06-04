"""Compute statistics and t-tests from saved experiment data."""
import json, statistics
from pathlib import Path
from scipy import stats as sp_stats

base = Path(__file__).parent

def compute_for_provider(provider):
    data_file = base / provider / "all_runs.json"
    if not data_file.exists():
        print(f"  No data for {provider}")
        return None

    data = json.loads(data_file.read_text(encoding="utf-8"))

    stats_out = {}
    for cond in ["A", "B", "C", "D"]:
        tokens = [r["tokens"] for r in data[cond]]
        stats_out[cond] = {
            "mean": round(statistics.mean(tokens), 1),
            "std": round(statistics.stdev(tokens), 1) if len(tokens) > 1 else 0,
            "min": min(tokens),
            "max": max(tokens),
            "n": len(tokens),
            "values": tokens,
        }

    def t_test(a_vals, b_vals, label):
        t_stat, p_val = sp_stats.ttest_ind(a_vals, b_vals)
        cohens_d = (statistics.mean(a_vals) - statistics.mean(b_vals)) / (
            ((statistics.stdev(a_vals)**2 + statistics.stdev(b_vals)**2) / 2) ** 0.5
        )
        return {
            "label": label,
            "t_stat": round(t_stat, 4),
            "p_value": round(p_val, 6),
            "cohens_d": round(cohens_d, 4),
            "significant_005": bool(p_val < 0.05),
            "significant_001": bool(p_val < 0.01),
        }

    tests = [
        t_test(stats_out["C"]["values"], stats_out["B"]["values"], "C_vs_B"),
        t_test(stats_out["C"]["values"], stats_out["D"]["values"], "C_vs_D"),
        t_test(stats_out["B"]["values"], stats_out["D"]["values"], "B_vs_D"),
    ]

    return {"stats": stats_out, "t_tests": tests}

# Process DeepSeek
print("=" * 60)
print("DeepSeek Repeated Experiment Results")
print("=" * 60)
ds = compute_for_provider("deepseek")
if ds:
    for cond in ["A", "B", "C", "D"]:
        s = ds["stats"][cond]
        print(f"  {cond}: mean={s['mean']:>10,.1f}  std={s['std']:>8,.1f}  min={s['min']:>8,}  max={s['max']:>8,}  n={s['n']}")
    print()
    for t in ds["t_tests"]:
        sig = "***" if t["p_value"] < 0.001 else "**" if t["p_value"] < 0.01 else "*" if t["p_value"] < 0.05 else "n.s."
        print(f"  {t['label']}: t={t['t_stat']:>7.3f}  p={t['p_value']:.6f} {sig}  d={t['cohens_d']:.3f}")

    # Mechanism decomposition
    b_mean = ds["stats"]["B"]["mean"]
    c_mean = ds["stats"]["C"]["mean"]
    d_mean = ds["stats"]["D"]["mean"]
    cde_pct = (b_mean - d_mean) / (b_mean - c_mean) * 100 if (b_mean - c_mean) != 0 else 0
    cc_pct = (d_mean - c_mean) / (b_mean - c_mean) * 100 if (b_mean - c_mean) != 0 else 0
    cb_ratio = b_mean / c_mean if c_mean else 0
    dc_ratio = d_mean / c_mean if c_mean else 0
    print(f"\n  C/B ratio: {cb_ratio:.2f}x")
    print(f"  D/C ratio: {dc_ratio:.2f}x")
    print(f"  CDE contribution: {cde_pct:.1f}%")
    print(f"  CC contribution: {cc_pct:.1f}%")

# Check MiMo
print()
mimo_file = base / "mimo" / "all_runs.json"
if mimo_file.exists():
    print("=" * 60)
    print("MiMo Repeated Experiment Results")
    print("=" * 60)
    mm = compute_for_provider("mimo")
    if mm:
        for cond in ["A", "B", "C", "D"]:
            s = mm["stats"][cond]
            print(f"  {cond}: mean={s['mean']:>10,.1f}  std={s['std']:>8,.1f}  min={s['min']:>8,}  max={s['max']:>8,}  n={s['n']}")
        print()
        for t in mm["t_tests"]:
            sig = "***" if t["p_value"] < 0.001 else "**" if t["p_value"] < 0.01 else "*" if t["p_value"] < 0.05 else "n.s."
            print(f"  {t['label']}: t={t['t_stat']:>7.3f}  p={t['p_value']:.6f} {sig}  d={t['cohens_d']:.3f}")

        b_mean = mm["stats"]["B"]["mean"]
        c_mean = mm["stats"]["C"]["mean"]
        d_mean = mm["stats"]["D"]["mean"]
        cde_pct = (b_mean - d_mean) / (b_mean - c_mean) * 100 if (b_mean - c_mean) != 0 else 0
        cc_pct = (d_mean - c_mean) / (b_mean - c_mean) * 100 if (b_mean - c_mean) != 0 else 0
        cb_ratio = b_mean / c_mean if c_mean else 0
        dc_ratio = d_mean / c_mean if c_mean else 0
        print(f"\n  C/B ratio: {cb_ratio:.2f}x")
        print(f"  D/C ratio: {dc_ratio:.2f}x")
        print(f"  CDE contribution: {cde_pct:.1f}%")
        print(f"  CC contribution: {cc_pct:.1f}%")
else:
    print("MiMo data not yet available")

# Save combined results
results = {"deepseek": ds}
if mimo_file.exists():
    mm_data = compute_for_provider("mimo")
    if mm_data:
        results["mimo"] = mm_data

# Generate CSV
csv_lines = ["provider,condition,mean_tokens,std_tokens,min_tokens,max_tokens,n"]
for p_name, p_data in results.items():
    if p_data:
        for cond in ["A", "B", "C", "D"]:
            s = p_data["stats"][cond]
            csv_lines.append(f"{p_name},{cond},{s['mean']},{s['std']},{s['min']},{s['max']},{s['n']}")

csv_lines.append("")
csv_lines.append("# T-Test Results")
csv_lines.append("provider,comparison,t_stat,p_value,cohens_d,significant_005")
for p_name, p_data in results.items():
    if p_data:
        for t in p_data["t_tests"]:
            csv_lines.append(f"{p_name},{t['label']},{t['t_stat']},{t['p_value']},{t['cohens_d']},{t['significant_005']}")

csv_path = base / "results_summary.csv"
csv_path.write_text("\n".join(csv_lines), encoding="utf-8")
print(f"\nCSV saved to {csv_path}")

# Save JSON
json_path = base / "stats_summary.json"
json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"JSON saved to {json_path}")
