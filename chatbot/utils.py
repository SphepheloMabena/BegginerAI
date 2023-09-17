import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import googlemaps
from geopy.geocoders import Nominatim

import geocoder


# Load environment variables from .env file
env_path = Path('beginneraichat') / '.env'
load_dotenv(dotenv_path=env_path)


def get_prices(fuel_type):
    """"Returns the current petrol and diesel prices in South Africa"""

    diesel_prices_url = "https://www.globalpetrolprices.com/South-Africa/diesel_prices/"
    petrol_prices_url = "https://www.globalpetrolprices.com/South-Africa/gasoline_prices/"

    if fuel_type == "petrol":
        PRICES_PAGE = requests.get(petrol_prices_url)
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

    querystring = {"make": make, "year": year, "model": model}

    headers = {
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
        "X-RapidAPI-Host": "cars-fuel-consumption.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    car_data = response.json()
    return car_data


def get_car_fuel_consumption(car_data):
    """Returns the fuel consumption of a car in litres per 100km"""
    if car_data[0]["fuel_Consumtion_Combo"] > 0:
        return car_data[0]["fuel_Consumtion_Combo"]
    else:
        return 7
    


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


def scrape_historical_fuel_prices():
    """Scrapes historical fuel prices from the sapia website"""

    base_url = "https://www.sapia.org.za/old-fuel-prices/"
    years = list(range(2012, 2023))  # Years from 2012 to 2022

    fuel_data = {}

    for year in years:
        url = f"{base_url}#tablepress-{year}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", class_=f"tablepress-id-{year}")

        if table:
            rows = table.find_all("tr")
            header = [header.text.strip() for header in rows[0].find_all("th")]

            year_data = []

            for row in rows[1:]:
                cells = [cell.text.strip() for cell in row.find_all("td")]
                entry = dict(zip(header, cells))
                year_data.append(entry)

                # Convert prices from cents to rands
            # Convert prices from cents to rands for numeric values
            for entry in year_data:
                for key, value in entry.items():
                    if key != "YR2012" and key != "" and value != "":
                        try:
                            entry[key] = f"{float(value) / 100:.2f}"  # Convert to rands with two decimal places
                        except ValueError:
                            pass  # Skip conversion for non-numeric values # Convert to rands with two decimal places

            # Filter out "COASTAL" and "GAUTENG" data
            filtered_data = [entry for entry in year_data if
                             entry.get(f"YR{year}") not in ("COASTAL", "") and
                             entry.get(f"YR{year}") not in ("GAUTENG", "")]

            fuel_data[str(year)] = filtered_data

    # Save the data to a JSON file
    with open("fuel_prices.json", "w") as json_file:
        json.dump(fuel_data, json_file, indent=4)

def calculateDistance(fromWhere, destinationn):
 
    # Requires API key
    gmaps = googlemaps.Client(key='AIzaSyDSnqPcx0ObekjzjZAwDJHjVDhj5M5KmSg')


    
    # Requires cities name
    my_dist = gmaps.distance_matrix(fromWhere, destinationn)['rows'][0]['elements'][0]
    
    # Printing the result
    distance = my_dist["distance"]["value"]

    return distance


def get_current_location():
    # Using the 'ipinfo' provider to get location based on your IP address
    location = geocoder.ipinfo('me')
    return location.latlng  # Returns a tuple of latitude and longitude



if __name__ == "__main__":
    calculateDistance("Pretoria", "Benoni")
    current_location = get_current_location()
    print(f"Latitude: {current_location[0]}, Longitude: {current_location[1]}")
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.reverse((current_location[0], current_location[1]))
    scrape_historical_fuel_prices()
