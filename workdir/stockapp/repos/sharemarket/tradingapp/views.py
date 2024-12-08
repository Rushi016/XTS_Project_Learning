from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from .models import MasterInstrument


def market_data_view(request):
    """
    Handles market data search and retrieval.
    """
    query = request.GET.get('q', '')
    instruments = []

    if query:
        instruments = MasterInstrument.objects.filter(
            Q(Name__icontains=query) |
            Q(ExchangeInstrumentID__icontains=query) |
            Q(Description__icontains=query) |
            Q(InstrumentID__icontains=query)
        )
    else:
        instruments = MasterInstrument.objects.all()[:10]  # Default list

    return render(request, 'search.html', {'instruments': instruments, 'query': query})


def stock_suggestions(request):
    query = request.GET.get('q', '').strip()
    if query:
        suggestions = MasterInstrument.objects.filter(Name__icontains=query).values_list('Name', flat=True).distinct()[:10]
    else:
        suggestions = []
    return render(request, 'suggestions.html', {'suggestions': suggestions})