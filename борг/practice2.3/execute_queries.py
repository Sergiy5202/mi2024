import sqlite3
import pandas as pd
from create_database import execute_query
import os

# Перевірка наявності директорії для результатів запитів
if not os.path.exists('query_results'):
    os.makedirs('query_results')

# Функція для виконання всіх запитів
def execute_all_queries():
    print("Виконання всіх SQL-запитів...")
    for query_info in queries:
        print(f"\nВиконання запиту: {query_info['description']}")
        result = execute_query(query_info['query'], query_info['name'])
        if result is not None:
            print(f"Результат запиту '{query_info['name']}':\n")
            print(result.head())
            print(f"\nЗбережено у файли: query_results/{query_info['name']}.csv та query_results/{query_info['name']}.xlsx")
        print("-" * 80)

# Список SQL-запитів з описами
queries = [
    # 1. Базова вибірка всіх операцій
    {
        "name": "all_operations",
        "description": "Список всіх операцій",
        "query": "SELECT * FROM Operations"
    },
    
    # 2. Базова вибірка всього персоналу
    {
        "name": "all_staff",
        "description": "Список всього персоналу",
        "query": "SELECT * FROM Operations_Staff"
    },
    
    # 3. Вибірка активних операцій (без дати завершення)
    {
        "name": "active_operations",
        "description": "Список активних операцій (без дати завершення)",
        "query": "SELECT * FROM Operations WHERE Operation_End_Date IS NULL"
    },
    
    # 4. Вибірка завершених операцій (з датою завершення)
    {
        "name": "completed_operations",
        "description": "Список завершених операцій (з датою завершення)",
        "query": "SELECT * FROM Operations WHERE Operation_End_Date IS NOT NULL"
    },
    
    # 5. Простий JOIN - персонал з інформацією про операції
    {
        "name": "staff_with_operations",
        "description": "Персонал з інформацією про операції",
        "query": """SELECT s.ID, s.Name, s.Role, o.Operation_Name, o.Commander, s.Date_Assigned 
                 FROM Operations_Staff s 
                 JOIN Operations o ON s.Operation_ID = o.Operation_ID"""
    },
    
    # 6. Кількість персоналу в кожній операції (GROUP BY)
    {
        "name": "staff_count_per_operation",
        "description": "Кількість персоналу в кожній операції",
        "query": """SELECT o.Operation_ID, o.Operation_Name, COUNT(s.ID) as Staff_Count 
                 FROM Operations o 
                 LEFT JOIN Operations_Staff s ON o.Operation_ID = s.Operation_ID 
                 GROUP BY o.Operation_ID, o.Operation_Name"""
    },
    
    # 7. Операції з більше ніж 3 співробітниками (HAVING)
    {
        "name": "operations_with_more_than_3_staff",
        "description": "Операції з більше ніж 3 співробітниками",
        "query": """SELECT o.Operation_ID, o.Operation_Name, COUNT(s.ID) as Staff_Count 
                 FROM Operations o 
                 JOIN Operations_Staff s ON o.Operation_ID = s.Operation_ID 
                 GROUP BY o.Operation_ID, o.Operation_Name 
                 HAVING COUNT(s.ID) > 3"""
    },
    
    # 8. Операції з менше ніж 3 співробітниками (HAVING)
    {
        "name": "operations_with_less_than_3_staff",
        "description": "Операції з менше ніж 3 співробітниками",
        "query": """SELECT o.Operation_ID, o.Operation_Name, COUNT(s.ID) as Staff_Count 
                 FROM Operations o 
                 JOIN Operations_Staff s ON o.Operation_ID = s.Operation_ID 
                 GROUP BY o.Operation_ID, o.Operation_Name 
                 HAVING COUNT(s.ID) < 3"""
    },
    
    # 9. Кількість різних ролей в кожній операції
    {
        "name": "role_count_per_operation",
        "description": "Кількість різних ролей в кожній операції",
        "query": """SELECT o.Operation_ID, o.Operation_Name, COUNT(DISTINCT s.Role) as Unique_Roles 
                 FROM Operations o 
                 JOIN Operations_Staff s ON o.Operation_ID = s.Operation_ID 
                 GROUP BY o.Operation_ID, o.Operation_Name"""
    },
    
    # 10. Список персоналу, призначеного на активні операції
    {
        "name": "staff_in_active_operations",
        "description": "Персонал, призначений на активні операції",
        "query": """SELECT s.ID, s.Name, s.Role, o.Operation_Name, s.Date_Assigned 
                 FROM Operations_Staff s 
                 JOIN Operations o ON s.Operation_ID = o.Operation_ID 
                 WHERE o.Operation_End_Date IS NULL"""
    },
    
    # 11. Список персоналу, призначеного на завершені операції
    {
        "name": "staff_in_completed_operations",
        "description": "Персонал, призначений на завершені операції",
        "query": """SELECT s.ID, s.Name, s.Role, o.Operation_Name, s.Date_Assigned, o.Operation_End_Date 
                 FROM Operations_Staff s 
                 JOIN Operations o ON s.Operation_ID = o.Operation_ID 
                 WHERE o.Operation_End_Date IS NOT NULL"""
    },
    
    # 12. Тривалість кожної завершеної операції в днях
    {
        "name": "operation_duration",
        "description": "Тривалість кожної завершеної операції в днях",
        "query": """SELECT Operation_ID, Operation_Name, 
                 julianday(Operation_End_Date) - julianday(Operation_Start_Date) as Duration_Days 
                 FROM Operations 
                 WHERE Operation_End_Date IS NOT NULL 
                 ORDER BY Duration_Days DESC"""
    },
    
    # 13. Операції, які тривали більше 30 днів
    {
        "name": "long_operations",
        "description": "Операції, які тривали більше 30 днів",
        "query": """SELECT Operation_ID, Operation_Name, 
                 julianday(Operation_End_Date) - julianday(Operation_Start_Date) as Duration_Days 
                 FROM Operations 
                 WHERE Operation_End_Date IS NOT NULL 
                 AND (julianday(Operation_End_Date) - julianday(Operation_Start_Date)) > 30 
                 ORDER BY Duration_Days DESC"""
    },
    
    # 14. Кількість операцій під командуванням кожного командира
    {
        "name": "operations_per_commander",
        "description": "Кількість операцій під командуванням кожного командира",
        "query": """SELECT Commander, COUNT(*) as Operation_Count 
                 FROM Operations 
                 GROUP BY Commander 
                 ORDER BY Operation_Count DESC"""
    },
    
    # 15. Кількість персоналу за ролями
    {
        "name": "staff_count_by_role",
        "description": "Кількість персоналу за ролями",
        "query": """SELECT Role, COUNT(*) as Staff_Count 
                 FROM Operations_Staff 
                 GROUP BY Role 
                 ORDER BY Staff_Count DESC"""
    },
    
    # 16. Персонал, який був призначений на операції після певної дати
    {
        "name": "staff_assigned_after_date",
        "description": "Персонал, призначений на операції після 2023-01-01",
        "query": """SELECT s.ID, s.Name, s.Role, o.Operation_Name, s.Date_Assigned 
                 FROM Operations_Staff s 
                 JOIN Operations o ON s.Operation_ID = o.Operation_ID 
                 WHERE s.Date_Assigned > '2023-01-01'
                 ORDER BY s.Date_Assigned"""
    },
    
    # 17. Операції, які почалися в певному місяці
    {
        "name": "operations_started_in_month",
        "description": "Операції, які почалися в січні 2023",
        "query": """SELECT * FROM Operations 
                 WHERE Operation_Start_Date LIKE '2023-01-%'
                 ORDER BY Operation_Start_Date"""
    },
    
    # 18. Персонал, який не призначений на жодну операцію (LEFT JOIN + IS NULL)
    {
        "name": "unassigned_staff",
        "description": "Персонал, який не призначений на жодну операцію",
        "query": """SELECT s.ID, s.Name, s.Role, s.Date_Assigned 
                 FROM Operations_Staff s 
                 LEFT JOIN Operations o ON s.Operation_ID = o.Operation_ID 
                 WHERE o.Operation_ID IS NULL"""
    },
    
    # 19. Операції без призначеного персоналу (LEFT JOIN + IS NULL)
    {
        "name": "operations_without_staff",
        "description": "Операції без призначеного персоналу",
        "query": """SELECT o.Operation_ID, o.Operation_Name, o.Commander, o.Operation_Start_Date 
                 FROM Operations o 
                 LEFT JOIN Operations_Staff s ON o.Operation_ID = s.Operation_ID 
                 WHERE s.ID IS NULL"""
    },
    
    # 20. Командири, які керують більше ніж однією активною операцією
    {
        "name": "commanders_with_multiple_active_operations",
        "description": "Командири, які керують більше ніж однією активною операцією",
        "query": """SELECT Commander, COUNT(*) as Active_Operations 
                 FROM Operations 
                 WHERE Operation_End_Date IS NULL 
                 GROUP BY Commander 
                 HAVING COUNT(*) > 1
                 ORDER BY Active_Operations DESC"""
    }
]

# Головна функція для запуску всіх запитів
def main():
    execute_all_queries()

if __name__ == "__main__":
    main()