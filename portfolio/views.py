from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
import json

from .forms import PortfolioForm, Search_Tickers
from .moex_api import get_stock_price, search_ticker, get_candles



def index(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PortfolioForm()
    
    items = Portfolio.objects.all()
    
    # Добавляем цену к каждому элементу
    for item in items:
        item.current_price = get_stock_price(item.ticker) or 0
        item.total = item.quantity * item.current_price
    total_all = sum(item.current_price * item.quantity for item in items)
    
    return render(request, 'portfolio/index.html', {
        'form': form, 
        'portfolio_items': items, 
        'total_all': total_all
    })


def delete_position(request, position_id):
    """Удаление позиции из портфеля"""
    item = get_object_or_404(Portfolio, id=position_id)
    item.delete()
    return redirect('index')


def find_ticker(request):
    result = None
    if request.method == 'POST':
        form = Search_Tickers(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search_by_ticker']
            result = search_ticker(query)
    else:
        form = Search_Tickers()
    
    return render(request, 'portfolio/search.html', {
        'form': form, 
        'result': result
    })


def blue_chips(request):
    from .moex_api import get_blue_chips
    stocks = get_blue_chips()
    return render(request, 'portfolio/blue_chips.html', {'stocks': stocks})


def stock_chart(request, ticker):
    """Отображает страницу с графиком для конкретного тикера"""
    # Получаем данные свечей
    df = get_candles(ticker)
    
    # Преобразуем DataFrame в формат, понятный для JavaScript графиков
    chart_data = {
        'dates': df['begin'].dt.strftime('%Y-%m-%d').tolist() if not df.empty else [],
        'prices': df['close'].tolist() if not df.empty else [],
        'ticker': ticker
    }
    
    # Передаем данные в шаблон как JSON строку
    return render(request, 'portfolio/chart.html', {
        'chart_data_json': json.dumps(chart_data),
        'ticker': ticker
    })
    
    
def stock_info(request, ticker):
    """Страница с информацией о компании"""
    from .moex_api import get_stock_info, get_stock_price
    
    info = get_stock_info(ticker)
    price = get_stock_price(ticker)
    
    context = {
        'ticker': ticker,
        'info': info,
        'price': price,
    }
    return render(request, 'portfolio/stock_info.html', context)



