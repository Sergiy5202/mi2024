import os
import sys

def main():
    print("Початок виконання програми планування операцій\n")
    
    # Крок 1: Створення тестових даних
    print("Крок 1: Створення тестових даних")
    from create_sample_data import create_sample_data
    create_sample_data()
    print("-" * 80)
    
    # Крок 2: Створення бази даних та імпорт даних
    print("\nКрок 2: Створення бази даних та імпорт даних")
    from create_database import main as create_db_main
    create_db_main()
    print("-" * 80)
    
    # Крок 3: Виконання SQL-запитів
    print("\nКрок 3: Виконання SQL-запитів")
    from execute_queries import execute_all_queries
    execute_all_queries()
    print("-" * 80)
    
    print("\nПрограма успішно завершила роботу!")
    print("Результати запитів збережено у директорії 'query_results'")

if __name__ == "__main__":
    main()