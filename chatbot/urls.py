from django.urls import path
from .views import SaveFuelPriceView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('save_fuel_price/<str:fuel_type>/', SaveFuelPriceView.as_view(), name='save_fuel_price'),
]
