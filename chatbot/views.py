from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from chatbot.models import FuelPrice
from chatbot.utils import get_prices


# Create your views here.

class HomeView(View):
    petrol_price = FuelPrice.objects.filter(fuel_type='petrol').order_by('-date_added').first().litres_price
    diesel_price = FuelPrice.objects.filter(fuel_type='diesel').order_by('-date_added').first().gallons_price

    def get(self, request):
        context = {
            'petrol_price': self.petrol_price,
            'diesel_price': self.diesel_price,
        }
        return render(request, 'index.html', context)


class SaveFuelPriceView(View):

    def get(self, request, fuel_type):
        if fuel_type not in ['petrol', 'diesel']:
            return JsonResponse({'error': 'Invalid fuel type'}, status=400)

        litres, gallons = get_prices(fuel_type)

        # Save to the model
        fuel_price = FuelPrice(fuel_type=fuel_type, litres_price=litres, gallons_price=gallons)
        fuel_price.save()

        return JsonResponse({'message': f'{fuel_type} prices saved successfully!'})
