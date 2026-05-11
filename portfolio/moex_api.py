import pandas as pd
import requests

def get_stock_price(ticker):
    try:
        url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}.json"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['securities']['data'][0][3]
    except (IndexError, KeyError, requests.RequestException):
        return None  # цена недоступна
    



def search_ticker(query):
    url = f'https://iss.moex.com/iss/securities.json?q={query}'
    j = requests.get(url).json()
    data = [{k: r[i] for i, k in enumerate(j['securities']['columns'])} for r in j['securities']['data']]
    df = pd.DataFrame(data)
    
    # Оставляем дубликаты, но показываем только основные тикеры
    if 'secid' in df.columns:
        df = df.drop_duplicates(subset=['secid'])
    
    return df


def get_blue_chips():
    """Возвращает акции из индекса МосБиржи голубых фишек (MOEXBC)"""
    url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities.json'
    params = {
        'iss.meta': 'off',
        'limit': 100
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    securities = data['securities']['data']
    sec_columns = data['securities']['columns']
    
    secid_idx = sec_columns.index('SECID')
    name_idx = sec_columns.index('SHORTNAME')
    
    # Официальный список голубых фишек (проверен на март 2026)
    blue_chips_tickers = [
        'SBER', 'SBERP', 'LKOH', 'GAZP', 'ROSN', 'NVTK', 'GMKN', 'MGNT',
        'TATN', 'TATNP', 'MTSS', 'CHMF', 'NLMK', 'SNGS', 'SNGSP', 'MOEX',
        'VTBR', 'POLY', 'RUAL', 'PHOR', 'YNDX', 'OZON', 'TCSG', 'AFKS'
    ]
    
    stocks = []
    for sec in securities:
        ticker = sec[secid_idx]
        if ticker in blue_chips_tickers:
            stocks.append({
                'ticker': ticker,
                'name': sec[name_idx]
            })
    
    return stocks


def get_candles(ticker, interval=24, start_date=None):
    """
    Получает данные свечей для тикера.
    interval=24 - дневные свечи.
    """
    # Если дата не указана, берем данные за последние 30-40 дней с запасом
    if start_date is None:
        start_date = (pd.Timestamp.now() - pd.DateOffset(days=45)).strftime('%Y-%m-%d')
    
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}/candles.json"
    
    params = {
        'from': start_date,
        'till': end_date,
        'interval': interval
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        candles_data = data['candles']['data']
        columns = data['candles']['columns']
        
        # Создаем DataFrame для удобной работы
        df = pd.DataFrame(candles_data, columns=columns)
        
        # Преобразуем колонку с датой в формат datetime
        df['begin'] = pd.to_datetime(df['begin'])
        
        # Возвращаем только нужные колонки: дата, open, high, low, close
        return df[['begin', 'open', 'high', 'low', 'close']].tail(30) # последние 30 дней
        
    except Exception as e:
        print(f"Ошибка получения свечей для {ticker}: {e}")
        return pd.DataFrame() # Пустой DataFrame в случае ошибки
    
    
def get_stock_info(ticker):
    """Получить информацию о компании: название, сектор, ISIN"""
    url = f'https://iss.moex.com/iss/securities/{ticker}.json'
    params = {'iss.meta': 'off'}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {'shortname': 'Нет данных', 'latname': 'Нет данных', 
                'sector': 'Нет данных', 'isin': 'Нет данных'}
    
    info = {'shortname': 'Нет данных', 'latname': 'Нет данных', 
            'sector': 'Нет данных', 'isin': 'Нет данных'}
    
    try:
        # Данные в секции description
        description_data = data.get('description', {}).get('data', [])
        
        # Проходим по всем строкам
        for row in description_data:
            if len(row) >= 3:
                key = row[0]      # например 'SHORTNAME'
                value = row[2]    # значение
                
                if key == 'SHORTNAME':
                    info['shortname'] = value if value else 'Нет данных'
                elif key == 'LATNAME':
                    info['latname'] = value if value else 'Нет данных'
                elif key == 'SECTOR':
                    info['sector'] = value if value else 'Нет данных'
                elif key == 'ISIN':
                    info['isin'] = value if value else 'Нет данных'
    except Exception as e:
        print(f"Ошибка парсинга info для {ticker}: {e}")
    
    return info