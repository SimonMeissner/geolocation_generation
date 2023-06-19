import mysql.connector
from dotenv import load_dotenv
import os
import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import quote


def connectToDataBase() -> mysql.connector.connection_cext.CMySQLConnection:
    dotenv_path = '.env'  # Path to the .env file
    load_dotenv(dotenv_path)

    host = os.getenv('DB_HOST')  # Docker container name in Laravel Sail
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_DATABASE')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Connected to the database!")
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None
    

def insertLatitudeInDataBaseTableRow(connection: mysql.connector.connection_cext.CMySQLConnection, latitude_value: float, rowId: int, tableName: str):
    cursor = connection.cursor()
    query = f'UPDATE {tableName} SET lat = %s WHERE id = %s' 
    values = (latitude_value, rowId)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def insertLongitudeInDataBaseTableRow(connection: mysql.connector.connection_cext.CMySQLConnection, longitude_value: float ,rowId: int, tableName: str):
    cursor = connection.cursor()
    query = f'UPDATE {tableName} SET lng = %s WHERE id = %s' 
    values = (longitude_value, rowId)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def generateGeolocationFromAddress(country: str, city: str, zip: int, street_name: str, street_number: int):

    street_number_string = f'&housenumber={street_number}' if street_number  else ''
    street_name_string = f'&street={street_name}' if street_name else ''
    postcode_string = f'&postcode={zip}' if {zip} else ''
    city_string = f'&city={city}' if {zip} else ''
    country_string = f'&country={country}' if {country} else ''
    
    url = f'https://api.geoapify.com/v1/geocode/search?{street_number_string}{street_name_string}{postcode_string}{city_string}{country_string}&lang=en&limit=5&apiKey={os.getenv("GEOAPIFY_API_KEY")}'

    safeUrl = url.replace(' ', '%20')

    print(f'api call: {safeUrl}')

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    response = requests.get(safeUrl, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def generateGeolocationFromCity(country: str, city: str):
    
    url = f'https://api.geoapify.com/v1/geocode/search?city={city}&country={country}&lang=en&limit=5&type=city&apiKey={os.getenv("GEOAPIFY_API_KEY")}'

    safeUrl = url.replace(' ', '%20')

    print(f'api call: {safeUrl}')

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    response = requests.get(safeUrl, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def queryAllRowsFromDataBaseTable(connection: mysql.connector.connection_cext.CMySQLConnection, tableName: str):
    cursor = connection.cursor()
    query = f'SELECT * FROM {tableName}'
    cursor.execute(query)
    results = cursor.fetchall()
    return results


if __name__ == "__main__":
    startAtTableRowWithId = 1
    stopAtTableRowWithId = 2

    db_connection = connectToDataBase()

    if db_connection:
        contactInformationRows = queryAllRowsFromDataBaseTable(db_connection, 'contact_information')

        counter = 1
        for contactInformationRow in contactInformationRows:
            print(f'selected table row: {contactInformationRow[0]} | ', f'value1: {contactInformationRow[1]} | ', f'value2: {contactInformationRow[3]} | ', f'insert into table row: {counter}')

            if counter >= startAtTableRowWithId:
                response = generateGeolocationFromCity(contactInformationRow[1], contactInformationRow[3])
                insertLatitudeInDataBaseTableRow(db_connection, response['features'][0]['properties']['lat'], (counter), 'contact_information')
                insertLongitudeInDataBaseTableRow(db_connection, response['features'][0]['properties']['lon'], (counter), 'contact_information')
            
            counter += 1

            if counter == stopAtTableRowWithId:
                break


        db_connection.close()
    else:
        # Handle connection error
        print("Failed to connect to the database.")