from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from chatbot.models import FuelPrice, Chat
from chatbot.utils import get_prices, get_response


# Create your views here.

class HomeView(View, LoginRequiredMixin):
    petrol_price = FuelPrice.objects.filter(fuel_type='petrol').order_by('-date_added').first().litres_price
    diesel_price = FuelPrice.objects.filter(fuel_type='diesel').order_by('-date_added').first().gallons_price

    def get_chat_history(self):
        return Chat.objects.all().order_by('-id')[:10]

    def get(self, request):
        context = {
            'petrol_price': self.petrol_price,
            'diesel_price': self.diesel_price,
            'chat_history': self.get_chat_history()
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('user_message')
        bot_message = get_response(user_message)
        chat = Chat(user_message=user_message, bot_message=bot_message)
        chat.save()
        context = {
            'user_message': user_message,
            'bot_message': bot_message,
            'chat_history': self.get_chat_history()
        }
        return render(request, 'index.html', context)


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a welcome message for the user
            Chat.objects.create(user=user, user_message='', bot_message='Hi, how can I help you?')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class ChatView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('user_message')
        bot_message = get_response(user_message)
        chat = Chat(user_message=user_message, bot_message=bot_message)
        chat.save()
        return render(request, 'index.html', {'user_message': user_message, 'bot_message': bot_message})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class SaveFuelPriceView(View):

    def get(self, request, fuel_type):
        if fuel_type not in ['petrol', 'diesel']:
            return JsonResponse({'error': 'Invalid fuel type'}, status=400)

        litres, gallons = get_prices(fuel_type)

        # Save to the model
        fuel_price = FuelPrice(fuel_type=fuel_type, litres_price=litres, gallons_price=gallons)
        fuel_price.save()

        return JsonResponse({'message': f'{fuel_type} prices saved successfully!'})
