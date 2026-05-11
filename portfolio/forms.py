from django import forms
from .models import Portfolio, Ticker

class YourForm(forms.Form):
    ticker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'ticker', 'quantity']
        
        
class Search_Tickers(forms.ModelForm):
    class Meta:
        model = Ticker
        fields = ['search_by_ticker']  # должно совпадать с именем поля в модели
    