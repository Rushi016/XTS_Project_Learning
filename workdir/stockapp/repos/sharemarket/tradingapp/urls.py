from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_data_view, name='home'),
    path('market-data/', views.market_data_view, name='market_data'),
    path('stock-suggestions/', views.stock_suggestions, name='stock_suggestions'),
]
