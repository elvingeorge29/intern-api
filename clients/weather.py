import requests

def fetch_daily_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"      #API weather URL

    params = {                  #Parameters
        "latitude": latitude,
        "longitude": longitude, 
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "past_days": 7,
        "forecast_days": 0,
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10) #Show error if meteo takes longer than 10 seconds to respond

    response.raise_for_status()     #Line will raise exception to show what went wrong

    return response.json()

if __name__ == "__main__":
    lat = 41.5868       #Latitude for Des Moines
    lon = -93.6250      #Longitude for Des Moines 
    
    data = fetch_daily_weather(lat, lon)
    
    dates = data["daily"]["time"]                   #Extract the lists from the JSON
    highs = data["daily"]["temperature_2m_max"]
    
    for date, high in zip(dates, highs):
        print(f"Date: {date}, High: {high}°C")      #Print them out
