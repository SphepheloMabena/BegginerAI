import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from chatbot.models import FuelPrice, Chat
import chatbot.utils as utils

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('beginneraichat') / '.env'
load_dotenv(dotenv_path=env_path)

# Create your views here.

class HomeView(View, LoginRequiredMixin):
    petrol_price = FuelPrice.objects.filter(fuel_type='petrol').order_by('-date_added').first().litres_price
    diesel_price = FuelPrice.objects.filter(fuel_type='diesel').order_by('-date_added').first().gallons_price

    def get_chat_history(self):
        return Chat.objects.all().order_by('-id')[:10]
    
    def append_user_message_to_history(user_message):
        """
        Appends the user's message to the chat history list.

        Args:
            user_message (str): The user's message to be appended to the history.
        """

    def get(self, request):
        context = {
            'petrol_price': self.petrol_price,
            'diesel_price': self.diesel_price,
            'chat_history': self.get_chat_history()
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('user_message')
        cars = ['bmw', 'hyuandai', 'kia']

        for word in user_message:
            if word in cars:
                car_make = word

            if word in range(1990, 2022):
                car_year = word

            if word in ['m4', 'm5', 'm6']:
                car_model = word

        if car_make.empty() or car_year.empty() or car_model.empty():
            if car_make.empty():
               bot_response = "Please provide the car make"
            elif car_year.empty():
                bot_response = "Please provide the car year"
            elif car_model.empty():
                bot_response = "Please provide the car model"

        bot_capcity_promt = "Please provide the fuel tank capicty in litres"
        bot_fuel_type_prompt = "Please provide the fuel type (petrol or diesel)"

        if bot_fuel_type_prompt.empty() or bot_fuel_type_prompt not in ['petrol', 'diesel']:
            bot_response = "Please provide the fuel type (petrol or diesel)"

        
        car_data = utils.get_car_info(car_make, car_year, car_model)
        consumption = utils.get_fuel_consumption(car_data)
        fuel_price = utils.get_prices(bot_fuel_type_prompt)
        full_tank = float(fuel_price) * float(bot_capcity_promt)
        # litres_used = utils.calculate_litres_used(distance, consumption)
        bot_response = f"Fuel consumption for your car is {consumption} per 100km. The price of fuel is {fuel_price} per litre. A full tank will cost {full_tank}."

        # Prepare the request to the external service
        url = "http://5827294430427910.eu-central-1.pai-eas.aliyuncs.com/api/predict/chatbot_service"
        headers = {
            "Authorization": os.getenv("EAS-KEY")
        }
        response = requests.post(url, headers=headers, data=user_message.encode('utf-8'))

        # Process the response or set a default message
        bot_message = response.text if response.status_code == 200 else "Sorry, I couldn't process that."

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

        litres, gallons = utils.get_prices(fuel_type)

        # Save to the model
        fuel_price = FuelPrice(fuel_type=fuel_type, litres_price=litres, gallons_price=gallons)
        fuel_price.save()

        return JsonResponse({'message': f'{fuel_type} prices saved successfully!'})
