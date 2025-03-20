import pandas as pd
import os
from datetime import datetime, timedelta

# Функція для створення тестових даних
def create_sample_data():
    # Створення даних для таблиці Operations
    operations_data = [
        {"Operation_ID": 1, "Operation_Name": "Операція Альфа", "Commander": "Іван Петренко", 
         "Operation_Start_Date": "2023-01-15", "Operation_End_Date": "2023-02-28"},
        {"Operation_ID": 2, "Operation_Name": "Операція Бета", "Commander": "Олена Коваленко", 
         "Operation_Start_Date": "2023-02-10", "Operation_End_Date": "2023-04-20"},
        {"Operation_ID": 3, "Operation_Name": "Операція Гамма", "Commander": "Петро Сидоренко", 
         "Operation_Start_Date": "2023-03-05", "Operation_End_Date": "2023-05-15"},
        {"Operation_ID": 4, "Operation_Name": "Операція Дельта", "Commander": "Марія Шевченко", 
         "Operation_Start_Date": "2023-01-20", "Operation_End_Date": None},
        {"Operation_ID": 5, "Operation_Name": "Операція Епсилон", "Commander": "Іван Петренко", 
         "Operation_Start_Date": "2023-04-10", "Operation_End_Date": None},
        {"Operation_ID": 6, "Operation_Name": "Операція Зета", "Commander": "Олена Коваленко", 
         "Operation_Start_Date": "2022-12-01", "Operation_End_Date": "2023-03-15"},
        {"Operation_ID": 7, "Operation_Name": "Операція Ета", "Commander": "Петро Сидоренко", 
         "Operation_Start_Date": "2023-05-01", "Operation_End_Date": None},
        {"Operation_ID": 8, "Operation_Name": "Операція Тета", "Commander": "Марія Шевченко", 
         "Operation_Start_Date": "2023-01-05", "Operation_End_Date": "2023-06-10"},
        {"Operation_ID": 9, "Operation_Name": "Операція Йота", "Commander": "Іван Петренко", 
         "Operation_Start_Date": "2023-06-15", "Operation_End_Date": None},
        {"Operation_ID": 10, "Operation_Name": "Операція Каппа", "Commander": "Олена Коваленко", 
         "Operation_Start_Date": "2023-07-01", "Operation_End_Date": None}
    ]
    
    # Створення даних для таблиці Operations_Staff
    staff_data = [
        {"ID": 1, "Name": "Андрій Мельник", "Role": "Аналітик", "Operation_ID": 1, "Date_Assigned": "2023-01-15"},
        {"ID": 2, "Name": "Ірина Ковальчук", "Role": "Оператор", "Operation_ID": 1, "Date_Assigned": "2023-01-16"},
        {"ID": 3, "Name": "Сергій Бондаренко", "Role": "Технік", "Operation_ID": 1, "Date_Assigned": "2023-01-17"},
        {"ID": 4, "Name": "Тетяна Лисенко", "Role": "Координатор", "Operation_ID": 1, "Date_Assigned": "2023-01-18"},
        {"ID": 5, "Name": "Василь Кравченко", "Role": "Аналітик", "Operation_ID": 2, "Date_Assigned": "2023-02-10"},
        {"ID": 6, "Name": "Наталія Шевчук", "Role": "Оператор", "Operation_ID": 2, "Date_Assigned": "2023-02-11"},
        {"ID": 7, "Name": "Олександр Мороз", "Role": "Технік", "Operation_ID": 3, "Date_Assigned": "2023-03-05"},
        {"ID": 8, "Name": "Юлія Ткаченко", "Role": "Координатор", "Operation_ID": 3, "Date_Assigned": "2023-03-06"},
        {"ID": 9, "Name": "Микола Іванченко", "Role": "Аналітик", "Operation_ID": 4, "Date_Assigned": "2023-01-20"},
        {"ID": 10, "Name": "Оксана Петренко", "Role": "Оператор", "Operation_ID": 4, "Date_Assigned": "2023-01-21"},
        {"ID": 11, "Name": "Дмитро Савченко", "Role": "Технік", "Operation_ID": 5, "Date_Assigned": "2023-04-10"},
        {"ID": 12, "Name": "Людмила Кузьменко", "Role": "Координатор", "Operation_ID": 5, "Date_Assigned": "2023-04-11"},
        {"ID": 13, "Name": "Віктор Романенко", "Role": "Аналітик", "Operation_ID": 6, "Date_Assigned": "2022-12-01"},
        {"ID": 14, "Name": "Катерина Левченко", "Role": "Оператор", "Operation_ID": 6, "Date_Assigned": "2022-12-02"},
        {"ID": 15, "Name": "Павло Захарченко", "Role": "Технік", "Operation_ID": 7, "Date_Assigned": "2023-05-01"},
        {"ID": 16, "Name": "Галина Даниленко", "Role": "Координатор", "Operation_ID": 8, "Date_Assigned": "2023-01-05"},
        {"ID": 17, "Name": "Роман Тимошенко", "Role": "Аналітик", "Operation_ID": 9, "Date_Assigned": "2023-06-15"},
        {"ID": 18, "Name": "Софія Кравчук", "Role": "Оператор", "Operation_ID": 10, "Date_Assigned": "2023-07-01"},
        {"ID": 19, "Name": "Ігор Лисенко", "Role": "Технік", "Operation_ID": None, "Date_Assigned": "2023-07-15"},
        {"ID": 20, "Name": "Анна Мельничук", "Role": "Координатор", "Operation_ID": None, "Date_Assigned": "2023-07-16"}
    ]
    
    # Створення DataFrame
    operations_df = pd.DataFrame(operations_data)
    staff_df = pd.DataFrame(staff_data)
    
    # Створення Excel-файлу з двома аркушами
    with pd.ExcelWriter('operations_data.xlsx') as writer:
        operations_df.to_excel(writer, sheet_name='Operations', index=False)
        staff_df.to_excel(writer, sheet_name='Operations_Staff', index=False)
    
    print("Excel-файл з тестовими даними успішно створено.")

if __name__ == "__main__":
    create_sample_data()