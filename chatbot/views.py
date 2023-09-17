import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from chatbot.models import FuelPrice, Chat
from chatbot.utils import get_prices, calculateDistance

import os
from pathlib import Path
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

# Load environment variables from .env file
env_path = Path('beginneraichat') / '.env'
load_dotenv(dotenv_path=env_path)

# Create your views here.
stemmer = PorterStemmer()

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
        valid_greetings = ['hi', 'hello', 'hey', 'howdy', 'hola', 'bonjour', 'oi', 'greetings', 'sup']

        # Prepare the request to the external service
        url = "http://5827294430427910.eu-central-1.pai-eas.aliyuncs.com/api/predict/chatbot_service"
        headers = {
            "Authorization": os.getenv("EAS-KEY")
        }

        response = requests.post(url, headers=headers, data=user_message.encode('utf-8'))

        def contains_keywords(sentence):
            keywords = ['travel', 'go', 'drive', 'driving', 'petrol', 'diesel', 'price', 'cost', 'distance', 'litres', 'gallons', 'km', 'kilometres', 'kilometers', 'litre']
            # Convert the sentence to lowercase to make it case-insensitive
            sentence = sentence.lower()
            
            # Check if any of the keywords is in the sentence
            for keyword in keywords:
                if keyword.lower() in sentence:
                    return True
                
            return False
       

        if contains_keywords(user_message):

            wordsTokenized= word_tokenize(user_message)
            stemmed_words = PorterStemmer()

            string_for_stemming = user_message

            words = word_tokenize(string_for_stemming)


            stemmed_words = [stemmer.stem(word) for word in words]
            print(f"Stemmed Words: {stemmed_words}")
            fuel_price = get_prices('petrol')

            for stem in stemmed_words:
                if stem == "travel":
                    bot_message = "Please give us you start and final destination and also the car and model you will be using"
                if stem == "go": 
                    bot_message = "Please give us you start and final destination and also the car and model you will be using"
                if stem == "driving To":
                    bot_message = "Please give us you start and final destination and also the car and model you will be using"
                if stem == "drive":
                    bot_message = "Please give us you start and final destination and also the car and model you will be using"

                if stem == "petrol":
                    bot_message = f"The current price of petrol is R{fuel_price}"

            fuel_price = get_prices('petrol')[0]

            get_distnce = calculateDistance("BCX Centurion", "Mall of Africa")
            calculatedDistance = int(get_distnce)/1000
            full_tank = int(fuel_price * calculatedDistance)

            message = (f"The distance between BCX Centurion and Mall of Africa is {calculatedDistance}km and the price of "
                        f"petrol is R{fuel_price} per litre. It will cost you R{full_tank} to travel from BCX Centurion "
                        f"to Mall of Africa")

            chat = Chat(user_message=user_message, bot_message=message)
            chat.save()

            context = {
                'user_message': user_message,
                'bot_message': message,
                'chat_history': self.get_chat_history()
            }
        
        else:
            message = response.text if response.status_code == 200 else "Sorry, I couldn't process that."

            chat = Chat(user_message=user_message, bot_message=message)
            chat.save()

            context = {
                'user_message': user_message,
                'bot_message': message,
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
        bot_message
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
