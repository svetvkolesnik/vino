# Фаза 1. Проектирование и самопроверка схемы

## 1. Тип строки (уровень наблюдения)

**Одна строка датасета соответствует одной партии винограда (batch), собранной с конкретного блока виноградника в определённую дату урожая и прошедшей первичную производственную обработку с последующей дегустационной оценкой вина из этой партии.**

Уровень строки: `batch`.

## 2. Целевая переменная и задачи анализа

### 2.1 Целевые переменные
В кейсе используются три целевые переменные уровня `batch`:

1. `wine_quality_index` — интегральный индекс качества вина по итогам внутренней дегустационной комиссии.
2. `sensory_aroma_score` — оценка ароматического профиля.
3. `sensory_balance_score` — оценка баланса (кислотность, танины, тело, послевкусие).

### 2.2 Явная фиксация уровня
Все три целевые переменные рассчитаны **для конкретной партии** и полностью соответствуют уровню строки `batch`.

## 3. Перечень полей без дубликатов

| Имя поля | Тип данных | Уровень | Описание смысла | Пример значения |
|---|---|---|---|---|
| batch_id | строка | batch | Уникальный идентификатор партии | BATCH_2022_01874 |
| harvest_date | дата/время | batch | Дата сбора винограда для партии | 2022-09-18 |
| vintage_year | число | batch | Год урожая (винтаж) партии | 2022 |
| vineyard_block | категория | batch | Блок виноградника, откуда получена партия | Block_East_07 |
| region_microzone | категория | batch | Микрозона терруара в пределах хозяйства | River_Terrace |
| grape_variety | категория | batch | Сорт винограда | Cabernet_Sauvignon |
| vine_age_years | число | batch | Средний возраст лоз на блоке | 14 |
| soil_type | категория | batch | Преобладающий тип почвы блока | Clay_Loam |
| soil_ph | число | batch | Кислотность почвы (pH) | 6.5 |
| soil_organic_matter_pct | число | batch | Доля органического вещества в почве, % | 2.8 |
| slope_exposure | категория | batch | Экспозиция склона | South |
| irrigation_regime | категория | batch | Режим орошения в сезон | Deficit |
| growing_season_temp_avg | число | batch | Средняя температура вегетационного периода, °C | 22.4 |
| growing_season_rain_mm | число | batch | Суммарные осадки за вегетационный период, мм | 415 |
| sunshine_days | число | batch | Количество солнечных дней в сезон | 118 |
| heatwave_days | число | batch | Количество дней с экстремальной жарой | 9 |
| disease_pressure_index | число | batch | Индекс фитосанитарного давления (болезни/гниль), 0–100 | 27 |
| harvest_brix | число | batch | Сахаристость сусла на сборе (°Brix) | 24.1 |
| harvest_acidity_g_l | число | batch | Титруемая кислотность на сборе (г/л) | 6.1 |
| fermentation_control_score | число | batch | Индекс стабильности и управляемости брожения, 0–100 | 78 |
| oak_aging_months | число | batch | Выдержка в дубе (месяцы) | 12 |
| sensory_aroma_score | число | batch | Дегустационный балл ароматики (0–100) | 86.4 |
| sensory_balance_score | число | batch | Дегустационный балл баланса (0–100) | 83.9 |
| wine_quality_index | число | batch | Интегральный итоговый индекс качества (0–100) | 85.1 |

**Примечание по отсутствию дубликатов:**
- Поля `vintage_year` и `harvest_date` не являются смысловыми дубликатами: дата нужна для детального временного анализа внутри сезона, а год — для стабильного межгодового сравнения винтажей и группировок без вычислений в BI-инструменте.
- Поля целевых переменных не выводятся друг из друга простой формулой и отражают разные аспекты сенсорной оценки.

## 4. Описание скрытых закономерностей и связанных визуализаций (для преподавателя)

### Закономерность 1. «Сорт как магистральный фактор качества»
- **Поля:** `grape_variety`, `wine_quality_index`.
- **Тип эффекта:** различия между группами.
- **Ожидаемый эффект:** среднее качество устойчиво различается по сортам; разница между лидерами и аутсайдерами заметная.
- **Диаграмма:** столбчатая.
  - X: сорт.
  - Y: средний индекс качества.
  - Сравнение: все сорта между собой.

### Закономерность 2. «Нелинейный температурный оптимум»
- **Поля:** `growing_season_temp_avg`, `wine_quality_index`.
- **Тип эффекта:** нелинейная (колоколообразная) зависимость.
- **Ожидаемый эффект:** качество растёт до оптимального диапазона температур и снижается при переохлаждении/перегреве.
- **Диаграмма:** точечная + сглаженный тренд.
  - X: средняя сезонная температура.
  - Y: индекс качества.
  - Сравнение: общий тренд и по сортам.

### Закономерность 3. «Осадки: эффект дефицита и переувлажнения»
- **Поля:** `growing_season_rain_mm`, `wine_quality_index`.
- **Тип эффекта:** нелинейная U-образная инверсия (оптимум в середине).
- **Ожидаемый эффект:** крайние уровни осадков ухудшают качество, умеренные — лучшие.
- **Диаграмма:** точечная/линейная по бинам осадков.
  - X: бины осадков.
  - Y: средний индекс качества.
  - Сравнение: режимы орошения.

### Закономерность 4. «Солнечные дни дают эффект насыщения»
- **Поля:** `sunshine_days`, `sensory_aroma_score`.
- **Тип эффекта:** рост с насыщением (S-образный/плато).
- **Ожидаемый эффект:** ароматика увеличивается при росте солнечных дней до плато.
- **Диаграмма:** точечная + тренд.
  - X: солнечные дни.
  - Y: средний балл ароматики.
  - Сравнение: микрозоны.

### Закономерность 5. «Органика почвы улучшает баланс, но с убывающей отдачей»
- **Поля:** `soil_organic_matter_pct`, `sensory_balance_score`.
- **Тип эффекта:** нелинейная положительная зависимость с насыщением.
- **Ожидаемый эффект:** рост баланса при увеличении органики, затем замедление прироста.
- **Диаграмма:** точечная + сглаживание.
  - X: % органики.
  - Y: балл баланса.
  - Сравнение: типы почв.

### Закономерность 6. «Жара сильнее бьёт по чувствительным сортам»
- **Поля:** `heatwave_days`, `grape_variety`, `wine_quality_index`.
- **Тип эффекта:** взаимодействие факторов.
- **Ожидаемый эффект:** отрицательный наклон качества при росте дней жары, причём для части сортов падение круче.
- **Диаграмма:** линейная (многосерийная) или фасет по сорту.
  - X: дни жары.
  - Y: средний индекс качества.
  - Сравнение: линии разных сортов.

### Закономерность 7. «Болезни снижают качество, но контроль брожения частично компенсирует»
- **Поля:** `disease_pressure_index`, `fermentation_control_score`, `wine_quality_index`.
- **Тип эффекта:** отрицательный основной эффект + смягчающее взаимодействие.
- **Ожидаемый эффект:** при высоком фитодавлении партии с высоким контролем брожения теряют меньше качества.
- **Диаграмма:** точечная/линейная по группам уровня контроля.
  - X: индекс фитодавления.
  - Y: средний индекс качества.
  - Сравнение: низкий/средний/высокий контроль брожения.

### Закономерность 8. «Сахаристость и кислотность: оптимальный коридор, а не максимум»
- **Поля:** `harvest_brix`, `harvest_acidity_g_l`, `sensory_balance_score`.
- **Тип эффекта:** пороговый/оптимизационный (штраф за отклонения от коридора).
- **Ожидаемый эффект:** лучший баланс при умеренной сахаристости и кислотности в оптимальном диапазоне.
- **Диаграмма:** тепловая карта категорий или точечная 2D с цветом.
  - X: сахаристость.
  - Y: кислотность.
  - Цвет/значение: средний балл баланса.

### Закономерность 9. «Выдержка в дубе полезна до порога»
- **Поля:** `oak_aging_months`, `wine_quality_index`, `grape_variety`.
- **Тип эффекта:** нелинейная (рост до оптимума, затем стагнация/лёгкий спад).
- **Ожидаемый эффект:** качество растёт до умеренной выдержки, затем эффект ослабевает.
- **Диаграмма:** линейная по бинам выдержки.
  - X: месяцы выдержки (бины).
  - Y: средний индекс качества.
  - Сравнение: сорта.

### Закономерность 10. «Микрозона и экспозиция формируют терруарный бонус»
- **Поля:** `region_microzone`, `slope_exposure`, `wine_quality_index`.
- **Тип эффекта:** кросс-категориальное взаимодействие.
- **Ожидаемый эффект:** некоторые сочетания микрозоны и экспозиции стабильно дают более высокий индекс.
- **Диаграмма:** тепловая карта категорий или группированная столбчатая.
  - X: микрозона.
  - Y: средний индекс качества.
  - Группы/цвет: экспозиция.

## 5. Самопроверка логической согласованности

- **Q1:** Соответствует ли целевая переменная уровню строки? — **Да.** Все целевые переменные измеряются для конкретной партии.
- **Q2:** Есть ли поля более высокого уровня? — **Нет критичных противоречий.** Даже если `soil_type` или `vineyard_block` могут повторяться, их значение однозначно определено для каждой партии.
- **Q3:** Есть ли дубликаты/тривиально вычисляемые поля? — **Нет.** Избегали полей вроде «месяц», «день недели» и простых производных итогов.
- **Q4:** Есть ли другие смысловые противоречия? — **Нет.** Метрики сбора, погодные факторы и дегустационные оценки находятся на одном уровне наблюдения.

**ИТОГОВАЯ СХЕМА ДАТАСЕТА СФОРМИРОВАНА, ПРОТИВОРЕЧИЯ И ДУБЛИКАТЫ УСТРАНЕНЫ.**

---

# Фаза 2

## 2 A. Код на Python для генерации датасета

```python
import numpy as np
import pandas as pd

np.random.seed(42)

N = 6000  # минимум 5000 строк

# Категориальные справочники
varieties = ["Cabernet_Sauvignon", "Merlot", "Pinot_Noir", "Chardonnay", "Syrah", "Sauvignon_Blanc"]
microzones = ["River_Terrace", "North_Hills", "South_Slope", "Valley_Floor", "Limestone_Ridge"]
soil_types = ["Clay_Loam", "Sandy_Loam", "Limestone", "Gravel", "Silt_Loam"]
exposures = ["North", "South", "East", "West", "Southwest"]
irrigation = ["None", "Standard", "Deficit"]
blocks = [f"Block_{z}_{i:02d}" for z in ["East", "West", "North", "South", "Central"] for i in range(1, 13)]

years = np.arange(2018, 2025)

# Основные поля
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

# Климат
temp_base_by_zone = {
    "River_Terrace": 22.1,
    "North_Hills": 21.0,
    "South_Slope": 23.0,
    "Valley_Floor": 22.4,
    "Limestone_Ridge": 21.6,
}

rain_base_by_zone = {
    "River_Terrace": 430,
    "North_Hills": 460,
    "South_Slope": 390,
    "Valley_Floor": 440,
    "Limestone_Ridge": 410,
}

year_temp_shift = {2018: -0.3, 2019: 0.0, 2020: 0.4, 2021: -0.2, 2022: 0.5, 2023: 0.7, 2024: 0.2}
year_rain_shift = {2018: 15, 2019: -10, 2020: -25, 2021: 30, 2022: -35, 2023: -20, 2024: 10}

growing_temp = np.array([
    temp_base_by_zone[microzone[i]] + year_temp_shift[vintage_year[i]] + np.random.normal(0, 0.8)
    for i in range(N)
])
growing_rain = np.array([
    rain_base_by_zone[microzone[i]] + year_rain_shift[vintage_year[i]] + np.random.normal(0, 55)
    for i in range(N)
])
growing_rain = np.clip(growing_rain, 220, 700)

sunshine_days = np.clip((145 - 0.08 * growing_rain + 2.5 * (growing_temp - 21) + np.random.normal(0, 6, N)), 75, 155).round(0)
heatwave_days = np.clip((1.5 + 1.9 * (growing_temp - 21.5) + np.random.normal(0, 1.8, N)), 0, 22).round(0)

# Болезни: растут от влажности и осадков, снижаются при дефицитном поливе
disease_pressure = (
    25
    + 0.06 * (growing_rain - 420)
    + 0.22 * np.maximum(0, 18 - sunshine_days)
    + np.where(irrig == "Deficit", -4, 0)
    + np.random.normal(0, 4, N)
)
disease_pressure = np.clip(disease_pressure, 5, 85)

# Технология брожения и выдержка
fermentation_control = np.clip(
    68
    + 0.35 * vine_age_years
    + 1.8 * (vintage_year - 2018)  # постепенное улучшение технологий по годам
    + np.where(irrig == "Deficit", 2.5, 0)
    + np.random.normal(0, 6, N),
    40,
    98,
)

oak_aging = np.random.choice([0, 3, 6, 9, 12, 15, 18, 24], size=N, p=[0.06, 0.08, 0.18, 0.2, 0.24, 0.12, 0.08, 0.04])

# Параметры на сборе
variety_brix_base = {
    "Cabernet_Sauvignon": 24.5,
    "Merlot": 24.0,
    "Pinot_Noir": 23.4,
    "Chardonnay": 22.8,
    "Syrah": 24.2,
    "Sauvignon_Blanc": 22.5,
}

harvest_brix = np.array([
    variety_brix_base[variety[i]]
    + 0.18 * (growing_temp[i] - 22)
    + 0.025 * (sunshine_days[i] - 115)
    - 0.015 * (growing_rain[i] - 420)
    + np.random.normal(0, 0.55)
    for i in range(N)
])
harvest_brix = np.clip(harvest_brix, 19.0, 28.0)

harvest_acidity = np.clip(
    8.8 - 0.11 * harvest_brix - 0.03 * (growing_temp - 22) + np.random.normal(0, 0.35, N),
    4.2,
    8.8,
)

# ---------- Скрытые закономерности (сигнал сильнее шума) ----------

# 1) Магистральный эффект сорта (+/- до ~6 пунктов)
variety_effect_map = {
    "Cabernet_Sauvignon": 4.5,
    "Merlot": 2.0,
    "Pinot_Noir": 1.0,
    "Chardonnay": -0.5,
    "Syrah": 3.0,
    "Sauvignon_Blanc": -1.2,
}
variety_effect = np.array([variety_effect_map[v] for v in variety])

# 2) Нелинейный температурный оптимум (парабола, максимум около 22°C)
temp_effect = -0.95 * (growing_temp - 22.0) ** 2 + 5.3

# 3) Осадки: оптимум в центре, штраф на краях
rain_effect = -0.00011 * (growing_rain - 420) ** 2 + 3.8

# 4) Солнечные дни: эффект насыщения (логистический) в аромате
sun_effect_aroma = 6.0 / (1 + np.exp(-(sunshine_days - 108) / 8.0)) - 2.8

# 5) Органика почвы: убывающая отдача в балансе
organic_effect_balance = 4.0 * np.tanh((soil_organic - 2.2) / 1.3)

# 6) Жара сильнее вредит Pinot Noir (взаимодействие)
heat_penalty_base = -0.38 * heatwave_days
heat_penalty_pinot_extra = np.where(variety == "Pinot_Noir", -0.35 * heatwave_days, 0.0)
heat_effect = heat_penalty_base + heat_penalty_pinot_extra

# 7) Болезни снижают качество, контроль брожения смягчает удар
disease_main = -0.14 * disease_pressure
mitigation = 0.055 * disease_pressure * (fermentation_control - 65) / 35

# 8) Оптимальный коридор brix+acidity для баланса
brix_penalty = -0.9 * np.abs(harvest_brix - 24.0)
acidity_penalty = -1.15 * np.abs(harvest_acidity - 6.0)

# 9) Выдержка в дубе: рост до порога и легкий спад после
oak_effect = -0.045 * (oak_aging - 12) ** 2 + 2.5

# 10) Взаимодействие микрозоны и экспозиции (терруарный бонус)
terroir_bonus = np.zeros(N)
terroir_bonus += np.where((microzone == "Limestone_Ridge") & (exposure == "Southwest"), 2.2, 0)
terroir_bonus += np.where((microzone == "River_Terrace") & (exposure == "South"), 1.7, 0)
terroir_bonus += np.where((microzone == "North_Hills") & (exposure == "North"), 1.2, 0)
terroir_bonus += np.where((microzone == "Valley_Floor") & (exposure == "West"), -1.0, 0)

# Доп. слабые корректировки
ph_effect = -1.3 * np.abs(soil_ph - 6.45)
irrig_effect = np.where(irrig == "Deficit", 1.0, np.where(irrig == "None", -0.4, 0.3))
vine_age_effect = 0.08 * np.minimum(vine_age_years, 25) - 0.03 * np.maximum(vine_age_years - 25, 0)

# Базовый латентный уровень качества
latent_quality = (
    73.0
    + variety_effect
    + temp_effect
    + rain_effect
    + heat_effect
    + disease_main
    + mitigation
    + oak_effect
    + terroir_bonus
    + ph_effect
    + irrig_effect
    + vine_age_effect
)

# Целевые переменные (не являются прямыми формулами друг друга)
noise_quality = np.random.normal(0, 2.4, N)
noise_aroma = np.random.normal(0, 2.1, N)
noise_balance = np.random.normal(0, 2.2, N)

sensory_aroma = np.clip(latent_quality + sun_effect_aroma + 0.3 * oak_effect + noise_aroma, 55, 98)
sensory_balance = np.clip(latent_quality + organic_effect_balance + brix_penalty + acidity_penalty + noise_balance, 50, 98)
wine_quality = np.clip(latent_quality + 0.35 * sun_effect_aroma + 0.45 * organic_effect_balance + noise_quality, 50, 99)

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

# Контроль плотности минорного сегмента (чтобы был статистически видим)
minor_segment = df[(df["grape_variety"] == "Pinot_Noir") & (df["heatwave_days"] >= 12)]
if len(minor_segment) < 50:
    idx = df.sample(50 - len(minor_segment), random_state=42).index
    df.loc[idx, "grape_variety"] = "Pinot_Noir"
    df.loc[idx, "heatwave_days"] = np.maximum(df.loc[idx, "heatwave_days"].values, 12)

# Сохранение датасета
df.to_csv("dataset.csv", index=False, encoding="utf-8")
print("dataset.csv сохранён:", df.shape)
```

## 2 B. Учебный кейс со сторителлингом, визуализациями и элементами управления

### 2 B.1 Описание кейса (для студента)

Винодельня «Виноградная Долина» за последние годы резко расширила линейку вин и стала работать с несколькими микрозонами терруара. Технологи заметили, что даже при схожем регламенте производства итоговое качество по партиям заметно колеблется. Руководство считает, что ключ не только в сорте винограда, но и в сочетании погодных факторов, характеристик почвы и управляемости брожения.

Вам передан набор данных по партиям урожая: условия сезона, параметры почвы, сбор, технологические факторы и дегустационные оценки. Ваша задача как аналитика — выявить устойчивые факторы качества и подготовить визуальный обзор для производственной и коммерческой команд.

**Подзадачи в терминах истории:**
1. Помогите главному энологу понять, какие сорта и терруарные зоны стабильно дают более высокое качество.
2. Покажите, как погодные условия сезона связаны с итоговой дегустационной оценкой.
3. Разберитесь, есть ли диапазоны погодных параметров, где качество максимально, а где начинается ухудшение.
4. Оцените, как управляемость брожения помогает при сложных фитосанитарных условиях.
5. Проверьте, как параметры на момент сбора (сахаристость и кислотность) связаны с ощущением баланса вина.
6. Подготовьте рекомендации, какие сегменты партий наиболее перспективны для флагманской линейки.

### 2 B.2 Общие рекомендации по анализу и визуализации

Рекомендуется сначала посчитать базовые агрегаты:
- средние дегустационные показатели по сортам, микрозонам, типам почв и экспозициям;
- средние и медианные показатели по годам урожая;
- распределения ключевых погодных метрик и технологических индексов;
- сравнение долей партий высокого качества по выбранным сегментам;
- динамику показателей по времени (по дате и по винтажу).

Далее соберите не менее 8–10 визуализаций, чтобы покрыть все ключевые эффекты:
1. Столбчатая: средний итоговый индекс по сортам.
2. Точечная + тренд: температура сезона и итоговый индекс.
3. Линейная/биновая: осадки и средний итоговый индекс.
4. Точечная + тренд: солнечные дни и балл ароматики.
5. Точечная + сглаживание: органика почвы и балл баланса.
6. Многосерийная линейная: дни жары против итогового индекса по сортам.
7. Линии по группам контроля: фитодавление и итоговый индекс для разных уровней контроля брожения.
8. Тепловая карта: сочетание сахаристости и кислотности против балла баланса.
9. Линейная/столбчатая по бинам: выдержка в дубе и итоговый индекс (сравнение сортов).
10. Тепловая карта категорий: микрозона × экспозиция и средний итоговый индекс.

Для каждого графика старайтесь явно фиксировать:
- что стоит на горизонтальной оси (время, диапазон метрики, категория);
- что стоит на вертикальной оси (средний дегустационный показатель);
- какие группы сравниваются (сорта, микрозоны, режимы орошения, уровни контроля).

### 2 B.3 Фильтры и элементы управления (обязательный компонент дашборда)

В итоговом дашборде обязательно добавьте интерактивные элементы, чтобы можно было менять условия анализа и проверять устойчивость выводов.

Рекомендуемые фильтры:
- по времени (диапазон дат сбора или выбор винтажей);
- по сорту винограда;
- по микрозоне терруара;
- по режиму орошения;
- по диапазонам ключевых погодных метрик.

Рекомендуемый элемент управления:
- переключатель сценария анализа (например, фокус на определённом сегменте сортов или диапазоне качества), который меняет набор отображаемых партий и позволяет увидеть, как изменяются закономерности.

**Явное требование к студенту:**
- добавить на итоговый дашборд **не менее 2–3 фильтров** по важным измерениям;
- добавить **как минимум один элемент управления**, который меняет условия анализа и влияет на выводы, и описать это влияние в итоговом комментарии.

## 2 C. Код проверки для преподавателя (с графиками)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv("dataset.csv", parse_dates=["harvest_date"])

print("Размер датасета:", df.shape)
print(df[["wine_quality_index", "sensory_aroma_score", "sensory_balance_score"]].describe())

# -------------------------
# 1) Сорт как магистральный фактор качества
# Коэффициент влияния: до ~+4.5/-1.2 к базовому уровню, шум quality ~2.4
# Поля графика: X=grape_variety, Y=mean(wine_quality_index)
# Ожидаемо: устойчивое ранжирование сортов по среднему качеству
# -------------------------
m1 = df.groupby("grape_variety")["wine_quality_index"].mean().sort_values(ascending=False)
print("\n[1] Разница лидер-аутсайдер по сортам:", (m1.iloc[0] - m1.iloc[-1]).round(2))
plt.figure(figsize=(8, 4))
sns.barplot(x=m1.index, y=m1.values, palette="viridis")
plt.title("[1] Средний wine_quality_index по сортам")
plt.xticks(rotation=25)
plt.ylabel("Средний индекс качества")
plt.tight_layout()
plt.show()

# -------------------------
# 2) Нелинейный температурный оптимум
# Коэффициент влияния: параболический эффект до ~+5.3 вблизи оптимума
# Шум quality ~2.4
# Поля: X=growing_season_temp_avg, Y=wine_quality_index
# Ожидаемо: колокол (максимум в среднем диапазоне температур)
# -------------------------
corr2 = df[["growing_season_temp_avg", "wine_quality_index"]].corr().iloc[0, 1]
print("[2] Линейная корреляция temp-quality (может быть умеренной из-за нелинейности):", round(corr2, 3))
plt.figure(figsize=(7, 4))
sns.regplot(data=df, x="growing_season_temp_avg", y="wine_quality_index", lowess=True,
            scatter_kws={"alpha": 0.25, "s": 12}, line_kws={"color": "red"})
plt.title("[2] Нелинейная связь температуры и качества")
plt.tight_layout()
plt.show()

# -------------------------
# 3) Осадки: оптимум в центре
# Коэффициент влияния: ~-0.00011*(rain-420)^2 + 3.8, шум quality ~2.4
# Поля: X=rain_bin, Y=mean(wine_quality_index)
# Ожидаемо: ухудшение на краях по осадкам
# -------------------------
df["rain_bin"] = pd.cut(df["growing_season_rain_mm"], bins=10)
m3 = df.groupby("rain_bin", observed=False)["wine_quality_index"].mean()
print("[3] Max-Min среднего quality по бинам осадков:", round(m3.max() - m3.min(), 2))
plt.figure(figsize=(9, 4))
m3.plot(marker="o")
plt.title("[3] Среднее качество по бинам осадков")
plt.ylabel("Средний индекс качества")
plt.xlabel("Бины осадков")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# -------------------------
# 4) Солнечные дни и насыщение в аромате
# Коэффициент влияния: логистический, амплитуда ~6 пунктов, шум aroma ~2.1
# Поля: X=sunshine_days, Y=sensory_aroma_score
# Ожидаемо: рост с выходом на плато
# -------------------------
plt.figure(figsize=(7, 4))
sns.regplot(data=df, x="sunshine_days", y="sensory_aroma_score", lowess=True,
            scatter_kws={"alpha": 0.22, "s": 10}, line_kws={"color": "darkorange"})
plt.title("[4] Солнечные дни и ароматика (эффект насыщения)")
plt.tight_layout()
plt.show()

# -------------------------
# 5) Органика почвы и баланс (убывающая отдача)
# Коэффициент влияния: 4*tanh(...), амплитуда ~8, шум balance ~2.2
# Поля: X=soil_organic_matter_pct, Y=sensory_balance_score
# Ожидаемо: рост с замедлением на высоких значениях
# -------------------------
plt.figure(figsize=(7, 4))
sns.regplot(data=df, x="soil_organic_matter_pct", y="sensory_balance_score", lowess=True,
            scatter_kws={"alpha": 0.22, "s": 10}, line_kws={"color": "green"})
plt.title("[5] Органика почвы и баланс")
plt.tight_layout()
plt.show()

# -------------------------
# 6) Жара сильнее вредит Pinot Noir
# Коэффициент: базово -0.38/день жары, для Pinot дополнительный -0.35/день
# Шум quality ~2.4
# Поля: X=heatwave_days, Y=mean(wine_quality_index), group=grape_variety
# Ожидаемо: более крутой отрицательный наклон для Pinot Noir
# -------------------------
heat_group = (
    df.groupby(["grape_variety", "heatwave_days"])["wine_quality_index"].mean().reset_index()
)
plt.figure(figsize=(9, 5))
for v in ["Pinot_Noir", "Cabernet_Sauvignon", "Merlot", "Syrah"]:
    sub = heat_group[heat_group["grape_variety"] == v]
    plt.plot(sub["heatwave_days"], sub["wine_quality_index"], marker="o", label=v)
plt.title("[6] Влияние дней жары по сортам")
plt.xlabel("Дни жары")
plt.ylabel("Средний индекс качества")
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------
# 7) Болезни и компенсация контролем брожения
# Коэффициенты: disease -0.14*index; mitigation +0.055*index*control_factor
# Шум quality ~2.4
# Поля: X=disease_pressure_index, Y=wine_quality_index, group=уровень контроля
# Ожидаемо: при высоком контроле спад качества от болезней более пологий
# -------------------------
df["control_group"] = pd.qcut(df["fermentation_control_score"], q=3, labels=["Low", "Mid", "High"])
plt.figure(figsize=(8, 5))
sns.lmplot(
    data=df.sample(2500, random_state=42),
    x="disease_pressure_index",
    y="wine_quality_index",
    hue="control_group",
    lowess=True,
    height=5,
    aspect=1.4,
    scatter_kws={"alpha": 0.2, "s": 12},
)
plt.title("[7] Болезни vs качество при разных уровнях контроля брожения")
plt.tight_layout()
plt.show()

# Числовая проверка: разница slope proxy между High и Low
high = df[df["control_group"] == "High"]["wine_quality_index"].corr(df[df["control_group"] == "High"]["disease_pressure_index"])
low = df[df["control_group"] == "Low"]["wine_quality_index"].corr(df[df["control_group"] == "Low"]["disease_pressure_index"])
print("[7] Корреляция quality~disease, High control:", round(high, 3), "Low control:", round(low, 3))

# -------------------------
# 8) Оптимальный коридор brix и acidity для баланса
# Коэффициенты: штрафы -0.9*|brix-24| и -1.15*|acidity-6|
# Шум balance ~2.2
# Поля: X=harvest_brix_bin, Y=harvest_acidity_bin, color=mean(balance)
# Ожидаемо: лучшая зона вблизи центрального коридора
# -------------------------
df["brix_bin"] = pd.cut(df["harvest_brix"], bins=8)
df["acid_bin"] = pd.cut(df["harvest_acidity_g_l"], bins=8)
heat8 = df.pivot_table(index="acid_bin", columns="brix_bin", values="sensory_balance_score", aggfunc="mean")
plt.figure(figsize=(9, 6))
sns.heatmap(heat8, cmap="YlGnBu")
plt.title("[8] Баланс по сочетанию сахаристости и кислотности")
plt.xlabel("Бины sugar (Brix)")
plt.ylabel("Бины acidity")
plt.tight_layout()
plt.show()

# -------------------------
# 9) Выдержка в дубе: рост до порога
# Коэффициент: -0.045*(oak-12)^2 + 2.5, шум quality ~2.4
# Поля: X=oak_aging_months, Y=mean(wine_quality_index)
# Ожидаемо: максимум в области умеренной выдержки
# -------------------------
m9 = df.groupby("oak_aging_months")["wine_quality_index"].mean().sort_index()
print("[9] Лучший интервал выдержки (по среднему):", m9.idxmax(), "месяцев")
plt.figure(figsize=(7, 4))
plt.plot(m9.index, m9.values, marker="o")
plt.title("[9] Средний quality по длительности дубовой выдержки")
plt.xlabel("Месяцы выдержки")
plt.ylabel("Средний индекс качества")
plt.tight_layout()
plt.show()

# -------------------------
# 10) Микрозона × экспозиция: терруарный бонус
# Коэффициент: бонусы до +2.2, штраф до -1.0, шум quality ~2.4
# Поля: X=region_microzone, Y=slope_exposure, value=mean(wine_quality_index)
# Ожидаемо: видимые «тёплые» ячейки лучших комбинаций
# -------------------------
heat10 = df.pivot_table(index="region_microzone", columns="slope_exposure", values="wine_quality_index", aggfunc="mean")
best_pair = heat10.stack().idxmax()
print("[10] Лучшая комбинация microzone×exposure:", best_pair)
plt.figure(figsize=(8, 5))
sns.heatmap(heat10, annot=True, fmt=".1f", cmap="RdYlGn")
plt.title("[10] Терруарный профиль качества: микрозона × экспозиция")
plt.tight_layout()
plt.show()
```
