import requests


LOCATIONS = [
    {"name": "Des Moines", "lat": 41.5868, "lon": -93.6250},
    {"name": "Midland", "lat": 31.9974, "lon": -102.0779},
    {"name": "Wichita", "lat": 37.6872, "lon": -97.3301}
]

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

def to_days(location_name, data):       #Extract parallel JSON arrays 
    dates = data ["daily"]["time"]
    highs  = data ["daily"]["temperature_2m_max"]
    lows = data ["daily"]["temperature_2m_min"]
    precips = data ["daily"]["precipitation_sum"]

    days = []       #Combined List of flat dictionaries
    for date, high, low, precip in zip(dates, highs, lows, precips, strict = True):     #Strict = True, crash if arrays dont match 
        day_record = {
            "location": location_name,
            "date": date,
            "high_c": high,
            "low_c": low,
            "precip_mm": precip
        }
        days.append(day_record)     #Adds to the end of the days list
    return days                     #Return the days that were called

def fetch_all(locations):
    all_days = []
    for loc in locations:
        data = fetch_daily_weather(loc["lat"], loc["lon"])  #Fetch the raw data for this location
        
        days = to_days(loc["name"], data)   #Convert it to a clean list of days
        
        all_days.extend(days)           #Add them to the master list
        
    return all_days


if __name__ == "__main__":
    print("Fetching weather for all locations")
    
    all_days = fetch_all(LOCATIONS)                 #Fetch and format all the days
    
    for day in all_days:                    #Calls day to go through all the lists one at a time then print 
        print(f"{day['location']} | {day['date']} | High: {day['high_c']}°C | Low: {day['low_c']}°C | Precip: {day['precip_mm']}mm")
