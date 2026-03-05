import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загружаем датасет
df = pd.read_csv('dataset.csv')

# Устанавливаем параметры для графиков
plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style("whitegrid")

print("=== ПРОВЕРКА ЗАКОНОМЕРНОСТЕЙ ===\n")

# #1: Влияние скорости ветра на успешность доставки (пороговый эффект)
print("1. Проверка: Влияние скорости ветра на успешность доставки")
high_wind_success = df[df['wind_speed'] > 10]['delivery_success'].mean()
low_wind_success = df[df['wind_speed'] <= 10]['delivery_success'].mean()
print(f"   Успешность при ветре > 10 м/с: {high_wind_success:.3f}")
print(f"   Успешность при ветре <= 10 м/с: {low_wind_success:.3f}")
print(f"   Разница: {low_wind_success - high_wind_success:.3f} ({((low_wind_success - high_wind_success)/low_wind_success)*100:.1f}%)")
print(f"   Ожидаемый эффект: снижение успеха при сильном ветре (~25%)")

# Визуализация
plt.figure(figsize=(10, 6))
wind_groups = pd.cut(df['wind_speed'], bins=[0, 10, 20], labels=['<=10 м/с', '>10 м/с'])
wind_success = df.groupby(wind_groups)['delivery_success'].mean()
plt.bar(wind_success.index, wind_success.values)
plt.title('Успешность доставки в зависимости от скорости ветра')
plt.ylabel('Доля успешных доставок')
plt.xlabel('Скорость ветра')
plt.show()

print("\n" + "="*50 + "\n")

# #2: Сезонность в успешности доставок
print("2. Проверка: Сезонность в успешности доставок")
df['month'] = pd.to_datetime(df['delivery_date']).dt.month
winter_months = [12, 1, 2]
summer_months = [6, 7, 8]
winter_success = df[df['month'].isin(winter_months)]['delivery_success'].mean()
summer_success = df[df['month'].isin(summer_months)]['delivery_success'].mean()
print(f"   Успешность зимой: {winter_success:.3f}")
print(f"   Успешность летом: {summer_success:.3f}")
print(f"   Разница: {summer_success - winter_success:.3f} ({((summer_success - winter_success)/summer_success)*100:.1f}%)")
print(f"   Ожидаемый эффект: снижение успеха зимой (~15%)")

# Визуализация
monthly_success = df.groupby('month')['delivery_success'].mean()
plt.figure(figsize=(12, 6))
plt.plot(monthly_success.index, monthly_success.values, marker='o')
plt.title('Месячная успешность доставок (сезонность)')
plt.ylabel('Доля успешных доставок')
plt.xlabel('Месяц')
plt.grid(True)
plt.show()

print("\n" + "="*50 + "\n")

# #3: Влияние веса груза на потребление батареи
print("3. Проверка: Влияние веса груза на потребление батареи")
correlation = df['package_weight_kg'].corr(df['battery_consumption_rate'])
print(f"   Корреляция между весом груза и расходом батареи: {correlation:.3f}")
print(f"   Ожидаемый эффект: положительная корреляция (~0.7)")

# Визуализация
plt.figure(figsize=(10, 6))
plt.scatter(df['package_weight_kg'], df['battery_consumption_rate'], alpha=0.5)
z = np.polyfit(df['package_weight_kg'], df['battery_consumption_rate'], 1)
p = np.poly1d(z)
plt.plot(df['package_weight_kg'], p(df['package_weight_kg']), "r--", alpha=0.8)
plt.title('Расход батареи в зависимости от веса груза')
plt.xlabel('Вес груза (кг)')
plt.ylabel('Расход батареи (%)')
plt.show()

print("\n" + "="*50 + "\n")

# #4: Влияние опыта оператора на успешность (насыщение после 5 лет)
print("4. Проверка: Влияние опыта оператора на успешность (насыщение)")
df['exp_group'] = pd.cut(df['pilot_experience_years'], bins=[0, 3, 5, 10, 20], labels=['<3 лет', '3-5 лет', '5-10 лет', '>10 лет'])
exp_success = df.groupby('exp_group')['delivery_success'].mean()
print("   Успешность по группам опыта:")
for group, success_rate in exp_success.items():
    print(f"     {group}: {success_rate:.3f}")
print(f"   Ожидаемый эффект: рост до 5 лет, затем насыщение")

# Визуализация
plt.figure(figsize=(10, 6))
plt.plot(range(len(exp_success)), exp_success.values, marker='o')
plt.xticks(range(len(exp_success)), exp_success.index)
plt.title('Успешность доставки в зависимости от опыта пилота')
plt.ylabel('Доля успешных доставок')
plt.xlabel('Опыт пилота')
plt.grid(True)
plt.show()

print("\n" + "="*50 + "\n")

# #5: Влияние температуры на точность приземления (оптимально 15-25°C)
print("5. Проверка: Влияние температуры на точность приземления")
# Рассчитаем отклонение от оптимальной температуры (20°C)
df['temp_deviation'] = abs(df['temperature'] - 20)
correlation_temp = df['temp_deviation'].corr(df['landing_accuracy_m'])
print(f"   Корреляция между отклонением от 20°C и точностью: {correlation_temp:.3f}")
print(f"   Ожидаемый эффект: положительная корреляция (точность падает при отклонении)")

# Визуализация
plt.figure(figsize=(10, 6))
plt.scatter(df['temperature'], df['landing_accuracy_m'], alpha=0.5)
plt.axvline(x=20, color='red', linestyle='--', label='Оптимальная температура 20°C')
plt.title('Точность приземления в зависимости от температуры')
plt.xlabel('Температура (°C)')
plt.ylabel('Точность приземления (м)')
plt.legend()
plt.show()

print("\n" + "="*50 + "\n")

# #6: Влияние типа упаковки на успешность
print("6. Проверка: Влияние типа упаковки на успешность")
package_success = df.groupby('package_type')['delivery_success'].mean().sort_values(ascending=False)
print("   Успешность по типам грузов:")
for pkg_type, success_rate in package_success.items():
    print(f"     {pkg_type}: {success_rate:.3f}")
print(f"   Ожидаемый эффект: хрупкие грузы имеют ниже успешность (~10% меньше)")

# Визуализация
plt.figure(figsize=(10, 6))
plt.bar(package_success.index, package_success.values)
plt.title('Успешность доставки по типам грузов')
plt.ylabel('Доля успешных доставок')
plt.xlabel('Тип груза')
plt.xticks(rotation=45)
plt.show()

print("\n" + "="*50 + "\n")

# #7: Влияние воздушного трафика на продолжительность полета
print("7. Проверка: Влияние воздушного трафика на продолжительность полета")
traffic_duration = df.groupby('traffic_congestion')['flight_duration_min'].mean().reindex(['Low', 'Medium', 'High'])
print("   Средняя продолжительность полета по уровню трафика:")
for traffic_level, duration in traffic_duration.items():
    print(f"     {traffic_level}: {duration:.2f} мин")
print(f"   Ожидаемый эффект: рост продолжительности с увеличением трафика")

# Визуализация
plt.figure(figsize=(10, 6))
plt.bar(traffic_duration.index, traffic_duration.values)
plt.title('Средняя продолжительность полета по уровню воздушного трафика')
plt.ylabel('Средняя продолжительность (мин)')
plt.xlabel('Уровень трафика')
plt.show()

print("\n" + "="*50 + "\n")

# #8: Взаимодействие между весом груза и погодными условиями
print("8. Проверка: Взаимодействие между весом груза и погодными условиями")
stormy_heavy = df[(df['weather_condition'] == 'Stormy') & (df['package_weight_kg'] > 3)]['delivery_success'].mean()
stormy_light = df[(df['weather_condition'] == 'Stormy') & (df['package_weight_kg'] <= 3)]['delivery_success'].mean()
print(f"   Успешность при шторме с тяжелым грузом (>3 кг): {stormy_heavy:.3f}")
print(f"   Успешность при шторме с легким грузом (≤3 кг): {stormy_light:.3f}")
print(f"   Разница: {stormy_light - stormy_heavy:.3f}")
print(f"   Ожидаемый эффект: значительно хуже при шторме с тяжелым грузом")

# Визуализация
plt.figure(figsize=(10, 6))
stormy_data = df[df['weather_condition'] == 'Stormy']
weight_groups = pd.cut(stormy_data['package_weight_kg'], bins=[0, 3, 15], labels=['≤3 кг', '>3 кг'])
stormy_success_by_weight = stormy_data.groupby(weight_groups)['delivery_success'].mean()
plt.bar(stormy_success_by_weight.index, stormy_success_by_weight.values)
plt.title('Успешность доставки при шторме в зависимости от веса груза')
plt.ylabel('Доля успешных доставок')
plt.xlabel('Вес груза')
plt.show()

print("\n" + "="*50 + "\n")

# #9: Влияние модели дрона на эффективность в зависимости от погоды
print("9. Проверка: Влияние модели дрона на эффективность в зависимости от погоды")
bad_weather_drones = df[((df['drone_model'] == 'ND-Light-Carry-X1') | (df['drone_model'] == 'ND-Speedster-X1')) & 
                       ((df['weather_condition'] == 'Stormy') | (df['weather_condition'] == 'Rainy'))]
good_weather_drones = df[~((df['drone_model'] == 'ND-Light-Carry-X1') | (df['drone_model'] == 'ND-Speedster-X1')) | 
                         ~((df['weather_condition'] == 'Stormy') | (df['weather_condition'] == 'Rainy'))]

bad_weather_success = bad_weather_drones['delivery_success'].mean()
good_weather_success = good_weather_drones['delivery_success'].mean()

print(f"   Успешность легких дронов в плохую погоду: {bad_weather_success:.3f}")
print(f"   Успешность других комбинаций: {good_weather_success:.3f}")
print(f"   Разница: {good_weather_success - bad_weather_success:.3f}")
print(f"   Ожидаемый эффект: легкие дроны хуже в плохую погоду")

# Визуализация
plt.figure(figsize=(12, 6))
drone_weather_success = df.groupby(['drone_model', 'weather_condition'])['delivery_success'].mean().unstack()
bad_weather_cols = [col for col in drone_weather_success.columns if col in ['Stormy', 'Rainy']]
light_drones = ['ND-Light-Carry-X1', 'ND-Speedster-X1']
heavy_drones = ['ND-Heavy-Lift-X1', 'ND-AllTerrain-X1']

bad_weather_light = drone_weather_success.loc[light_drones, bad_weather_cols].mean().mean() if bad_weather_cols else 0
bad_weather_heavy = drone_weather_success.loc[heavy_drones, bad_weather_cols].mean().mean() if bad_weather_cols else 0

plt.bar(['Легкие дроны в плохую погоду', 'Тяжелые дроны в плохую погоду'], [bad_weather_light, bad_weather_heavy])
plt.title('Сравнение успешности разных моделей дронов в плохую погоду')
plt.ylabel('Доля успешных доставок')
plt.show()

print("\n" + "="*50 + "\n")

# #10: Влияние района доставки на точность приземления
print("10. Проверка: Влияние района доставки на точность приземления")
area_accuracy = df.groupby('delivery_area')['landing_accuracy_m'].mean().sort_values()
print("   Средняя точность приземления по районам:")
for area, accuracy in area_accuracy.items():
    print(f"     {area}: {accuracy:.2f} м")
print(f"   Ожидаемый эффект: хуже точность в городских районах")

# Визуализация
plt.figure(figsize=(10, 6))
plt.bar(area_accuracy.index, area_accuracy.values)
plt.title('Средняя точность приземления по типу района')
plt.ylabel('Точность приземления (м)')
plt.xlabel('Тип района')
plt.show()

print("\n" + "="*50 + "\n")
print("=== ВАЛИДАЦИЯ ЗАКОНОМЕРНОСТЕЙ ЗАВЕРШЕНА ===")