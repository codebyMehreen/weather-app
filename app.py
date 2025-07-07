import streamlit as st
import requests
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="WeatherWatch", page_icon="🌦", layout="centered")

# --- Branding ---
st.markdown("<h1 style='text-align: center;'>🌦️ WeatherWatch</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Presented by <strong>Mehreen</strong> — crafted with Python & Streamlit</p>", unsafe_allow_html=True)
st.write("")  # spacing

# --- Input field ---
city = st.text_input("🌍 Enter City Name")

if city:
    try:
        api_key = "8422d0579f796c2c6558875825314c6a"  # Replace with your actual API key

        # --- Geolocation validation ---
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            st.error("❌ Invalid city name. Please enter a real location.")
        else:
            # --- Extract location data ---
            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]
            city_name = geo_response[0]["name"]
            country = geo_response[0]["country"]

            # --- Fetch weather data via coordinates ---
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_data = requests.get(weather_url).json()

            if weather_data.get("cod") != 200:
                st.error("⚠️ Weather data not available.")
            else:
                # --- Weather details ---
                icon = weather_data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                desc = weather_data["weather"][0]["description"].title()
                temp = weather_data["main"]["temp"]
                feels_like = weather_data["main"]["feels_like"]
                humidity = weather_data["main"]["humidity"]
                wind = weather_data["wind"]["speed"]
                timezone_offset = weather_data["timezone"]

                # --- Time conversion ---
                sunrise = datetime.utcfromtimestamp(weather_data["sys"]["sunrise"] + timezone_offset).strftime('%I:%M %p')
                sunset = datetime.utcfromtimestamp(weather_data["sys"]["sunset"] + timezone_offset).strftime('%I:%M %p')

                # --- Weather Display ---
                st.subheader(f"📍 Weather in {city_name}, {country}")
                st.image(icon_url, width=100)
                st.markdown(f"🌤️ **Condition:** {desc}")

                # Temperature comparison
                col1, col2 = st.columns(2)
                col1.metric("Temperature", f"{temp}°C")
                col2.metric("Feels Like", f"{feels_like}°C")

                # Comfort advisory
                difference = feels_like - temp
                if abs(difference) >= 3:
                    if feels_like > temp:
                        st.info("🥵 It feels warmer and more humid than the actual temperature.")
                    else:
                        st.info("🥶 It feels colder than it looks. Keep warm!")

                # Extras
                st.markdown(f"💧 **Humidity:** {humidity}%")
                st.markdown(f"💨 **Wind Speed:** {wind} m/s")
                st.markdown(f"🌞 **Sunrise:** {sunrise}")
                st.markdown(f"🌜 **Sunset:** {sunset}")

                # Footer credit
                st.write("---")
                st.caption("🔗 Data by OpenWeatherMap • Developed with ❤️ by Mehreen")

    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")

        
                
