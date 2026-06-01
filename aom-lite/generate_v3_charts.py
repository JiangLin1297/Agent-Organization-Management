"""
V3 实验结果可视化

生成图表：
1. 不同不确定性水平下，ST vs AOM-DT 的平均Token柱状图
2. 不同不确定性水平下，ST vs AOM-DT 的平均时间柱状图
3. 每个Agent的Token消耗分布散点图

保存到 assets/ 目录
"""

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

COLORS = {
    'ST': '#4A90D9',
    'AOM-DT': '#E8584F'
}


def load_results(filepath):
    """加载实验结果"""
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['uncertainty_value'] = float(row['uncertainty_value'])
            row['total_tokens'] = int(row['total_tokens'])
            row['total_time'] = float(row['total_time'])
            row['quality_score'] = int(row['quality_score'])
            row['coordination_overhead_pct'] = float(row['coordination_overhead_pct'])
            row['coordinator_tokens'] = int(row['coordinator_tokens'])
            row['synthesis_tokens'] = int(row['synthesis_tokens'])
            for wk in ['A', 'B', 'C']:
                row[f'worker_{wk}_tokens'] = int(row[f'worker_{wk}_tokens'])
                row[f'worker_{wk}_time'] = float(row[f'worker_{wk}_time'])
            results.append(row)
    return results


def plot_token_comparison(results, output_dir):
    """柱状图：不同不确定性水平下 ST vs AOM-DT 的平均Token"""
    levels = ['low', 'medium', 'high']
    level_labels = ['Low Uncertainty', 'Medium Uncertainty', 'High Uncertainty']

    st_tokens = []
    dt_tokens = []
    st_stds = []
    dt_stds = []

    for level in levels:
        st = [r['total_tokens'] for r in results if r['uncertainty_level'] == level and r['condition'] == 'ST']
        dt = [r['total_tokens'] for r in results if r['uncertainty_level'] == level and r['condition'] == 'AOM-DT']
        st_tokens.append(np.mean(st))
        dt_tokens.append(np.mean(dt))
        st_stds.append(np.std(st))
        dt_stds.append(np.std(dt))

    x = np.arange(len(levels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, st_tokens, width, label='ST (Fixed S1)',
                   color=COLORS['ST'], yerr=st_stds, capsize=5, alpha=0.85)
    bars2 = ax.bar(x + width/2, dt_tokens, width, label='AOM-DT (Dynamic)',
                   color=COLORS['AOM-DT'], yerr=dt_stds, capsize=5, alpha=0.85)

    ax.set_xlabel('Task Uncertainty Level', fontsize=13)
    ax.set_ylabel('Average Token Consumption', fontsize=13)
    ax.set_title('Token Consumption: ST vs AOM-DT by Uncertainty Level', fontsize=15, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(level_labels, fontsize=11)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3)

    # 添加数值标签
    for bar in bars1:
        h = bar.get_height()
        ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
    for bar in bars2:
        h = bar.get_height()
        ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)

    plt.tight_layout()
    path = os.path.join(output_dir, 'v3_token_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


def plot_time_comparison(results, output_dir):
    """柱状图：不同不确定性水平下 ST vs AOM-DT 的平均时间"""
    levels = ['low', 'medium', 'high']
    level_labels = ['Low Uncertainty', 'Medium Uncertainty', 'High Uncertainty']

    st_times = []
    dt_times = []
    st_stds = []
    dt_stds = []

    for level in levels:
        st = [r['total_time'] for r in results if r['uncertainty_level'] == level and r['condition'] == 'ST']
        dt = [r['total_time'] for r in results if r['uncertainty_level'] == level and r['condition'] == 'AOM-DT']
        st_times.append(np.mean(st))
        dt_times.append(np.mean(dt))
        st_stds.append(np.std(st))
        dt_stds.append(np.std(dt))

    x = np.arange(len(levels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, st_times, width, label='ST (Fixed S1)',
                   color=COLORS['ST'], yerr=st_stds, capsize=5, alpha=0.85)
    bars2 = ax.bar(x + width/2, dt_times, width, label='AOM-DT (Dynamic)',
                   color=COLORS['AOM-DT'], yerr=dt_stds, capsize=5, alpha=0.85)

    ax.set_xlabel('Task Uncertainty Level', fontsize=13)
    ax.set_ylabel('Average Completion Time (seconds)', fontsize=13)
    ax.set_title('Task Completion Time: ST vs AOM-DT by Uncertainty Level', fontsize=15, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(level_labels, fontsize=11)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3)

    for bar in bars1:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}s', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
    for bar in bars2:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}s', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)

    plt.tight_layout()
    path = os.path.join(output_dir, 'v3_time_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


def plot_agent_token_distribution(results, output_dir):
    """散点图：每个Agent的Token消耗分布"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    agents = [('A', 'Novice (R=0.24)'), ('B', 'Growth (R=0.54)'), ('C', 'Senior (R=0.87)')]

    # ST condition
    ax = axes[0]
    for agent_key, agent_label in agents:
        tokens = [r[f'worker_{agent_key}_tokens'] for r in results if r['condition'] == 'ST']
        jitter = np.random.normal(0, 0.1, len(tokens))
        x_pos = [{'A': 0, 'B': 1, 'C': 2}[agent_key] + jitter[i] for i in range(len(tokens))]
        ax.scatter(x_pos, tokens, alpha=0.5, s=30, label=agent_label)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Novice\n(R=0.24)', 'Growth\n(R=0.54)', 'Senior\n(R=0.87)'])
    ax.set_ylabel('Token Consumption', fontsize=12)
    ax.set_title('ST (Fixed S1): Worker Token Distribution', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    # AOM-DT condition
    ax = axes[1]
    for agent_key, agent_label in agents:
        tokens = [r[f'worker_{agent_key}_tokens'] for r in results if r['condition'] == 'AOM-DT']
        jitter = np.random.normal(0, 0.1, len(tokens))
        x_pos = [{'A': 0, 'B': 1, 'C': 2}[agent_key] + jitter[i] for i in range(len(tokens))]
        ax.scatter(x_pos, tokens, alpha=0.5, s=30, label=agent_label)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Novice\n(S1)', 'Growth\n(S3)', 'Senior\n(S4)'])
    ax.set_ylabel('Token Consumption', fontsize=12)
    ax.set_title('AOM-DT (Dynamic): Worker Token Distribution', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, 'v3_agent_token_distribution.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


def main():
    results_path = 'experiment_v3_results.csv'
    output_dir = '../assets'

    if not os.path.exists(results_path):
        # Try partial results
        results_path = 'experiment_v3_results_partial.csv'
        if not os.path.exists(results_path):
            print('No results file found. Run experiment_v3.py first.')
            return

    os.makedirs(output_dir, exist_ok=True)

    print(f'Loading results from {results_path}...')
    results = load_results(results_path)
    print(f'Loaded {len(results)} results')

    print('\nGenerating charts...')
    plot_token_comparison(results, output_dir)
    plot_time_comparison(results, output_dir)
    plot_agent_token_distribution(results, output_dir)

    print('\nDone! Charts saved to assets/')


if __name__ == '__main__':
    main()
