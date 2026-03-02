import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
df = pd.read_csv("dataset.csv", parse_dates=["harvest_date"])
print("Размер:", df.shape)

# 1) Сорт как магистральный фактор качества
m1 = df.groupby("grape_variety")["wine_quality_index"].mean().sort_values(ascending=False)
print("[1] Разница лидер-аутсайдер:", round(m1.iloc[0] - m1.iloc[-1], 2))
plt.figure(figsize=(8, 4)); sns.barplot(x=m1.index, y=m1.values); plt.xticks(rotation=25); plt.tight_layout(); plt.savefig("check_01.png"); plt.close()

# 2) Температурный оптимум (нелинейность)
plt.figure(figsize=(7, 4)); sns.regplot(data=df, x="growing_season_temp_avg", y="wine_quality_index", lowess=True, scatter_kws={"alpha":0.2,"s":10}); plt.tight_layout(); plt.savefig("check_02.png"); plt.close()

# 3) Осадки: оптимум
rb = df.assign(rain_bin=pd.cut(df["growing_season_rain_mm"], bins=10)).groupby("rain_bin", observed=False)["wine_quality_index"].mean()
print("[3] Размах по бинам осадков:", round(rb.max()-rb.min(), 2))
plt.figure(figsize=(9, 4)); rb.plot(marker="o"); plt.xticks(rotation=30); plt.tight_layout(); plt.savefig("check_03.png"); plt.close()

# 4) Солнечные дни и ароматика
plt.figure(figsize=(7, 4)); sns.regplot(data=df, x="sunshine_days", y="sensory_aroma_score", lowess=True, scatter_kws={"alpha":0.2,"s":10}); plt.tight_layout(); plt.savefig("check_04.png"); plt.close()

# 5) Органика и баланс
plt.figure(figsize=(7, 4)); sns.regplot(data=df, x="soil_organic_matter_pct", y="sensory_balance_score", lowess=True, scatter_kws={"alpha":0.2,"s":10}); plt.tight_layout(); plt.savefig("check_05.png"); plt.close()

# 6) Жара и сорта
heat_group = df.groupby(["grape_variety", "heatwave_days"])["wine_quality_index"].mean().reset_index()
plt.figure(figsize=(9, 5))
for v in ["Pinot_Noir", "Cabernet_Sauvignon", "Merlot", "Syrah"]:
    sub = heat_group[heat_group["grape_variety"] == v]
    plt.plot(sub["heatwave_days"], sub["wine_quality_index"], marker="o", label=v)
plt.legend(); plt.tight_layout(); plt.savefig("check_06.png"); plt.close()

# 7) Болезни и контроль брожения
fg = df.copy()
fg["control_group"] = pd.qcut(fg["fermentation_control_score"], q=3, labels=["Low", "Mid", "High"])
sample = fg.sample(2500, random_state=42)
g = sns.lmplot(data=sample, x="disease_pressure_index", y="wine_quality_index", hue="control_group", lowess=True, height=5, aspect=1.4, scatter_kws={"alpha":0.2,"s":12})
g.fig.tight_layout(); g.savefig("check_07.png")

# 8) brix/acidity и баланс
fg["brix_bin"] = pd.cut(fg["harvest_brix"], bins=8)
fg["acid_bin"] = pd.cut(fg["harvest_acidity_g_l"], bins=8)
heat8 = fg.pivot_table(index="acid_bin", columns="brix_bin", values="sensory_balance_score", aggfunc="mean")
plt.figure(figsize=(9, 6)); sns.heatmap(heat8, cmap="YlGnBu"); plt.tight_layout(); plt.savefig("check_08.png"); plt.close()

# 9) Выдержка дуба
m9 = fg.groupby("oak_aging_months")["wine_quality_index"].mean().sort_index()
print("[9] Лучший oak_aging_months:", int(m9.idxmax()))
plt.figure(figsize=(7, 4)); plt.plot(m9.index, m9.values, marker="o"); plt.tight_layout(); plt.savefig("check_09.png"); plt.close()

# 10) Терруарный бонус
heat10 = fg.pivot_table(index="region_microzone", columns="slope_exposure", values="wine_quality_index", aggfunc="mean")
print("[10] Лучшая пара:", heat10.stack().idxmax())
plt.figure(figsize=(8, 5)); sns.heatmap(heat10, annot=True, fmt=".1f", cmap="RdYlGn"); plt.tight_layout(); plt.savefig("check_10.png"); plt.close()

print("Графики сохранены check_01.png ... check_10.png")
