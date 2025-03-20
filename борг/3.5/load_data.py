# Імпортуємо необхідні бібліотеки
import os
import pandas as pd
import kagglehub
import matplotlib.pyplot as plt

# Завантажуємо набір даних про прийом до університету
print("Завантаження набору даних...")
path = kagglehub.dataset_download("maicolab/university-admission")
print("Шлях до файлів набору даних:", path)

# Перевіряємо вміст директорії з даними
print("\nФайли в директорії з даними:")
for file in os.listdir(path):
    print(f"- {file}")

# Завантажуємо CSV файл за допомогою Pandas
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

if csv_files:
    # Беремо перший CSV файл для прикладу
    csv_file = os.path.join(path, csv_files[0])
    print(f"\nЗавантаження файлу: {csv_files[0]}")
    
    # Читаємо дані з CSV файлу
    df = pd.read_csv(csv_file)
    
    # Спробуємо перетворити стовпець 'Puntaje' у числовий формат
    try:
        # Замінюємо коми на крапки та видаляємо нечислові символи
        df['Puntaje'] = df['Puntaje'].str.replace(',', '.').str.replace(' ', '')
        # Перетворюємо у числовий формат
        df['Puntaje'] = pd.to_numeric(df['Puntaje'], errors='coerce')
        print("\nСтовпець 'Puntaje' перетворено у числовий формат")
    except Exception as e:
        print(f"\nПомилка при перетворенні стовпця 'Puntaje': {e}")
    
    # Виводимо інформацію про набір даних
    print("\nРозмір набору даних:", df.shape)
    print("\nПерші 5 рядків даних:")
    print(df.head())
    
    print("\nІнформація про набір даних:")
    print(df.info())
    
    print("\nСтатистичні показники:")
    print(df.describe())
    
    # Візуалізація даних (приклад)
    print("\nСтворення простої візуалізації...")
    if len(df.columns) > 1:
        # Вибираємо числові стовпці для візуалізації
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(10, 6))
            plt.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
            plt.xlabel(numeric_cols[0])
            plt.ylabel(numeric_cols[1])
            plt.title(f'Діаграма розсіювання: {numeric_cols[0]} vs {numeric_cols[1]}')
            plt.savefig('scatter_plot.png')
            print("Діаграму розсіювання збережено як 'scatter_plot.png'")
        else:
            print("Недостатньо числових стовпців для створення діаграми розсіювання")
else:
    print("CSV файли не знайдено в завантаженому наборі даних")

print("\nЗавантаження та аналіз даних завершено!")