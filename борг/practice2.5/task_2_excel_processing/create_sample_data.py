import pandas as pd
import numpy as np

# Створюємо тестові дані
def create_sample_data():
    # Встановлюємо seed для відтворюваності результатів
    np.random.seed(42)
    
    # Кількість рядків
    n_rows = 100
    
    # Створюємо дані
    data = {
        'ID': np.arange(1, n_rows + 1),
        'Ім\'я': [f'Особа_{i}' for i in range(1, n_rows + 1)],
        'Вік': np.random.randint(18, 65, size=n_rows),
        'Зарплата': np.random.randint(30000, 100000, size=n_rows),
        'Досвід_роботи': np.random.randint(0, 30, size=n_rows),
        'Відділ': np.random.choice(['Маркетинг', 'Розробка', 'Продажі', 'HR', 'Фінанси'], size=n_rows)
    }
    
    # Створюємо DataFrame
    df = pd.DataFrame(data)
    
    # Зберігаємо у Excel-файл
    df.to_excel('data.xlsx', index=False)
    
    print(f"Створено тестовий файл 'data.xlsx' з {n_rows} рядками даних.")
    print("Структура даних:")
    print(df.info())
    print("\nПриклад даних:")
    print(df.head())

if __name__ == "__main__":
    create_sample_data()