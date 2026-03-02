import numpy as np
import pandas as pd

np.random.seed(42)
N = 6000

varieties = ["Cabernet_Sauvignon", "Merlot", "Pinot_Noir", "Chardonnay", "Syrah", "Sauvignon_Blanc"]
microzones = ["River_Terrace", "North_Hills", "South_Slope", "Valley_Floor", "Limestone_Ridge"]
soil_types = ["Clay_Loam", "Sandy_Loam", "Limestone", "Gravel", "Silt_Loam"]
exposures = ["North", "South", "East", "West", "Southwest"]
irrigation = ["None", "Standard", "Deficit"]
blocks = [f"Block_{z}_{i:02d}" for z in ["East", "West", "North", "South", "Central"] for i in range(1, 13)]
years = np.arange(2018, 2025)

vintage_year = np.random.choice(years, size=N, p=[0.12, 0.13, 0.14, 0.15, 0.16, 0.15, 0.15])
harvest_day_of_year = np.random.randint(240, 301, size=N)
harvest_date = pd.to_datetime(vintage_year.astype(str), format="%Y") + pd.to_timedelta(harvest_day_of_year - 1, unit="D")

variety = np.random.choice(varieties, size=N, p=[0.2, 0.2, 0.14, 0.18, 0.16, 0.12])
microzone = np.random.choice(microzones, size=N)
soil = np.random.choice(soil_types, size=N)
exposure = np.random.choice(exposures, size=N)
irrig = np.random.choice(irrigation, size=N, p=[0.2, 0.45, 0.35])
block = np.random.choice(blocks, size=N)

vine_age_years = np.clip(np.random.normal(16, 6, N), 3, 40).round(0)
soil_ph = np.clip(np.random.normal(6.4, 0.35, N), 5.5, 7.5)
soil_organic = np.clip(np.random.normal(2.7, 0.8, N), 1.0, 5.5)

temp_base_by_zone = {"River_Terrace": 22.1, "North_Hills": 21.0, "South_Slope": 23.0, "Valley_Floor": 22.4, "Limestone_Ridge": 21.6}
rain_base_by_zone = {"River_Terrace": 430, "North_Hills": 460, "South_Slope": 390, "Valley_Floor": 440, "Limestone_Ridge": 410}
year_temp_shift = {2018: -0.3, 2019: 0.0, 2020: 0.4, 2021: -0.2, 2022: 0.5, 2023: 0.7, 2024: 0.2}
year_rain_shift = {2018: 15, 2019: -10, 2020: -25, 2021: 30, 2022: -35, 2023: -20, 2024: 10}

growing_temp = np.array([temp_base_by_zone[microzone[i]] + year_temp_shift[vintage_year[i]] + np.random.normal(0, 0.8) for i in range(N)])
growing_rain = np.array([rain_base_by_zone[microzone[i]] + year_rain_shift[vintage_year[i]] + np.random.normal(0, 55) for i in range(N)])
growing_rain = np.clip(growing_rain, 220, 700)

sunshine_days = np.clip((145 - 0.08 * growing_rain + 2.5 * (growing_temp - 21) + np.random.normal(0, 6, N)), 75, 155).round(0)
heatwave_days = np.clip((1.5 + 1.9 * (growing_temp - 21.5) + np.random.normal(0, 1.8, N)), 0, 22).round(0)

disease_pressure = (25 + 0.06 * (growing_rain - 420) + 0.22 * np.maximum(0, 18 - sunshine_days) + np.where(irrig == "Deficit", -4, 0) + np.random.normal(0, 4, N))
disease_pressure = np.clip(disease_pressure, 5, 85)

fermentation_control = np.clip(68 + 0.35 * vine_age_years + 1.8 * (vintage_year - 2018) + np.where(irrig == "Deficit", 2.5, 0) + np.random.normal(0, 6, N), 40, 98)
oak_aging = np.random.choice([0, 3, 6, 9, 12, 15, 18, 24], size=N, p=[0.06, 0.08, 0.18, 0.2, 0.24, 0.12, 0.08, 0.04])

variety_brix_base = {"Cabernet_Sauvignon": 24.5, "Merlot": 24.0, "Pinot_Noir": 23.4, "Chardonnay": 22.8, "Syrah": 24.2, "Sauvignon_Blanc": 22.5}
harvest_brix = np.array([variety_brix_base[variety[i]] + 0.18 * (growing_temp[i] - 22) + 0.025 * (sunshine_days[i] - 115) - 0.015 * (growing_rain[i] - 420) + np.random.normal(0, 0.55) for i in range(N)])
harvest_brix = np.clip(harvest_brix, 19.0, 28.0)
harvest_acidity = np.clip(8.8 - 0.11 * harvest_brix - 0.03 * (growing_temp - 22) + np.random.normal(0, 0.35, N), 4.2, 8.8)

# 1) Магистральный эффект сорта
variety_effect_map = {"Cabernet_Sauvignon": 4.5, "Merlot": 2.0, "Pinot_Noir": 1.0, "Chardonnay": -0.5, "Syrah": 3.0, "Sauvignon_Blanc": -1.2}
variety_effect = np.array([variety_effect_map[v] for v in variety])
# 2) Нелинейный температурный оптимум
temp_effect = -0.95 * (growing_temp - 22.0) ** 2 + 5.3
# 3) Осадки: оптимум в центре
rain_effect = -0.00011 * (growing_rain - 420) ** 2 + 3.8
# 4) Солнечные дни: насыщение для ароматики
sun_effect_aroma = 6.0 / (1 + np.exp(-(sunshine_days - 108) / 8.0)) - 2.8
# 5) Органика почвы: убывающая отдача для баланса
organic_effect_balance = 4.0 * np.tanh((soil_organic - 2.2) / 1.3)
# 6) Жара сильнее бьет по Pinot Noir
heat_effect = -0.38 * heatwave_days + np.where(variety == "Pinot_Noir", -0.35 * heatwave_days, 0.0)
# 7) Болезни и компенсация контролем брожения
disease_main = -0.14 * disease_pressure
mitigation = 0.055 * disease_pressure * (fermentation_control - 65) / 35
# 8) Оптимальный коридор brix+acidity
brix_penalty = -0.9 * np.abs(harvest_brix - 24.0)
acidity_penalty = -1.15 * np.abs(harvest_acidity - 6.0)
# 9) Выдержка в дубе: максимум до порога
oak_effect = -0.045 * (oak_aging - 12) ** 2 + 2.5
# 10) Терруарный бонус микрозона*экспозиция
terroir_bonus = np.zeros(N)
terroir_bonus += np.where((microzone == "Limestone_Ridge") & (exposure == "Southwest"), 2.2, 0)
terroir_bonus += np.where((microzone == "River_Terrace") & (exposure == "South"), 1.7, 0)
terroir_bonus += np.where((microzone == "North_Hills") & (exposure == "North"), 1.2, 0)
terroir_bonus += np.where((microzone == "Valley_Floor") & (exposure == "West"), -1.0, 0)

ph_effect = -1.3 * np.abs(soil_ph - 6.45)
irrig_effect = np.where(irrig == "Deficit", 1.0, np.where(irrig == "None", -0.4, 0.3))
vine_age_effect = 0.08 * np.minimum(vine_age_years, 25) - 0.03 * np.maximum(vine_age_years - 25, 0)

latent_quality = 73.0 + variety_effect + temp_effect + rain_effect + heat_effect + disease_main + mitigation + oak_effect + terroir_bonus + ph_effect + irrig_effect + vine_age_effect

sensory_aroma = np.clip(latent_quality + sun_effect_aroma + 0.3 * oak_effect + np.random.normal(0, 2.1, N), 55, 98)
sensory_balance = np.clip(latent_quality + organic_effect_balance + brix_penalty + acidity_penalty + np.random.normal(0, 2.2, N), 50, 98)
wine_quality = np.clip(latent_quality + 0.35 * sun_effect_aroma + 0.45 * organic_effect_balance + np.random.normal(0, 2.4, N), 50, 99)

batch_id = [f"BATCH_{vintage_year[i]}_{i+1:05d}" for i in range(N)]

df = pd.DataFrame({
    "batch_id": batch_id,
    "harvest_date": harvest_date,
    "vintage_year": vintage_year,
    "vineyard_block": block,
    "region_microzone": microzone,
    "grape_variety": variety,
    "vine_age_years": vine_age_years.astype(int),
    "soil_type": soil,
    "soil_ph": np.round(soil_ph, 2),
    "soil_organic_matter_pct": np.round(soil_organic, 2),
    "slope_exposure": exposure,
    "irrigation_regime": irrig,
    "growing_season_temp_avg": np.round(growing_temp, 2),
    "growing_season_rain_mm": np.round(growing_rain, 1),
    "sunshine_days": sunshine_days.astype(int),
    "heatwave_days": heatwave_days.astype(int),
    "disease_pressure_index": np.round(disease_pressure, 1),
    "harvest_brix": np.round(harvest_brix, 2),
    "harvest_acidity_g_l": np.round(harvest_acidity, 2),
    "fermentation_control_score": np.round(fermentation_control, 1),
    "oak_aging_months": oak_aging.astype(int),
    "sensory_aroma_score": np.round(sensory_aroma, 2),
    "sensory_balance_score": np.round(sensory_balance, 2),
    "wine_quality_index": np.round(wine_quality, 2),
})

minor_segment = df[(df["grape_variety"] == "Pinot_Noir") & (df["heatwave_days"] >= 12)]
if len(minor_segment) < 50:
    idx = df.sample(50 - len(minor_segment), random_state=42).index
    df.loc[idx, "grape_variety"] = "Pinot_Noir"
    df.loc[idx, "heatwave_days"] = np.maximum(df.loc[idx, "heatwave_days"].values, 12)

df.to_csv("dataset.csv", index=False, encoding="utf-8")
print("dataset.csv сохранён:", df.shape)
