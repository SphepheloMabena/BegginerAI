import requests
from bs4 import BeautifulSoup

def get_prices(fuel_type):
    DIESEL_PRICES_URL = "https://www.globalpetrolprices.com/South-Africa/diesel_prices/"
    PETROL_PRICES_URL = "https://www.globalpetrolprices.com/South-Africa/gasoline_prices/"

    if fuel_type == "petrol":
        PRICES_PAGE = requests.get(PETROL_PRICES_URL)
    else:
        PRICES_PAGE = requests.get(DIESEL_PRICES_URL)


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
