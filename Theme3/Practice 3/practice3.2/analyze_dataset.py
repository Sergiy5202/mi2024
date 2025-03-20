import os
import pandas as pd
import sys
import subprocess

# Функція для встановлення пакетів
def install_package(package):
    print(f"Встановлення {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Пакет {package} успішно встановлено")
    except Exception as e:
        print(f"Помилка при встановленні пакету {package}: {e}")
        raise

# Перевірка та встановлення необхідних бібліотек
required_packages = ["matplotlib", "seaborn"]
for package in required_packages:
    try:
        __import__(package)
        print(f"Бібліотека {package} вже встановлена")
    except ImportError:
        print(f"Бібліотека {package} не знайдена. Встановлюємо...")
        install_package(package)

# Імпортуємо бібліотеки для візуалізації після перевірки
import matplotlib.pyplot as plt
import seaborn as sns

# Спочатку запустимо скрипт для завантаження даних, якщо вони ще не завантажені
print("Перевірка наявності набору даних...")

# Функція для отримання шляху до CSV-файлу з набору даних
def get_csv_file_path():
    # Імпортуємо kagglehub для отримання шляху до завантаженого набору даних
    try:
        import kagglehub
    except ImportError:
        print("Бібліотека kagglehub не встановлена. Спочатку запустіть download_dataset.py")
        sys.exit(1)
    
    # Отримуємо шлях до завантаженого набору даних
    dataset_path = kagglehub.dataset_download("adilshamim8/personalized-learning-and-adaptive-education-dataset")
    
    # Шукаємо CSV-файли в директорії з набором даних
    csv_files = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    if not csv_files:
        print("CSV-файли не знайдені в завантаженому наборі даних")
        sys.exit(1)
    
    # Якщо знайдено кілька CSV-файлів, виводимо список і даємо користувачу вибрати
    if len(csv_files) > 1:
        print("\nЗнайдено кілька CSV-файлів:")
        for i, file_path in enumerate(csv_files):
            print(f"{i+1}. {os.path.basename(file_path)}")
        
        try:
            choice = int(input("\nВведіть номер файлу для аналізу: "))
            if 1 <= choice <= len(csv_files):
                return csv_files[choice-1]
            else:
                print("Невірний вибір. Використовуємо перший файл.")
                return csv_files[0]
        except ValueError:
            print("Невірний ввід. Використовуємо перший файл.")
            return csv_files[0]
    else:
        # Якщо знайдено лише один CSV-файл, повертаємо його шлях
        return csv_files[0]

# Отримуємо шлях до CSV-файлу
csv_file_path = get_csv_file_path()
print(f"\nВикористовуємо файл: {csv_file_path}")

# Завантаження даних у pandas DataFrame
try:
    print("\nЗавантаження даних у pandas DataFrame...")
    df = pd.read_csv(csv_file_path)
    
    # Виведення перших рядків набору даних
    print("\nПерші 5 рядків набору даних:")
    print(df.head())
    
    # Виведення інформації про набір даних
    print("\nІнформація про набір даних:")
    print(df.info())
    
    # Додатковий аналіз даних
    print("\nСтатистичний опис числових даних:")
    print(df.describe())
    
    # Розширена описова статистика
    print("\n--- Розширена описова статистика ---")
    
    # Статистика для категоріальних змінних
    print("\nСтатистика для категоріальних змінних:")
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        print(f"\nСтатистика для стовпця '{col}':")
        print(f"Кількість унікальних значень: {df[col].nunique()}")
        print(f"Найчастіше значення: {df[col].mode().values[0] if not df[col].mode().empty else 'Немає'}")
        print(f"Частота найчастішого значення: {df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0}")
        print("Топ-5 значень:")
        print(df[col].value_counts().head())
    
    # Кореляційна матриця для числових змінних
    print("\nКореляційна матриця для числових змінних:")
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        correlation_matrix = numeric_df.corr()
        print(correlation_matrix)
        
        # Знаходження найбільш корельованих пар змінних
        print("\nНайбільш корельовані пари змінних:")
        corr_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) > 0.5:  # Поріг кореляції
                    corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], correlation_matrix.iloc[i, j]))
        
        # Сортування за абсолютним значенням кореляції
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        # Виведення топ-10 корельованих пар
        for var1, var2, corr in corr_pairs[:10]:
            print(f"{var1} — {var2}: {corr:.3f}")
    else:
        print("Немає числових змінних для обчислення кореляції")
    
    # Створення візуалізацій
    print("\n--- Створення візуалізацій ---")
    
    # Створення директорії для збереження графіків, якщо вона не існує
    plots_dir = os.path.join(os.path.dirname(csv_file_path), "plots")
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        print(f"Створено директорію для графіків: {plots_dir}")
    
    # Гістограми для числових змінних
    print("\nСтворення гістограм для числових змінних...")
    for i, col in enumerate(numeric_df.columns[:5]):  # Обмеження до перших 5 числових стовпців
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=col, kde=True)
        plt.title(f'Розподіл значень для {col}')
        plt.xlabel(col)
        plt.ylabel('Частота')
        plot_path = os.path.join(plots_dir, f"{col}_histogram.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"  - Збережено гістограму для '{col}' у {plot_path}")
    
    # Boxplot для числових змінних
    print("\nСтворення boxplot для числових змінних...")
    if len(numeric_df.columns) > 0:
        plt.figure(figsize=(12, 8))
        sns.boxplot(data=numeric_df.iloc[:, :5])  # Обмеження до перших 5 числових стовпців
        plt.title('Boxplot для числових змінних')
        plt.xticks(rotation=45)
        plot_path = os.path.join(plots_dir, "numeric_boxplot.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"  - Збережено boxplot у {plot_path}")
        
        # Додаткові boxplot для окремих числових змінних
        print("\nСтворення окремих boxplot для числових змінних...")
        for i, col in enumerate(numeric_df.columns[:3]):  # Обмеження до перших 3 числових стовпців
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=df[col])
            plt.title(f'Boxplot для {col}')
            plt.xlabel(col)
            plot_path = os.path.join(plots_dir, f"{col}_boxplot.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"  - Збережено окремий boxplot для '{col}' у {plot_path}")
    
    # Діаграми розсіювання для пар числових змінних
    print("\nСтворення діаграм розсіювання для пар числових змінних...")
    if len(numeric_df.columns) >= 2:
        # Створюємо діаграми розсіювання для найбільш корельованих пар змінних
        for i, (var1, var2, corr) in enumerate(corr_pairs[:3]):  # Обмеження до перших 3 корельованих пар
            plt.figure(figsize=(10, 8))
            sns.scatterplot(x=df[var1], y=df[var2])
            plt.title(f'Діаграма розсіювання: {var1} vs {var2} (кореляція: {corr:.3f})')
            plt.xlabel(var1)
            plt.ylabel(var2)
            plot_path = os.path.join(plots_dir, f"scatter_{var1}_vs_{var2}.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"  - Збережено діаграму розсіювання для '{var1}' vs '{var2}' у {plot_path}")
        
        # Якщо немає корельованих пар, створюємо діаграми для перших пар змінних
        if len(corr_pairs) == 0:
            cols = numeric_df.columns[:3]  # Обмеження до перших 3 числових стовпців
            for i in range(len(cols)):
                for j in range(i+1, len(cols)):
                    var1, var2 = cols[i], cols[j]
                    plt.figure(figsize=(10, 8))
                    sns.scatterplot(x=df[var1], y=df[var2])
                    plt.title(f'Діаграма розсіювання: {var1} vs {var2}')
                    plt.xlabel(var1)
                    plt.ylabel(var2)
                    plot_path = os.path.join(plots_dir, f"scatter_{var1}_vs_{var2}.png")
                    plt.savefig(plot_path)
                    plt.close()
                    print(f"  - Збережено діаграму розсіювання для '{var1}' vs '{var2}' у {plot_path}")
    
    # Теплова карта кореляції
    print("\nСтворення теплової карти кореляції...")
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        # Створення та збереження теплової карти
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Теплова карта кореляції')
        plot_path = os.path.join(plots_dir, "correlation_heatmap.png")
        plt.savefig(plot_path)
        print(f"  - Збережено теплову карту кореляції у {plot_path}")
        
        # Створення окремої теплової карти для відображення
        print("\nВідображення інтерактивної теплової карти кореляції...")
        plt.figure(figsize=(14, 12))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Кореляційна матриця')
        plt.show()
        plt.close()
    
    # Кругові діаграми для категоріальних змінних
    print("\nСтворення кругових діаграм для категоріальних змінних...")
    for i, col in enumerate(categorical_columns[:3]):  # Обмеження до перших 3 категоріальних стовпців
        if df[col].nunique() < 10:  # Обмеження для змінних з невеликою кількістю категорій
            plt.figure(figsize=(10, 8))
            df[col].value_counts().plot.pie(autopct='%1.1f%%', shadow=True)
            plt.title(f'Розподіл категорій для {col}')
            plt.ylabel('')
            plot_path = os.path.join(plots_dir, f"{col}_pie.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"  - Збережено кругову діаграму для '{col}' у {plot_path}")
    
    print("\n--- Візуалізація завершена ---")
    print(f"Усі графіки збережено у директорії: {plots_dir}")
    
    # Перевірка наявності пропущених значень
    print("\nКількість пропущених значень у кожному стовпці:")
    print(df.isnull().sum())
    
    # Обробка даних
    print("\n--- Початок обробки даних ---")
    
    # Збереження початкової кількості рядків та стовпців
    initial_rows = df.shape[0]
    initial_cols = df.shape[1]
    
    # Заповнення пропущених значень середнім для числових стовпців
    print("\nЗаповнення пропущених значень середнім для числових стовпців...")
    numeric_columns = df.select_dtypes(include=['number']).columns
    for col in numeric_columns:
        if df[col].isnull().sum() > 0:
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            print(f"  - Заповнено пропущені значення у стовпці '{col}' значенням {mean_value:.2f}")
    
    # Видалення дублікатів
    print("\nВидалення дублікатів...")
    duplicates_count = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    print(f"  - Видалено {duplicates_count} дублікатів")
    
    # Перетворення категоріальних змінних на числові
    print("\nПеретворення категоріальних змінних на числові...")
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        print(f"  - Перетворення стовпця '{col}'")
        df[col] = df[col].astype('category').cat.codes
    
    # Виведення інформації про результати обробки
    print("\nРезультати обробки даних:")
    print(f"  - Початкова кількість рядків: {initial_rows}")
    print(f"  - Кінцева кількість рядків: {df.shape[0]}")
    print(f"  - Видалено рядків: {initial_rows - df.shape[0]}")
    
    # Перевірка на пропущені значення після обробки
    missing_after = df.isnull().sum().sum()
    print(f"  - Кількість пропущених значень після обробки: {missing_after}")
    
    print("\n--- Обробка даних завершена ---")
    
    # Виведення перших рядків обробленого набору даних
    print("\nПерші 5 рядків обробленого набору даних:")
    print(df.head())
    
    # Виведення унікальних значень для категоріальних стовпців (перші 5 стовпців)
    print("\nУнікальні значення для категоріальних стовпців (перші 5):")
    categorical_columns = df.select_dtypes(include=['object']).columns[:5]
    for col in categorical_columns:
        print(f"\n{col}:")
        print(df[col].value_counts().head())
    
    print("\nАналіз даних завершено успішно!")
    
except Exception as e:
    print(f"\nПомилка при аналізі даних: {e}")
    import traceback
    traceback.print_exc()