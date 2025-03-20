# Імпортуємо необхідні бібліотеки
import os
import sys
import importlib.util

# Функція для перевірки наявності пакету
def is_package_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

# Перевірка наявності необхідних пакетів
required_packages = ['pandas', 'kagglehub', 'sklearn', 'matplotlib', 'seaborn']
missing_packages = [pkg for pkg in required_packages if not is_package_installed(pkg)]

# Якщо є відсутні пакети, виводимо інструкції та завершуємо роботу
if missing_packages:
    print("Помилка: Відсутні необхідні пакети:")
    for pkg in missing_packages:
        print(f"  - {pkg}")
    print("\nДля встановлення необхідних пакетів виконайте команду:")
    print("pip install -r requirements.txt")
    print("\nАбо встановіть кожен пакет окремо:")
    for pkg in missing_packages:
        print(f"pip install {pkg}")
    sys.exit(1)

# Імпортуємо необхідні бібліотеки після перевірки
import pandas as pd
import kagglehub
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Отримуємо шлях до набору даних (який вже завантажено)
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
    
    # Спробуємо перетворити стовпець 'Puntaje' у числовий формат
    try:
        if 'Puntaje' in df.columns:
            # Перевіряємо, чи стовпець є об'єктного типу (рядки)
            if df['Puntaje'].dtype == 'object':
                # Замінюємо коми на крапки та видаляємо нечислові символи
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
    
    # Нормалізація числових змінних
    print("\nНормалізація числових змінних...")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        scaler = MinMaxScaler()
        for col in numeric_columns:
            # Створюємо новий стовпець з нормалізованими значеннями
            df[f'{col}_normalized'] = scaler.fit_transform(df[[col]])
        print(f"Нормалізовано {len(numeric_columns)} числових стовпців")
    else:
        print("Числових стовпців для нормалізації не знайдено")
    
    # One-Hot Encoding для категоріальних змінних
    print("\nЗастосування One-Hot Encoding для категоріальних змінних...")
    # Знаходимо категоріальні стовпці, які ще не були закодовані
    categorical_columns_for_onehot = df.select_dtypes(include=['object']).columns
    if len(categorical_columns_for_onehot) > 0:
        # Застосовуємо One-Hot Encoding
        df_transformed = pd.get_dummies(df, columns=list(categorical_columns_for_onehot))
        print(f"Застосовано One-Hot Encoding до {len(categorical_columns_for_onehot)} категоріальних стовпців")
        # Оновлюємо наш DataFrame
        df = df_transformed
    else:
        print("Категоріальних стовпців для One-Hot Encoding не знайдено")
    
    # Виводимо перші рядки даних після обробки
    print("\nПерші 5 рядків даних після обробки:")
    print(df.head())
    
    # Додатково виводимо базову інформацію про набір даних
    print("\nРозмір набору даних після обробки:", df.shape)
    
    # Виводимо детальну інформацію про набір даних
    print("\nІнформація про набір даних після обробки:")
    print(df.info())
    
    # Поділ на навчальну та тестову вибірки
    from sklearn.model_selection import train_test_split
    
    print("\nПоділ на навчальну та тестову вибірки...")
    train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
    print(f"Розмір навчальної вибірки: {train_set.shape}")
    print(f"Розмір тестової вибірки: {test_set.shape}")
    
    # Обчислення кореляційної матриці
    print("\nОбчислення кореляційної матриці...")
    correlation_matrix = df.corr()
    print("\nКореляційна матриця:")
    print(correlation_matrix)
    
    # Виведення описової статистики
    print("\nОписова статистика:")
    print(df.describe())
    
    # Візуалізація даних
    print("\nСтворення візуалізацій даних...")
    
    # Вибираємо числові стовпці для візуалізації
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        # Створюємо директорію для збереження графіків, якщо вона не існує
        plots_dir = 'plots'
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        
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
        
        # Теплова карта кореляції
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Теплова карта кореляції')
        plt.savefig(os.path.join(plots_dir, 'correlation_heatmap.png'))
        plt.close()
        print(f"Теплову карту кореляції збережено як '{os.path.join(plots_dir, 'correlation_heatmap.png')}'")
    else:
        print("Числових стовпців для візуалізації не знайдено")
else:
    print("CSV файли не знайдено в завантаженому наборі даних")