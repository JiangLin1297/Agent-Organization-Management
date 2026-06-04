"""
V5.3 Quality Evaluation Module
Automated quality checks for 拼豆图生成器 HTML outputs.
Usage: python quality_eval.py [deepseek|mimo|all]
"""
import json, os, sys, re
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "all"

def check_grid_validity(html_content):
    """Check if HTML contains a valid grid rendering mechanism."""
    checks = {
        "has_canvas": bool(re.search(r'<canvas', html_content, re.IGNORECASE)),
        "has_table": bool(re.search(r'<table', html_content, re.IGNORECASE)),
        "has_grid_css": bool(re.search(r'display:\s*grid|grid-template', html_content, re.IGNORECASE)),
        "has_drawImage": bool(re.search(r'drawImage|fillRect|putImageData', html_content, re.IGNORECASE)),
        "has_pixel_rendering": bool(re.search(r'getImageData|putImageData|fillRect', html_content, re.IGNORECASE)),
    }
    checks["passed"] = any([checks["has_canvas"], checks["has_table"], checks["has_grid_css"]])
    checks["score"] = sum([checks["has_canvas"], checks["has_drawImage"], checks["has_pixel_rendering"]])
    return checks

def check_palette_validity(html_content):
    """Check if color palette is properly implemented."""
    checks = {
        "has_color_mapping": bool(re.search(r'color.*map|palette|颜色|配色', html_content, re.IGNORECASE)),
        "has_rgb_hex": bool(re.search(r'#[0-9a-fA-F]{3,6}|rgb\(|rgba\(', html_content)),
        "has_kmeans_or_quantize": bool(re.search(r'k-?means|quantiz|median.?cut|降色|量化', html_content, re.IGNORECASE)),
        "has_color_count": bool(re.search(r'颜色.*数|color.*count|统计', html_content, re.IGNORECASE)),
    }
    checks["passed"] = checks["has_color_mapping"] and checks["has_rgb_hex"]
    checks["score"] = sum(checks.values())
    return checks

def check_export_validity(html_content):
    """Check if export/download functionality exists."""
    checks = {
        "has_download_button": bool(re.search(r'download|下载|导出|export', html_content, re.IGNORECASE)),
        "has_blob_url": bool(re.search(r'createObjectURL|Blob\(|toDataURL', html_content)),
        "has_save_function": bool(re.search(r'\.save\(|\.download|saveAs', html_content, re.IGNORECASE)),
        "has_file_input": bool(re.search(r'<input.*file|type="file"', html_content, re.IGNORECASE)),
    }
    checks["passed"] = checks["has_file_input"]  # At minimum, must accept file input
    checks["score"] = sum(checks.values())
    return checks

def check_size_accuracy(html_content):
    """Check if required grid sizes are supported."""
    checks = {
        "has_32x32": bool(re.search(r'32\s*[x×]\s*32|32x32', html_content)),
        "has_48x48": bool(re.search(r'48\s*[x×]\s*48|48x48', html_content)),
        "has_64x64": bool(re.search(r'64\s*[x×]\s*64|64x64', html_content)),
        "has_size_selector": bool(re.search(r'select|选择.*大小|grid.*size|网格.*大小', html_content, re.IGNORECASE)),
        "has_slider_or_input": bool(re.search(r'<input.*range|<select|type="range"', html_content, re.IGNORECASE)),
    }
    size_count = sum([checks["has_32x32"], checks["has_48x48"], checks["has_64x64"]])
    checks["passed"] = size_count >= 2  # At least 2 of 3 sizes
    checks["score"] = size_count + checks["has_size_selector"] + checks["has_slider_or_input"]
    return checks

def check_functional_completeness(html_content):
    """Check overall functional completeness."""
    checks = {
        "has_image_upload": bool(re.search(r'<input.*file|type="file"|drag.*drop|ondrop', html_content, re.IGNORECASE)),
        "has_canvas_api": bool(re.search(r'getContext|canvas|Canvas', html_content)),
        "has_color_stats": bool(re.search(r'统计|count|频率|frequency|histogram', html_content, re.IGNORECASE)),
        "has_zoom": bool(re.search(r'zoom|scale|放大|缩小|magnif', html_content, re.IGNORECASE)),
        "has_responsive": bool(re.search(r'responsive|viewport|mobile|响应|移动端|媒体查询|@media', html_content, re.IGNORECASE)),
        "is_html5": bool(re.search(r'<!DOCTYPE\s+html|<html', html_content, re.IGNORECASE)),
    }
    checks["score"] = sum(checks.values())
    checks["passed"] = checks["score"] >= 4
    return checks

def evaluate_output(html_path):
    """Run all quality checks on an HTML file."""
    try:
        html_content = Path(html_path).read_text(encoding="utf-8")
    except:
        return {"error": "Cannot read file", "total_score": 0, "max_score": 25}

    results = {
        "grid_validity": check_grid_validity(html_content),
        "palette_validity": check_palette_validity(html_content),
        "export_validity": check_export_validity(html_content),
        "size_accuracy": check_size_accuracy(html_content),
        "functional_completeness": check_functional_completeness(html_content),
    }

    total_score = sum(r["score"] for r in results.values())
    max_score = 25  # 5 checks × max ~5 points each
    all_passed = all(r["passed"] for r in results.values())

    results["total_score"] = total_score
    results["max_score"] = max_score
    results["percentage"] = round(total_score / max_score * 100, 1)
    results["all_passed"] = all_passed

    return results

def run_evaluation(provider):
    """Evaluate all outputs for a provider."""
    base = Path(__file__).parent / provider
    if not base.exists():
        print(f"  Directory not found: {base}")
        return {}

    all_results = {}
    for cond in ["A", "B", "C", "D"]:
        cond_dir = base / f"condition_{cond}"
        if not cond_dir.exists():
            continue
        all_results[cond] = {}
        for run_dir in sorted(cond_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            html_path = run_dir / "output.html"
            if html_path.exists():
                result = evaluate_output(html_path)
                all_results[cond][run_dir.name] = result

    return all_results

def main():
    if PROVIDER == "all":
        providers = ["deepseek", "mimo"]
    else:
        providers = [PROVIDER]

    all_eval = {}
    for p in providers:
        print(f"\nEvaluating {p}...")
        all_eval[p] = run_evaluation(p)

    # Save raw results
    out_path = Path(__file__).parent / "quality_evaluation.json"
    out_path.write_text(json.dumps(all_eval, ensure_ascii=False, indent=2), encoding="utf-8")

    # Generate summary
    summary_lines = []
    summary_lines.append("# Quality Evaluation Report")
    summary_lines.append(f"\nGenerated: {__import__('datetime').datetime.now().isoformat()}")
    summary_lines.append("\n## Automated Quality Checks\n")

    for p in providers:
        summary_lines.append(f"### {p.upper()}\n")
        summary_lines.append("| Condition | Run | Grid | Palette | Export | Size | Functional | Total | Pass |")
        summary_lines.append("|-----------|-----|------|---------|--------|------|------------|-------|------|")

        cond_stats = {}
        for cond in ["A", "B", "C", "D"]:
            scores = []
            if cond in all_eval.get(p, {}):
                for run_name, result in all_eval[p][cond].items():
                    if "error" in result:
                        summary_lines.append(f"| {cond} | {run_name} | ERROR | ERROR | ERROR | ERROR | ERROR | 0 | No |")
                        continue
                    g = result["grid_validity"]["score"]
                    pl = result["palette_validity"]["score"]
                    e = result["export_validity"]["score"]
                    s = result["size_accuracy"]["score"]
                    f = result["functional_completeness"]["score"]
                    t = result["total_score"]
                    p_pass = "Yes" if result["all_passed"] else "No"
                    summary_lines.append(f"| {cond} | {run_name} | {g} | {pl} | {e} | {s} | {f} | {t} | {p_pass} |")
                    scores.append(t)
            if scores:
                cond_stats[cond] = {
                    "mean": round(sum(scores) / len(scores), 1),
                    "min": min(scores),
                    "max": max(scores),
                }

        summary_lines.append("")
        summary_lines.append("**Mean scores by condition:**")
        summary_lines.append("")
        summary_lines.append("| Condition | Mean Score | Min | Max |")
        summary_lines.append("|-----------|-----------|-----|-----|")
        for cond in ["A", "B", "C", "D"]:
            if cond in cond_stats:
                s = cond_stats[cond]
                summary_lines.append(f"| {cond} | {s['mean']}/{25} | {s['min']} | {s['max']} |")
        summary_lines.append("")

    summary_lines.append("## Human Evaluation Template\n")
    summary_lines.append("Please evaluate each output on the following dimensions (1-5 scale):\n")
    summary_lines.append("| Dimension | Description | Score (1-5) |")
    summary_lines.append("|-----------|-------------|-------------|")
    summary_lines.append("| Usability | Is the interface intuitive? Can a user complete the task without instructions? | |")
    summary_lines.append("| Visual Quality | Is the output visually appealing? Are colors, spacing, layout professional? | |")
    summary_lines.append("| Accuracy | Are the colors correctly mapped? Is the grid accurate? Do the stats match? | |")
    summary_lines.append("| Completeness | Does it implement all required features (upload, grid, stats, zoom)? | |")
    summary_lines.append("| Robustness | Does it handle edge cases (large images, many colors, mobile)? | |")
    summary_lines.append("")
    summary_lines.append("### Evaluation Sheet\n")
    summary_lines.append("| Provider | Condition | Run | Usability | Visual | Accuracy | Complete | Robust | Notes |")
    summary_lines.append("|----------|-----------|-----|-----------|--------|----------|----------|--------|-------|")

    for p in providers:
        for cond in ["A", "B", "C", "D"]:
            for run_id in range(1, 6):
                summary_lines.append(f"| {p} | {cond} | {run_id} | | | | | | |")
    summary_lines.append("")

    md_path = Path(__file__).parent / "quality_evaluation.md"
    md_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"\nSaved to {md_path}")
    print(f"JSON saved to {out_path}")

if __name__ == "__main__":
    main()
