# Імпортуємо необхідні бібліотеки
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub

# Перевіряємо наявність директорії для збереження графіків
plots_dir = 'plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

# Отримуємо шлях до набору даних
path = kagglehub.dataset_download("maicolab/university-admission")
print("Шлях до файлів набору даних:", path)

# Знаходимо CSV файли в директорії
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

if csv_files:
    # Беремо перший CSV файл
    csv_file = os.path.join(path, csv_files[0])
    print(f"Завантаження файлу: {csv_files[0]}")
    
    # Читаємо дані з CSV файлу
    df = pd.read_csv(csv_file)
    
    # Виводимо інформацію про набір даних
    print("\nРозмір набору даних:", df.shape)
    print("\nПерші 5 рядків даних:")
    print(df.head())
    
    # Перетворюємо категоріальні змінні на числові для аналізу
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        df[col] = pd.Categorical(df[col]).codes
    
    # Виводимо описову статистику
    print("\nОписова статистика:")
    print(df.describe())
    
    # Вибираємо числові стовпці для візуалізації
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        # Гістограма для першого числового стовпця
        plt.figure(figsize=(10, 6))
        sns.histplot(df[numeric_cols[0]], bins=10, kde=True)
        plt.title(f'Гістограма для {numeric_cols[0]}')
        plt.savefig(os.path.join(plots_dir, 'histogram.png'))
        plt.close()
        print(f"Гістограму збережено як '{os.path.join(plots_dir, 'histogram.png')}'")
        
        # Коробкова діаграма для першого числового стовпця
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df[numeric_cols[0]])
        plt.title(f'Коробкова діаграма для {numeric_cols[0]}')
        plt.savefig(os.path.join(plots_dir, 'boxplot.png'))
        plt.close()
        print(f"Коробкову діаграму збережено як '{os.path.join(plots_dir, 'boxplot.png')}'")
        
        # Діаграма розсіювання для перших двох числових стовпців (якщо є більше одного)
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]])
            plt.title(f'Діаграма розсіювання: {numeric_cols[0]} vs {numeric_cols[1]}')
            plt.savefig(os.path.join(plots_dir, 'scatterplot.png'))
            plt.close()
            print(f"Діаграму розсіювання збережено як '{os.path.join(plots_dir, 'scatterplot.png')}'")
        
        # Обчислення кореляційної матриці
        correlation_matrix = df.corr()
        
        # Теплова карта кореляції
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Теплова карта кореляції')
        plt.savefig(os.path.join(plots_dir, 'correlation_heatmap.png'))
        plt.close()
        print(f"Теплову карту кореляції збережено як '{os.path.join(plots_dir, 'correlation_heatmap.png')}'")
        
        # Додаткові візуалізації
        # Парні графіки для перших 5 числових стовпців (якщо є більше одного)
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(15, 10))
            sns.pairplot(df[numeric_cols[:5]] if len(numeric_cols) > 5 else df[numeric_cols])
            plt.savefig(os.path.join(plots_dir, 'pairplot.png'))
            plt.close()
            print(f"Парні графіки збережено як '{os.path.join(plots_dir, 'pairplot.png')}'")
    else:
        print("Числових стовпців для візуалізації не знайдено")
else:
    print("CSV файли не знайдено в завантаженому наборі даних")

print("\nВізуалізація даних завершена!")