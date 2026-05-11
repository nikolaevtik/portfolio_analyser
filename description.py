import requests
import json

url1 = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities/columns.json'
url2 = 'https://iss.moex.com/iss/engines.json'

def fetch_moex_data(url, params=None):
    """Универсальная функция для любого запроса к MOEX"""
    if params is None:
        params = {'iss.meta': 'off'}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Выводим все доступные секции в ответе
    for section_name, section_data in data.items():
        if 'data' in section_data and section_data['data']:
            print(f"\n=== Секция: {section_name} ===")
            columns = section_data['columns']
            print("Колонки:", columns)
            print("Первая строка данных:", section_data['data'][0])
    
    return data

# Выбор запроса (один input)
choice = input("Выбери запрос (1 или 2): ")

if choice == '1':
    data = fetch_moex_data(url1, {'lang': 'ru'})
    # Для url1 данные в секции 'securities'
    print("\n=== ПОЛЯ ТАБЛИЦЫ SECURITIES ===\n")
    for col in data['securities']['data']:
        print(f"{col[1]}: {col[3]}")
        
elif choice == '2':
    data = fetch_moex_data(url2, {'lang': 'ru'})
    # Для url2 данные в секции 'engines'
    if 'engines' in data:
        print("\n=== ДОСТУПНЫЕ ТОРГОВЫЕ СИСТЕМЫ ===\n")
        for engine in data['engines']['data']:
            # engine[0] - id, engine[1] - name
            print(f"{engine[0]}: {engine[1]}")
else:
    data = 'Нет данных'
    print("Неверный выбор")

# Сохраняем JSON (только если data не строка)
if isinstance(data, dict):
    with open('moex_description.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\nПолный JSON сохранен в moex_description.json")