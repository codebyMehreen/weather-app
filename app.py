import requests

def get_weather(city):
    api_key = "8422d0579f796c2c6558875825314c6a"  # <-- Replace with your actual API key!
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print(f"\n📍 Weather in {city.capitalize()}:")
        print(f"🌤️  {weather.title()}")
        print(f"🌡️  Temperature: {temp}°C")
        print(f"💧 Humidity: {humidity}%")
        print(f"💨 Wind Speed: {wind_speed} m/s\n")
    else:
        print("\n❌ City not found. Please try again!\n")

city = input("Enter city name: ")
get_weather(city)
