import streamlit as st
import requests

# --- Streamlit Page Settings ---
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

# --- App Title and Instructions ---
st.title("🌦️ Mehreen's Weather App")
st.write("Enter a city name below to see current weather conditions in that location.")

# --- User Input ---
city = st.text_input("🌍 City Name")

# --- Get Weather Info ---
if city:
    api_key = "8422d0579f796c2c6558875825314c6a"  # You should move this to Streamlit Secrets for safety!
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "404":
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            st.subheader(f"📍 Weather in {city.capitalize()}")
            st.image(icon_url, width=100)
            st.write(f"🌤️ **Condition:** {weather}")
            st.write(f"🌡️ **Temperature:** {temp}°C")
            st.write(f"💧 **Humidity:** {humidity}%")
            st.write(f"💨 **Wind Speed:** {wind_speed} m/s")
        else:
            st.error("❌ City not found. Please check spelling and try again.")
    except Exception as e:
        st.error("⚠️ Something went wrong while fetching data. Please try again later.")
