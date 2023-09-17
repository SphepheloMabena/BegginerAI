import json
import psycopg2

# Define your PostgreSQL connection parameters
db_params = {
    "host": "8.209.82.117",
    "database": "chatdb",
    "user": "chatadmin",
    "password": "B3ginner@!2023",
}

# Load data from the JSON file
with open("fuel_prices.json", "r") as file:
    data = json.load(file)

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Check if Historical_Fuel_Price_History table exists, and create it if not
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Historical_Fuel_Price_History (
            year VARCHAR(4),
            fuel_type VARCHAR(50),
            month DATE,
            price NUMERIC
        )
        """
    )

    print("Successfully connected to the PostgreSQL database.")
    print("Inserting data into the PostgreSQL database...")
    # Loop through the years and fuel types in the JSON data
    for year, fuel_data in data.items():
        for fuel_entry in fuel_data:
            fuel_type = fuel_entry.get(f"YR{year}")
            if fuel_type:
                # Loop through the months and prices for each fuel type
                for month, price in fuel_entry.items():
                    if (
                        month != f"YR{year}"  # Exclude the year field
                        and price is not None  # Check for None values
                        and price.strip() != ""  # Check for empty strings
                    ):
                        
                        # Replace commas with periods and convert the price to float
                        price = price.replace(",", ".")

                        # Construct the SQL query and insert data into the database
                        insert_query = """
                            INSERT INTO Historical_Fuel_Price_History (year, fuel_type, month, price)
                            VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(
                            insert_query, (year, fuel_type, month, float(price))
                        )

    # Commit the changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data has been successfully inserted into the PostgreSQL database.")

except Exception as e:
    print(f"Error: {e}")
