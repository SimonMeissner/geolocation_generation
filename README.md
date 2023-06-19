# geolocation_generation

This repository contains a python script which was used to seed a database table containing address data with geographic data using latitude and longitude coordinate pairs.
It communicates with the geoapify api which has a free subscription plan with up to 3000 requests/day. For more information visit: [Geoapify](https://www.geoapify.com/)

### Two granularity options

We provide two functions which address different api endpoints. If you have fine granularity in your address data use the generateGeolocationFromAddress() function.
```python

response = generateGeolocationFromAddress(country, city, zip, street_name, street_number)

```
If you use only country and city data for your address data use the generateGeolocationFromCity() function.
```python

response = generateGeolocationFromCity(country, city)

```

### Specify table_rows_ids affected

The script works on id selection. You can specify an id range in your database table in where you want to generate geographic data. You will find it in the main function.
```python

startAtTableRowWithId = 1
stopAtTableRowWithId = 2

```

### Get started
1. Create .env file from .env.example
2. Provide your database data in .env file to be able to connect to your database
3. Provide your indivdual geoapify api key in .env file
4. in all functions using table_name as a variable insert your specific table name which contains your address data
5. Configure the main function according to your needs.
