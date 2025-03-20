import pandas as pd
import os

def process_excel_file(input_file, output_file, filter_condition=None):
    """
    Функція для обробки Excel-файлу з використанням pandas
    
    Args:
        input_file (str): Шлях до вхідного Excel-файлу
        output_file (str): Шлях до вихідного Excel-файлу
        filter_condition (callable, optional): Функція фільтрації даних
    
    Returns:
        bool: True, якщо обробка пройшла успішно, False - в іншому випадку
    """
    try:
        # Перевіряємо, чи існує вхідний файл
        if not os.path.exists(input_file):
            print(f"Помилка: Файл {input_file} не знайдено.")
            return False
        
        # Читаємо Excel-файл
        print(f"Читаємо дані з файлу {input_file}...")
        df = pd.read_excel(input_file)
        
        # Виводимо інформацію про початкові дані
        print(f"Завантажено {len(df)} рядків даних.")
        print("Структура даних:")
        print(df.info())
        
        # Застосовуємо фільтрацію, якщо вказано умову
        if filter_condition is not None:
            filtered_df = df[filter_condition(df)]
            print(f"Після фільтрації залишилось {len(filtered_df)} рядків.")
        else:
            # Якщо умова не вказана, застосовуємо фільтрацію за замовчуванням
            # Наприклад, фільтруємо числові стовпці за значеннями більше середнього
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                # Вибираємо перший числовий стовпець для демонстрації
                col = numeric_cols[0]
                threshold = df[col].mean()
                filtered_df = df[df[col] > threshold]
                print(f"Застосовано фільтр: {col} > {threshold:.2f}")
                print(f"Після фільтрації залишилось {len(filtered_df)} рядків.")
            else:
                # Якщо немає числових стовпців, просто копіюємо дані
                filtered_df = df.copy()
                print("Не знайдено числових стовпців для фільтрації. Дані скопійовано без змін.")
        
        # Зберігаємо відфільтровані дані у новий файл
        filtered_df.to_excel(output_file, index=False)
        print(f"Відфільтровані дані збережено у файл {output_file}")
        
        return True
    
    except Exception as e:
        print(f"Помилка при обробці Excel-файлу: {e}")
        return False

def main():
    # Шляхи до файлів
    input_file = "data.xlsx"
    output_file = "filtered_data.xlsx"
    
    print("Початок обробки Excel-файлу...")
    
    # Виклик функції обробки з фільтром за замовчуванням
    success = process_excel_file(input_file, output_file)
    
    if success:
        print("Обробка завершена успішно!")
    else:
        print("Під час обробки виникли помилки.")

if __name__ == "__main__":
    main()