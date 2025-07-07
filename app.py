import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")
st.title("🌦️ Mehreen's Weather App")
st.write("Enter a city name below to see current weather conditions.")

# Input for city
city = st.text_input("🌍 City Name")

if not city:
    st.info("👋 Please enter a city name to get the weather.")

if city:
    try:
        api_key = "8422d0579f796c2c6558875825314c6a"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 404:
            # Basic weather details
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            # Timezone-adjusted sunrise and sunset
            sunrise_ts = data["sys"]["sunrise"]
            sunset_ts = data["sys"]["sunset"]
            timezone_offset = data["timezone"]  # in seconds

            sunrise_time = datetime.utcfromtimestamp(sunrise_ts + timezone_offset).strftime("%I:%M %p")
            sunset_time = datetime.utcfromtimestamp(sunset_ts + timezone_offset).strftime("%I:%M %p")

            # Display weather
            st.subheader(f"📍 Weather in {city.capitalize()}")
            st.image(icon_url, width=100)
            st.write(f"🌤️ **Condition:** {weather}")
            st.write(f"🌡️ **Temperature:** {temp}°C")
            st.write(f"💧 **Humidity:** {humidity}%")
            st.write(f"💨 **Wind Speed:** {wind_speed} m/s")
            st.write(f"🌅 **Sunrise:** {sunrise_time}")
            st.write(f"🌇 **Sunset:** {sunset_time}")
        else:
            st.error("❌ City not found. Please check the spelling and try again.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
