# Імпортуємо необхідні бібліотеки
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

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
    
    # Спробуємо перетворити стовпець 'Puntaje' у числовий формат, якщо він існує
    try:
        if 'Puntaje' in df.columns:
            # Перевіряємо, чи стовпець є об'єктного типу (рядки)
            if df['Puntaje'].dtype == 'object':
                # Замінюємо коми на крапки та видаляємо нечислові символи
                # Спочатку перевіряємо, чи всі значення є рядками
                df['Puntaje'] = df['Puntaje'].astype(str)
                # Тепер безпечно застосовуємо методи рядків
                df['Puntaje'] = df['Puntaje'].str.replace(',', '.').str.replace(' ', '')
                # Перетворюємо у числовий формат
                df['Puntaje'] = pd.to_numeric(df['Puntaje'], errors='coerce')
                print("\nСтовпець 'Puntaje' перетворено у числовий формат")
            else:
                print("\nСтовпець 'Puntaje' вже має числовий формат")
        else:
            print("\nСтовпець 'Puntaje' не знайдено в наборі даних")
    except Exception as e:
        print(f"\nПомилка при перетворенні стовпця 'Puntaje': {e}")
        print("Продовжуємо виконання скрипту...")
    
    # Перевірка на пропущені значення
    print("\nКількість пропущених значень у кожному стовпці:")
    print(df.isnull().sum())
    
    # Заповнення пропущених значень середнім значенням для числових стовпців
    print("\nЗаповнення пропущених значень середнім значенням для числових стовпців...")
    df.fillna(df.mean(), inplace=True)
    
    # Видалення дублікатів
    print("\nВидалення дублікатів...")
    duplicates_count = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    print(f"Видалено {duplicates_count} дублікатів")
    
    # Перетворення категоріальних змінних на числові
    print("\nПеретворення категоріальних змінних на числові...")
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        print(f"Перетворення стовпця '{col}'")
        df[col] = df[col].astype('category').cat.codes
    
    # Виводимо описову статистику
    print("\nОписова статистика:")
    print(df.describe())
    
    # Обчислення кореляційної матриці
    correlation_matrix = df.corr()
    print("\nКореляційна матриця:")
    print(correlation_matrix)
    
    # Вибираємо числові стовпці для моделювання
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) >= 2:
        print("\n--- Підготовка даних для лінійної регресії ---")
        
        # Визначаємо цільову змінну (останній стовпець) та ознаки (всі інші числові стовпці)
        target_column = numeric_cols[-1]
        feature_columns = numeric_cols[:-1]
        
        print(f"Цільова змінна: {target_column}")
        print(f"Ознаки: {', '.join(feature_columns)}")
        
        # Перевіряємо, чи є достатньо ознак для моделювання
        if len(feature_columns) < 2:
            # Якщо менше 2 ознак, використовуємо всі числові стовпці як ознаки, а останній як цільову змінну
            target_column = numeric_cols[-1]
            feature_columns = numeric_cols[:-1]
            print("\nНедостатньо ознак для моделювання. Використовуємо всі числові стовпці як ознаки.")
        
        # Розділяємо дані на ознаки та цільову змінну
        X = df[feature_columns]
        y = df[target_column]
        
        # Розділяємо дані на навчальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"\nРозмір навчальної вибірки: {X_train.shape}")
        print(f"Розмір тестової вибірки: {X_test.shape}")
        
        # Створюємо та навчаємо модель лінійної регресії
        print("\n--- Навчання моделі лінійної регресії ---")
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Виводимо коефіцієнти моделі
        print("\nКоефіцієнти моделі:")
        for feature, coef in zip(feature_columns, model.coef_):
            print(f"{feature}: {coef:.4f}")
        print(f"Вільний член (Intercept): {model.intercept_:.4f}")
        
        # Робимо прогноз на тестовій вибірці
        y_pred = model.predict(X_test)
        
        # Оцінюємо якість моделі
        print("\n--- Оцінка якості моделі ---")
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Середньоквадратична помилка (MSE): {mse:.4f}")
        print(f"Корінь з середньоквадратичної помилки (RMSE): {rmse:.4f}")
        print(f"Середня абсолютна помилка (MAE): {mae:.4f}")
        print(f"Коефіцієнт детермінації (R²): {r2:.4f}")
        
        # Візуалізація результатів
        print("\n--- Візуалізація результатів ---")
        
        # Візуалізація прогнозованих значень у порівнянні з фактичними
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel('Фактичні значення')
        plt.ylabel('Прогнозовані значення')
        plt.title('Порівняння фактичних та прогнозованих значень')
        plt.savefig(os.path.join(plots_dir, 'prediction_vs_actual.png'))
        plt.close()
        print(f"Графік порівняння фактичних та прогнозованих значень збережено як '{os.path.join(plots_dir, 'prediction_vs_actual.png')}'")
        
        # Візуалізація залишків
        residuals = y_test - y_pred
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), colors='r', linestyles='--')
        plt.xlabel('Прогнозовані значення')
        plt.ylabel('Залишки')
        plt.title('Графік залишків')
        plt.savefig(os.path.join(plots_dir, 'residuals.png'))
        plt.close()
        print(f"Графік залишків збережено як '{os.path.join(plots_dir, 'residuals.png')}'")
        
        # Гістограма залишків
        plt.figure(figsize=(10, 6))
        sns.histplot(residuals, kde=True)
        plt.xlabel('Залишки')
        plt.ylabel('Частота')
        plt.title('Розподіл залишків')
        plt.savefig(os.path.join(plots_dir, 'residuals_histogram.png'))
        plt.close()
        print(f"Гістограму залишків збережено як '{os.path.join(plots_dir, 'residuals_histogram.png')}'")
        
        # Візуалізація важливості ознак
        plt.figure(figsize=(12, 6))
        feature_importance = pd.DataFrame({'Ознака': feature_columns, 'Важливість': np.abs(model.coef_)})
        feature_importance = feature_importance.sort_values('Важливість', ascending=False)
        sns.barplot(x='Важливість', y='Ознака', data=feature_importance)
        plt.title('Важливість ознак')
        plt.savefig(os.path.join(plots_dir, 'feature_importance.png'))
        plt.close()
        print(f"Графік важливості ознак збережено як '{os.path.join(plots_dir, 'feature_importance.png')}'")
        
        print("\nМоделювання за допомогою лінійної регресії завершено!")
    else:
        print("\nНедостатньо числових стовпців для побудови моделі лінійної регресії.")
else:
    print("CSV файли не знайдено в завантаженому наборі даних")