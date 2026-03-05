import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Установим фиксированный seed для воспроизводимости
np.random.seed(42)

# Параметры датасета
n_rows = 5000

# Создадим базовые списки для генерации данных
weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Foggy']
package_types = ['Standard', 'Fragile', 'Perishable', 'Oversized', 'Hazardous']
delivery_zones = ['Residential', 'Commercial', 'Industrial', 'Rural']
delivery_areas = ['Urban', 'Suburban', 'Rural']
traffic_levels = ['Low', 'Medium', 'High']
drone_models = ['ND-Light-Carry-X1', 'ND-Heavy-Lift-X1', 'ND-Speedster-X1', 'ND-AllTerrain-X1']

# Генерация основных данных
data = {
    'delivery_id': [f'D-{i:06d}' for i in range(1, n_rows + 1)],
    'drone_id': [f'DRN-{np.random.randint(1, 101):03d}-{chr(65 + np.random.randint(0, 3))}' for _ in range(n_rows)],
    'route_id': [f'RT-{np.random.choice(["MOW", "SPB", "NSK", "EKB", "KZN"])}-{np.random.choice(["MOW", "SPB", "NSK", "EKB", "KZN"])}-{np.random.randint(1, 21):02d}' for _ in range(n_rows)],
    'delivery_date': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)],
    'departure_time': [datetime(2023, 1, 1) + timedelta(hours=np.random.randint(6, 20), minutes=np.random.randint(0, 60)) for _ in range(n_rows)],
    'weather_condition': np.random.choice(weather_conditions, size=n_rows, p=[0.3, 0.35, 0.2, 0.1, 0.05]),
    'temperature': np.random.normal(15, 12, size=n_rows),
    'wind_speed': np.clip(np.random.exponential(4, size=n_rows), 0, 20),
    'precipitation_mm': np.clip(np.random.exponential(1.5, size=n_rows), 0, 20),
    'distance_km': np.random.gamma(2, 2, size=n_rows),
    'battery_level_start': np.random.uniform(80, 100, size=n_rows),
    'package_weight_kg': np.random.gamma(1.5, 1.5, size=n_rows) * 3,
    'package_type': np.random.choice(package_types, size=n_rows, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
    'delivery_zone': np.random.choice(delivery_zones, size=n_rows, p=[0.4, 0.3, 0.2, 0.1]),
    'delivery_area': np.random.choice(delivery_areas, size=n_rows, p=[0.5, 0.3, 0.2]),
    'traffic_congestion': np.random.choice(traffic_levels, size=n_rows, p=[0.3, 0.5, 0.2]),
    'pilot_experience_years': np.random.gamma(2, 1.5, size=n_rows),
    'drone_model': np.random.choice(drone_models, size=n_rows, p=[0.3, 0.25, 0.25, 0.2])
}

df = pd.DataFrame(data)

# #1: Влияние скорости ветра на успешность доставки (пороговый эффект)
wind_factor = np.where(df['wind_speed'] > 10, 0.75, 1.0)  # при ветре > 10 м/с успех падает на 25%

# #2: Сезонность в успешности доставок
months = df['delivery_date'].apply(lambda x: x.month)
seasonal_factor = np.where((months >= 12) | (months <= 2), 0.85, 1.0)  # зимой успех падает на 15%

# #3: Влияние веса груза на потребление батареи
base_battery_consumption = 30 + (df['package_weight_kg'] * 5)  # +5% за каждый кг
noise = np.random.normal(0, 3, size=n_rows)  # небольшой шум
df['battery_consumption_rate'] = base_battery_consumption + noise

# #4: Влияние опыта оператора на успешность (насыщение после 5 лет)
experience_factor = np.minimum(1 + (df['pilot_experience_years'] * 0.08), 1.4)  # до 5 лет растет, потом стабилизируется

# #5: Влияние температуры на точность приземления (оптимально 15-25°C)
temp_deviation = abs(df['temperature'] - 20)  # отклонение от оптимальной температуры 20°C
df['landing_accuracy_m'] = 1.0 + (temp_deviation * 0.05) + np.random.normal(0, 0.2, size=n_rows)

# #6: Влияние типа упаковки на успешность
package_factor = np.where(df['package_type'] == 'Fragile', 0.9, 1.0)  # хрупкие грузы имеют -10% успеха

# #7: Влияние воздушного трафика на продолжительность полета
traffic_multiplier = np.where(df['traffic_congestion'] == 'High', 1.15, 
                    np.where(df['traffic_congestion'] == 'Medium', 1.07, 1.0))
base_flight_time = (df['distance_km'] / 15) * 60  # базовое время полета (15 км/ч)
df['flight_duration_min'] = base_flight_time * traffic_multiplier + np.random.normal(0, 5, size=n_rows)

# #8: Взаимодействие между весом груза и погодными условиями
weight_weather_interaction = np.where((df['weather_condition'] == 'Stormy') & (df['package_weight_kg'] > 3), 0.7, 1.0)

# #9: Влияние модели дрона на эффективность в зависимости от погоды
drone_weather_efficiency = np.where(((df['drone_model'] == 'ND-Light-Carry-X1') | (df['drone_model'] == 'ND-Speedster-X1')) & 
                                   ((df['weather_condition'] == 'Stormy') | (df['weather_condition'] == 'Rainy')), 
                                   1.15, 1.0)  # легкие дроны хуже в плохую погоду

# #10: Влияние района доставки на точность приземления
area_factor = np.where(df['delivery_area'] == 'Urban', 1.2, 1.0)  # в городах точность хуже
df['landing_accuracy_m'] = df['landing_accuracy_m'] * area_factor

# Рассчитываем конечный уровень батареи
battery_used = (df['flight_duration_min'] / 60) * df['battery_consumption_rate'] / 100
df['battery_level_end'] = df['battery_level_start'] - (battery_used * 100)
df['battery_level_end'] = np.clip(df['battery_level_end'], 0, 100)

# Рассчитываем время прибытия
df['arrival_time'] = pd.to_datetime(df['departure_time']) + pd.to_timedelta(df['flight_duration_min'], unit='minutes')

# Рассчитываем базовую вероятность успеха
base_success_prob = 0.9
success_prob = (base_success_prob * 
                wind_factor * 
                seasonal_factor * 
                experience_factor * 
                package_factor * 
                weight_weather_interaction * 
                drone_weather_efficiency)

# Добавляем немного случайности и ограничиваем диапазон
success_prob = np.clip(success_prob + np.random.normal(0, 0.05, size=n_rows), 0.5, 1.0)
df['delivery_success'] = np.random.binomial(1, success_prob, size=n_rows)

# Округляем числовые значения
numeric_cols = ['temperature', 'wind_speed', 'precipitation_mm', 'distance_km', 
                'battery_level_start', 'battery_level_end', 'package_weight_kg',
                'flight_duration_min', 'landing_accuracy_m', 'battery_consumption_rate',
                'pilot_experience_years']
for col in numeric_cols:
    df[col] = np.round(df[col], 2)

# Убедимся, что все строки в нужном диапазоне
df = df.head(n_rows)

# Сохраняем датасет
df.to_csv('dataset.csv', index=False)
print(f"Датасет сгенерирован: {len(df)} строк, {len(df.columns)} столбцов")
print("\nПервые 5 строк:")
print(df.head())
print("\nИнформация о датасете:")
print(df.info())