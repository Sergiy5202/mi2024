#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import datetime
import os

def create_xml():
    """
    Створює XML-файл з даними про підрозділи
    """
    # Створюємо кореневий елемент
    root = ET.Element("units")
    
    # Додаємо атрибут дати створення
    root.set("created", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Додаємо підрозділи
    units = [
        {"name": "Маркетинг", "count": 15, "status": "active"},
        {"name": "Розробка", "count": 25, "status": "active"},
        {"name": "Продажі", "count": 10, "status": "active"},
        {"name": "HR", "count": 5, "status": "active"},
        {"name": "Фінанси", "count": 8, "status": "active"},
        {"name": "Підтримка", "count": 12, "status": "inactive"}
    ]
    
    # Створюємо елементи для кожного підрозділу
    for unit_data in units:
        unit = ET.SubElement(root, "unit")
        
        # Додаємо елементи з даними про підрозділ
        name = ET.SubElement(unit, "name")
        name.text = unit_data["name"]
        
        count = ET.SubElement(unit, "count")
        count.text = str(unit_data["count"])
        
        status = ET.SubElement(unit, "status")
        status.text = unit_data["status"]
    
    # Створюємо дерево XML
    tree = ET.ElementTree(root)
    
    # Форматуємо XML з відступами для кращої читабельності
    ET.indent(tree, space="  ")
    
    # Зберігаємо XML у файл
    output_file = "unit_data.xml"
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    
    print(f"XML-файл '{output_file}' успішно створено.")
    return output_file

def main():
    """
    Головна функція програми
    """
    print("Створення XML-файлу з даними про підрозділи...")
    file_path = create_xml()
    
    # Виводимо абсолютний шлях до створеного файлу
    abs_path = os.path.abspath(file_path)
    print(f"Файл створено за шляхом: {abs_path}")

if __name__ == "__main__":
    main()