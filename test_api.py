import requests
import json

ticker = "LKOH"
url = f'https://iss.moex.com/iss/securities/{ticker}.json'
params = {'iss.meta': 'off'}

response = requests.get(url, params=params)
data = response.json()

# Выведем структуру
print("Доступные секции:", list(data.keys()))
print("\n" + "="*50)

# Посмотрим секцию 'securities'
if 'securities' in data:
    print("\nКолонки securities:", data['securities']['columns'])
    print("Данные securities:", data['securities']['data'][0] if data['securities']['data'] else "Нет данных")

print("\n" + "="*50)

# Посмотрим секцию 'description'
if 'description' in data:
    print("\nКолонки description:", data['description']['columns'])
    print("Данные description:", data['description']['data'][:5] if data['description']['data'] else "Нет данных")

# Сохраним полный JSON в файл
with open('moex_response.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("\n\nПолный JSON сохранен в moex_response.json")