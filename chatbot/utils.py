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

    if fuel_type == "petrol":
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
        litres = table_data_element[0].text
        gallons = table_data_element[1].text

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