import os
import sys
import subprocess

# Перевірка та встановлення необхідних бібліотек
def install_package(package):
    print(f"Встановлення {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Пакет {package} успішно встановлено")
    except Exception as e:
        print(f"Помилка при встановленні пакету {package}: {e}")
        raise

# Перевірка наявності kagglehub
print("Перевірка наявності kagglehub...")
try:
    import kagglehub
    print("Бібліотека kagglehub вже встановлена")
except ImportError:
    print("Бібліотека kagglehub не знайдена. Встановлюємо...")
    install_package("kagglehub")
    try:
        import kagglehub
        print("Бібліотека kagglehub успішно імпортована після встановлення")
    except ImportError as e:
        print(f"Не вдалося імпортувати kagglehub після встановлення: {e}")
        sys.exit(1)

# Завантаження набору даних
print("Завантаження набору даних про персоналізоване навчання та адаптивну освіту...")
try:
    print("Початок завантаження набору даних...")
    path = kagglehub.dataset_download("adilshamim8/personalized-learning-and-adaptive-education-dataset")
    print(f"\nШлях до файлів набору даних: {path}")
    
    # Перевірка, чи існує шлях
    if os.path.exists(path):
        print(f"Шлях {path} існує")
    else:
        print(f"Шлях {path} не існує!")
    
    # Виведення списку завантажених файлів
    print("\nЗавантажені файли:")
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            print(f"Директорія: {root}")
            print(f"Піддиректорії: {dirs}")
            print(f"Файли: {files}")
            for file in files:
                file_path = os.path.join(root, file)
                print(f" - {file_path}")
    else:
        print("Не вдалося знайти директорію з завантаженими файлами")
            
    print("\nЗавантаження завершено успішно!")
    
    # Додаткова інформація про використання даних
    print("\nДля завантаження даних у pandas DataFrame використовуйте:")
    print("import pandas as pd")
    print("df = pd.read_csv('шлях_до_csv_файлу')")
    
except Exception as e:
    print(f"Помилка при завантаженні набору даних: {e}")
    print(f"Тип помилки: {type(e).__name__}")
    import traceback
    print("Деталі помилки:")
    traceback.print_exc()
    
    print("\nМожливі причини помилки:")
    print(" - Відсутнє підключення до інтернету")
    print(" - Необхідна автентифікація в Kaggle (використовуйте kaggle.json)")
    print(" - Набір даних недоступний або змінив назву")
    
    print("\nДля автентифікації в Kaggle:")
    print("1. Зареєструйтесь на kaggle.com")
    print("2. Перейдіть в налаштування облікового запису")
    print("3. Прокрутіть до розділу API і натисніть 'Create New API Token'")
    print("4. Збережіть файл kaggle.json в ~/.kaggle/ (Linux/Mac) або %USERPROFILE%\.kaggle\ (Windows)")