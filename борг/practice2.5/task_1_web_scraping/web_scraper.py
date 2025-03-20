import requests
import csv
from bs4 import BeautifulSoup
import os

def scrape_news_titles(url):
    """
    Функція для збору заголовків новин з вказаного URL
    
    Args:
        url (str): URL-адреса вебсайту для скрапінгу
        
    Returns:
        list: Список заголовків новин
    """
    try:
        # Відправляємо GET-запит до вебсайту
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Перевіряємо на помилки HTTP
        
        # Створюємо об'єкт BeautifulSoup для парсингу HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Знаходимо всі заголовки новин (приклад селектора - може потребувати зміни)
        # Тут використовуємо загальний селектор для заголовків
        news_titles = []
        
        # Шукаємо заголовки в різних можливих HTML-елементах
        headlines = soup.find_all(['h1', 'h2', 'h3'], class_=lambda c: c and ('title' in c.lower() or 'headline' in c.lower()))
        if not headlines:
            headlines = soup.find_all(['h1', 'h2', 'h3'])
        
        for headline in headlines:
            title = headline.text.strip()
            if title:  # Перевіряємо, що заголовок не порожній
                news_titles.append(title)
        
        return news_titles
    
    except Exception as e:
        print(f"Помилка при скрапінгу: {e}")
        return []

def save_to_csv(titles, filename):
    """
    Функція для збереження заголовків у CSV-файл
    
    Args:
        titles (list): Список заголовків новин
        filename (str): Ім'я файлу для збереження
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Заголовок новини'])  # Заголовок стовпця
            for title in titles:
                writer.writerow([title])
        print(f"Дані успішно збережено у файл {filename}")
    except Exception as e:
        print(f"Помилка при збереженні у CSV: {e}")

def main():
    # URL вебсайту для скрапінгу (приклад - можна змінити на потрібний)
    url = "https://www.bbc.com/news"
    
    print(f"Починаємо збір заголовків з {url}...")
    news_titles = scrape_news_titles(url)
    
    if news_titles:
        print(f"Зібрано {len(news_titles)} заголовків.")
        
        # Шлях до CSV-файлу
        csv_filename = "news_titles.csv"
        save_to_csv(news_titles, csv_filename)
    else:
        print("Не вдалося зібрати заголовки новин.")

if __name__ == "__main__":
    main()