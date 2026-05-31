"""
控制-涌现平衡猜想数值模拟
Control-Emergence Balance Conjecture Numerical Simulation

==========================================================================
此模拟仅基于假设的效能函数，用于可视化猜想的理论形态，不代表真实数据。
This simulation is based on a hypothetical efficacy function only.
It visualizes the theoretical shape of the conjecture and does NOT represent real data.
==========================================================================

论文参考：智能体组织管理学 V2.0, §2.4.4

猜想内容：
- 最优管理强度 MI*(C, H) 使得系统效能 SE 最大化
- MI* 始终位于 (0, 1) 区间内，既非完全控制，也非完全涌现
- MI* 随任务复杂度 C 增大而减小（复杂任务需要更多涌现空间）
- MI* 随 Agent 异质性 H 增大而增大（异质团队需要更强协调）

数学形式：
    MI*(C, H) = argmax_{MI ∈ [0,1]} SE(MI, C, H)
    其中 SE 为系统效能函数

作者：江皓然
日期：2026-05-30
"""

import numpy as np
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import minimize_scalar

# ============================================================================
# 1. 定义模拟效能函数
# ============================================================================

def system_efficacy(MI, C, H):
    """
    计算系统效能 SE(MI, C, H)

    参数:
        MI (float): 管理强度，取值范围 [0, 1]
                    MI=0 表示完全涌现（无管理）
                    MI=1 表示完全控制（严格管理）
        C (float): 任务复杂度，取值范围 [0, 1]
                   C=0 表示简单任务
                   C=1 表示高度复杂任务
        H (float): Agent 异质性，取值范围 [0, 1]
                   H=0 表示同质化 Agent
                   H=1 表示高度异质 Agent

    返回:
        float: 系统效能值，非负

    函数设计原理：
    1. 基准最优管理强度 = 0.8 - 0.6*C + 0.4*H
       - C 增大 → 最优MI降低（复杂任务需要更多涌现空间）
       - H 增大 → 最优MI升高（异质团队需要更强协调）
    2. SE 呈倒U型曲线：偏离最优MI时效能下降
    3. 额外惩罚项：当 C 偏离 0.5 时，MI 的敏感性增加
       （极端复杂或极端简单的任务对管理强度更敏感）
    """
    # 计算基准最优管理强度
    # 这个线性组合确保 MI* 在 (0, 1) 区间内
    MI_optimal = 0.8 - 0.6 * C + 0.4 * H

    # 截断到 [0, 1] 区间
    MI_optimal = np.clip(MI_optimal, 0.05, 0.95)

    # 主效能项：倒U型曲线，峰值在 MI_optimal 处
    # 使用绝对值距离，形成 V 形下降
    main_term = 1 - 2 * abs(MI - MI_optimal)

    # 复杂度调节项：当 C 偏离 0.5 时，对 MI 的敏感性增加
    # 这反映了极端任务场景下管理强度选择的重要性
    sensitivity = 0.3 * MI * (1 - MI) * (C - 0.5) ** 2

    # 最终效能 = 主项 - 敏感性惩罚
    SE = main_term - sensitivity

    # 确保非负
    SE = max(SE, 0.0)

    return SE


# ============================================================================
# 2. 网格搜索最优管理强度
# ============================================================================

def find_optimal_MI(C, H, grid_size=1000):
    """
    对于给定的 (C, H)，找到使 SE 最大的 MI*

    参数:
        C (float): 任务复杂度
        H (float): Agent 异质性
        grid_size (int): 网格搜索的分辨率

    返回:
        tuple: (MI_star, SE_max) 最优管理强度和对应的最大效能
    """
    # 使用 scipy 的有界优化（比网格搜索更精确）
    result = minimize_scalar(
        lambda mi: -system_efficacy(mi, C, H),  # 取负号因为 minimize
        bounds=(0, 1),
        method='bounded'
    )

    MI_star = result.x
    SE_max = -result.fun  # 还原为正值

    return MI_star, SE_max


# ============================================================================
# 3. 生成网格数据
# ============================================================================

print("=" * 60)
print("控制-涌现平衡猜想数值模拟")
print("Control-Emergence Balance Conjecture Simulation")
print("=" * 60)
print("\n此模拟仅基于假设的效能函数，用于可视化猜想的理论形态")
print("不代表真实数据，仅供参考\n")

# 定义网格分辨率
resolution = 50

# 创建 C 和 H 的网格
C_range = np.linspace(0, 1, resolution)
H_range = np.linspace(0, 1, resolution)
C_grid, H_grid = np.meshgrid(C_range, H_range)

# 计算每个网格点的最优 MI*
MI_star_grid = np.zeros_like(C_grid)
SE_max_grid = np.zeros_like(C_grid)

print(f"正在计算 {resolution}x{resolution} = {resolution**2} 个网格点...")
for i in range(resolution):
    for j in range(resolution):
        c = C_grid[i, j]
        h = H_grid[i, j]
        mi_star, se_max = find_optimal_MI(c, h)
        MI_star_grid[i, j] = mi_star
        SE_max_grid[i, j] = se_max

print("计算完成！\n")

# 验证猜想性质
print("-" * 40)
print("猜想验证：")
print("-" * 40)

# 1. MI* 是否始终在 (0, 1) 区间内
print(f"MI* 范围: [{MI_star_grid.min():.4f}, {MI_star_grid.max():.4f}]")
assert MI_star_grid.min() > 0 and MI_star_grid.max() < 1, "猜想1不成立：MI* 超出 (0,1) 区间"
print("[OK] 猜想1成立：MI* ∈ (0, 1)")

# 2. MI* 是否随 C 增大而减小
# 固定 H=0.5，检查 MI* 随 C 的变化
H_fixed_idx = resolution // 2
MI_vs_C = MI_star_grid[H_fixed_idx, :]
correlation_C = np.corrcoef(C_range, MI_vs_C)[0, 1]
print(f"MI* 与 C 的相关系数: {correlation_C:.4f} (应为负)")
assert correlation_C < 0, "猜想2不成立：MI* 未随 C 增大而减小"
print("[OK] 猜想2成立：MI* 随 C 增大而减小")

# 3. MI* 是否随 H 增大而增大
# 固定 C=0.5，检查 MI* 随 H 的变化
C_fixed_idx = resolution // 2
MI_vs_H = MI_star_grid[:, C_fixed_idx]
correlation_H = np.corrcoef(H_range, MI_vs_H)[0, 1]
print(f"MI* 与 H 的相关系数: {correlation_H:.4f} (应为正)")
assert correlation_H > 0, "猜想3不成立：MI* 未随 H 增大而增大"
print("[OK] 猜想3成立：MI* 随 H 增大而增大")

print("\n" + "=" * 60)
print("所有猜想验证通过！")
print("=" * 60)


# ============================================================================
# 4. 绘制三维曲面图
# ============================================================================

print("\n正在生成三维曲面图...")

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面
surf = ax.plot_surface(
    C_grid, H_grid, MI_star_grid,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=True,
    alpha=0.9
)

# 添加颜色条
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20, label='MI* (最优管理强度)')

# 设置坐标轴标签
ax.set_xlabel('任务复杂度 C\n(Task Complexity)', fontsize=11, labelpad=10)
ax.set_ylabel('Agent 异质性 H\n(Agent Heterogeneity)', fontsize=11, labelpad=10)
ax.set_zlabel('最优管理强度 MI*\n(Optimal Management Intensity)', fontsize=11, labelpad=10)

# 设置标题
ax.set_title(
    '控制-涌现平衡猜想：最优管理强度曲面\n'
    'Control-Emergence Balance Conjecture: Optimal MI Surface\n'
    '(基于假设效能函数的数值模拟)',
    fontsize=13, pad=20
)

# 设置视角
ax.view_init(elev=30, azim=45)

# 保存图片
plt.tight_layout()
plt.savefig(
    'control_emergence_surface.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white',
    edgecolor='none'
)
print("[OK] 已保存: control_emergence_surface.png")


# ============================================================================
# 5. 绘制二维等高线图
# ============================================================================

print("\n正在生成二维等高线图...")

fig2, ax2 = plt.subplots(figsize=(10, 8))

# 绘制填充等高线
contour_filled = ax2.contourf(
    C_grid, H_grid, MI_star_grid,
    levels=20,
    cmap=cm.coolwarm,
    alpha=0.8
)

# 添加颜色条
cbar2 = fig2.colorbar(contour_filled, ax=ax2, label='MI* (最优管理强度)')

# 绘制等高线
contour_lines = ax2.contour(
    C_grid, H_grid, MI_star_grid,
    levels=10,
    colors='black',
    linewidths=0.5,
    alpha=0.5
)

# 标注等高线数值
ax2.clabel(contour_lines, inline=True, fontsize=8, fmt='%.2f')

# 特别标注 MI* = 0.5 的曲线（平衡复杂度 C* 的位置）
# 这是猜想中的关键等高线
contour_05 = ax2.contour(
    C_grid, H_grid, MI_star_grid,
    levels=[0.5],
    colors='white',
    linewidths=3,
    linestyles='--'
)
ax2.clabel(contour_05, inline=True, fontsize=10, fmt='MI*=0.5')

# 在图上添加注释
ax2.annotate(
    'MI* = 0.5\n(平衡线)',
    xy=(0.5, 0.5),
    xytext=(0.7, 0.3),
    fontsize=10,
    color='white',
    fontweight='bold',
    arrowprops=dict(arrowstyle='->', color='white', lw=2),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7)
)

# 设置坐标轴标签
ax2.set_xlabel('任务复杂度 C (Task Complexity)', fontsize=12)
ax2.set_ylabel('Agent 异质性 H (Agent Heterogeneity)', fontsize=12)

# 设置标题
ax2.set_title(
    '控制-涌现平衡猜想：最优管理强度等高线\n'
    'Control-Emergence Balance Conjecture: Optimal MI Contour\n'
    '(白色虚线表示 MI* = 0.5 的平衡位置)',
    fontsize=13, pad=15
)

# 添加网格
ax2.grid(True, alpha=0.3, linestyle='--')

# 保存图片
plt.tight_layout()
plt.savefig(
    'control_emergence_contour.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white',
    edgecolor='none'
)
print("[OK] 已保存: control_emergence_contour.png")


# ============================================================================
# 6. 输出关键数据点
# ============================================================================

print("\n" + "=" * 60)
print("关键数据点 (MI* 值):")
print("=" * 60)
print(f"{'C':>6} {'H':>6} {'MI*':>8} {'SE':>8}")
print("-" * 30)

# 选择几个代表性点
test_points = [
    (0.1, 0.1, "简单任务+同质Agent"),
    (0.1, 0.9, "简单任务+异质Agent"),
    (0.5, 0.5, "中等任务+中等异质"),
    (0.9, 0.1, "复杂任务+同质Agent"),
    (0.9, 0.9, "复杂任务+异质Agent"),
]

for c, h, desc in test_points:
    mi_star, se_max = find_optimal_MI(c, h)
    print(f"{c:6.2f} {h:6.2f} {mi_star:8.4f} {se_max:8.4f}  # {desc}")

print("\n" + "=" * 60)
print("模拟完成！")
print("=" * 60)
print("\n注意：以上数据基于假设的效能函数，仅用于可视化猜想的理论形态。")
print("真实数据需要通过实验验证或更精确的理论模型获得。")
