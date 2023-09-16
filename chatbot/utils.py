import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('beginneraichat') / '.env'
load_dotenv(dotenv_path=env_path)


def get_prices(fuel_type):
    """"Returns the current petrol and diesel prices in South Africa"""

    diesel_prices_url = "https://www.globalpetrolprices.com/South-Africa/diesel_prices/"
    prices_prices_url = "https://www.globalpetrolprices.com/South-Africa/gasoline_prices/"
    diesel_prices_url = "https://www.globalpetrolprices.com/South-Africa/diesel_prices/"
    prices_prices_url = "https://www.globalpetrolprices.com/South-Africa/gasoline_prices/"

    if fuel_type == "petrol":
        PRICES_PAGE = requests.get(prices_prices_url)
        PRICES_PAGE = requests.get(prices_prices_url)
    else:
        PRICES_PAGE = requests.get(diesel_prices_url)


    soup = BeautifulSoup(PRICES_PAGE.content, "html.parser")
    results = soup.find(id="graphPageLeft")

    job_elements = results.find_all("table")

    for job_element in job_elements:
        table_body_element = job_element.find("tbody")
        table_row_element = table_body_element.find("tr")
        table_data_element = table_row_element.find_all("td")
        litres = float(table_data_element[0].text)
        gallons = float(table_data_element[1].text)

    return litres, gallons


def get_car_models(make, year, model):
    """Returns a list of car models"""

    url = "https://cars-fuel-consumption.p.rapidapi.com/v1/Car/GetModel"

    querystring = {"make":make,"year":year,"model":model}

    headers = {
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
        "X-RapidAPI-Host": "cars-fuel-consumption.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    car_data = response.json()
    return car_data


def get_car_fuel_consumption(car_data):
    """Returns the fuel consumption of a car in litres per 100km"""	
    return car_data[0]["fuel_Consumtion_Combo"]


def calculate_litres_used(distance, fuel_consumption):
    """Returns the litres of fuel used for a given distance"""
    return (distance / 100) * fuel_consumption


def calculate_price(litres, price_per_litre):
    """Returns the price of fuel for a given number of litres"""
    return litres * price_per_litre


def calculate_fuel_price(litres, price_per_litre):
    """Returns the price of fuel for a given number of litres"""
    litres = float(litres)
    return litres * price_per_litre


def get_car_info():
    car_make = input("> Enter the make of your car: ")
    car_year = input("> Enter the year of your car: ")
    car_model = input("> Enter the model of your car: ")
    return car_make, car_year, car_model


def chat():
    """Chat with the user"""
    while True:
        user_input = input("\nEnter your message: ")

        if user_input == "quit":
            break

        if user_input == "price of petrol" or user_input == "price of diesel":

            fuel_type = "petrol" if user_input == "price of petrol" else "diesel"
            car_make, car_year, car_model = get_car_info()
            car_data = get_car_models(car_make, car_year, car_model)
            fuel_consumption = get_car_fuel_consumption(car_data)
            litres, gallons = get_prices(fuel_type)

            print(f"\nYour car has a fuel consumption rate of {fuel_consumption} liters per 100 kilometers on {fuel_type}, which translates to an estimated cost of R{litres} per liter.")

       
        elif user_input.lower() == "fuel price":
            distance = int(input("> Enter the distance you will be traveling (km): "))
            car_make, car_year, car_model = get_car_info()
            car_data = get_car_models(car_make, car_year, car_model)
            fuel_consumption = get_car_fuel_consumption(car_data)
            fuel_type = input("> Does your car use diesel or petrol?: ").lower()
            price_per_litre, gallons = get_prices(fuel_type)

            litres_used = int(calculate_litres_used(distance, fuel_consumption))
            fuel_price = int(calculate_fuel_price(litres_used, price_per_litre))

            print(f"\nYou will use {litres_used} litres of fuel for your {distance}km trip, which will cost you around R{fuel_price}.")


if __name__ == "__main__":
    chat()