import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(page_title="Weather App", page_icon="🌦", layout="centered")
st.title("🌦 Mehreen's Weather App")
st.write("Enter a valid city name to see current weather conditions.")

# Input box
city = st.text_input("🌍 City Name")

if city:
    try:
        api_key = "8422d0579f796c2c6558875825314c6a"  # Replace with your own API key

        # Validate city using Geocoding API
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            st.error("❌ This doesn't appear to be a valid city. Please try again.")
        else:
            # Extract valid coordinates
            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]
            city_name = geo_response[0]["name"]
            country = geo_response[0]["country"]

            # Get weather by coordinates
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_data = requests.get(weather_url).json()

            if weather_data.get("cod") != 200:
                st.error("⚠️ Weather data not found.")
            else:
                icon = weather_data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                desc = weather_data["weather"][0]["description"].title()
                temp = weather_data["main"]["temp"]
                humidity = weather_data["main"]["humidity"]
                wind = weather_data["wind"]["speed"]

                # Time conversion
                sunrise = datetime.utcfromtimestamp(weather_data["sys"]["sunrise"] + weather_data["timezone"]).strftime('%I:%M %p')
                sunset = datetime.utcfromtimestamp(weather_data["sys"]["sunset"] + weather_data["timezone"]).strftime('%I:%M %p')

                # Display results
                st.subheader(f"📍 Weather in {city_name}, {country}")
                st.image(icon_url, width=100)
                st.markdown(f"🌤️ **Condition:** {desc}")
                st.markdown(f"🌡️ **Temperature:** {temp}°C")
                st.markdown(f"💧 **Humidity:** {humidity}%")
                st.markdown(f"💨 **Wind Speed:** {wind} m/s")
                st.markdown(f"🌅 **Sunrise:** {sunrise}")
                st.markdown(f"🌇 **Sunset:** {sunset}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

        
                
