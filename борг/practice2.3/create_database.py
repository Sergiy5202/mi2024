import sqlite3
import pandas as pd
import os
from datetime import datetime

# Створення директорії для результатів запитів
if not os.path.exists('query_results'):
    os.makedirs('query_results')

# Підключення до бази даних (створення, якщо не існує)
def create_database():
    conn = sqlite3.connect('operations_planning.db')
    cursor = conn.cursor()
    
    # Створення таблиці Operations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Operations (
        Operation_ID INTEGER PRIMARY KEY,
        Operation_Name TEXT NOT NULL,
        Commander TEXT NOT NULL,
        Operation_Start_Date TEXT NOT NULL,
        Operation_End_Date TEXT
    )
    ''')
    
    # Створення таблиці Operations_Staff
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Operations_Staff (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Role TEXT NOT NULL,
        Operation_ID INTEGER,
        Date_Assigned TEXT NOT NULL,
        FOREIGN KEY (Operation_ID) REFERENCES Operations(Operation_ID)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База даних та таблиці успішно створені.")

# Імпорт даних з Excel-файлу
def import_data_from_excel(excel_file):
    try:
        # Читання даних з Excel-файлу
        operations_df = pd.read_excel(excel_file, sheet_name='Operations')
        staff_df = pd.read_excel(excel_file, sheet_name='Operations_Staff')
        
        # Підключення до бази даних
        conn = sqlite3.connect('operations_planning.db')
        
        # Імпорт даних в таблиці
        operations_df.to_sql('Operations', conn, if_exists='replace', index=False)
        staff_df.to_sql('Operations_Staff', conn, if_exists='replace', index=False)
        
        conn.close()
        print("Дані успішно імпортовані з Excel-файлу.")
    except Exception as e:
        print(f"Помилка при імпорті даних: {e}")

# Виконання SQL-запиту та збереження результату у файл
def execute_query(query, query_name):
    try:
        conn = sqlite3.connect('operations_planning.db')
        result = pd.read_sql_query(query, conn)
        
        # Збереження результату у CSV-файл
        result.to_csv(f'query_results/{query_name}.csv', index=False, encoding='utf-8')
        
        # Збереження результату у Excel-файл
        result.to_excel(f'query_results/{query_name}.xlsx', index=False)
        
        conn.close()
        print(f"Запит '{query_name}' успішно виконано та результати збережено.")
        return result
    except Exception as e:
        print(f"Помилка при виконанні запиту '{query_name}': {e}")
        return None

# Головна функція
def main():
    create_database()
    
    # Перевірка наявності Excel-файлу
    if os.path.exists('operations_data.xlsx'):
        import_data_from_excel('operations_data.xlsx')
    else:
        print("Excel-файл 'operations_data.xlsx' не знайдено. Спочатку створіть файл з даними.")

if __name__ == "__main__":
    main()
    
    

    