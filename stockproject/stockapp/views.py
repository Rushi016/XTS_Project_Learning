from django.shortcuts import render
from .models import MasterInstruments

# Create your views here.
def stockPicker(request):
    return render(request, 'stockapp/stockpicker.html')

def market_data_view(request):
    market_data = MasterInstruments.objects.all()[:20]  # Fetching first 20 rows of MarketData
    return render(request, 'stockapp/market_data.html', {'market_data': market_data})
