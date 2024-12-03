from django.urls import path
from . import views
from .views import market_data_view

urlpatterns = [
    path('', views.stockPicker, name='stockpicker'),
    path('market-data/', market_data_view, name='market-data'),
]
