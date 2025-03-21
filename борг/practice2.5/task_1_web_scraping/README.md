# Web Scraping Task

## Опис
Цей проект містить скрипт для збору заголовків новин з вебсайту та збереження їх у CSV-файл.

## Функціональність
Скрипт `web_scraper.py` виконує наступні дії:
1. Підключається до вказаного вебсайту (за замовчуванням BBC News)
2. Збирає заголовки новин з HTML-сторінки
3. Зберігає зібрані заголовки у файл `news_titles.csv`

## Вимоги
Для роботи скрипта потрібні наступні бібліотеки Python:
- requests
- beautifulsoup4
- csv (стандартна бібліотека)

Ви можете встановити необхідні бібліотеки за допомогою команди:
```
pip install requests beautifulsoup4
```

## Як запустити
1. Переконайтеся, що всі необхідні бібліотеки встановлені
2. Запустіть скрипт командою:
```
python web_scraper.py
```
3. Після успішного виконання, результати будуть збережені у файлі `news_titles.csv`

## Налаштування
Якщо ви хочете змінити вебсайт для скрапінгу, відредагуйте змінну `url` у функції `main()` скрипта `web_scraper.py`.