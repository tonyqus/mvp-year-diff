import pandas as pd
import numpy as np

# 读取两期数据（请确保文件名与列名一致）
df_2025 = pd.read_excel('mvp_country_counts_2024.xlsx')  # 包含列: Name, Count
df_2026 = pd.read_excel('mvp_country_counts_2025.xlsx')

# 合并并补齐缺失国家（以 0 填充）
df_merged = pd.merge(
    df_2025.rename(columns={'Count': 'Count_2024'}),
    df_2026.rename(columns={'Count': 'Count_2025'}),
    on='Name',
    how='outer'
).fillna(0)

# 计算绝对变化量
df_merged['Diff'] = (
    df_merged['Count_2025'].astype(int) - df_merged['Count_2024'].astype(int)
)

# 计算变化比例并保留 1 位小数
# 若 2025 年为 0 且 2026 年大于 0，标记为 'New'；若两者皆为 0 则为 0.0%
rate = (df_merged['Diff'] / df_merged['Count_2024']) * 100
df_merged['Change_Rate'] = np.where(
    df_merged['Count_2024'] == 0,
    np.where(df_merged['Count_2025'] > 0, 'New', '0.0%'),
    rate.round(1).astype(str) + '%',
)
# 分离增减榜单
increased = df_merged[df_merged['Diff'] > 0].sort_values(by='Diff', ascending=False)
decreased = df_merged[df_merged['Diff'] < 0].sort_values(by='Diff')

print("=== MVP 数量增加的国家 ===")
print(increased[['Name', 'Count_2024', 'Count_2025', 'Diff', 'Change_Rate']].head(15))

print("\n=== MVP 数量减少的国家 ===")
print(decreased[['Name', 'Count_2024', 'Count_2025', 'Diff', 'Change_Rate']].head(15))

# 导出到 Excel
df_merged.to_excel('mvp_comparison_2024_vs_2025.xlsx', index=False)