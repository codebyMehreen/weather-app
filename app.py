import streamlit as st
import requests
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="Weather App", page_icon="🌦", layout="centered")
st.title("🌦 Mehreen's Weather App")
st.write("Enter a valid city name to see current weather conditions.")

# --- User Input ---
city = st.text_input("🌍 City Name")

if city:
    try:
        api_key = "8422d0579f796c2c6558875825314c6a"  # Replace with your API key

        # --- Validate city using Geocoding API ---
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            st.error("❌ This doesn't appear to be a valid city. Please try again.")
        else:
            # --- Extract coordinates ---
            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]
            city_name = geo_response[0]["name"]
            country = geo_response[0]["country"]

            # --- Get weather data by coordinates ---
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_data = requests.get(weather_url).json()

            if weather_data.get("cod") != 200:
                st.error("⚠️ Weather data not found.")
            else:
                # --- Extract weather info ---
                icon = weather_data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                desc = weather_data["weather"][0]["description"].title()
                temp = weather_data["main"]["temp"]
                feels_like = weather_data["main"]["feels_like"]
                humidity = weather_data["main"]["humidity"]
                wind = weather_data["wind"]["speed"]

                # --- Time conversion ---
                timezone_offset = weather_data["timezone"]
                sunrise = datetime.utcfromtimestamp(weather_data["sys"]["sunrise"] + timezone_offset).strftime('%I:%M %p')
                sunset = datetime.utcfromtimestamp(weather_data["sys"]["sunset"] + timezone_offset).strftime('%I:%M %p')

                # --- Display results ---
                st.subheader(f"📍 Weather in {city_name}, {country}")
                st.image(icon_url, width=100)
                st.markdown(f"🌤️ **Condition:** {desc}")

                # Show actual vs feels-like with comparison
                col1, col2 = st.columns(2)
                col1.metric("Temperature", f"{temp}°C")
                col2.metric("Feels Like", f"{feels_like}°C")

                # Optional comfort message
                difference = feels_like - temp
                if abs(difference) >= 3:
                    if feels_like > temp:
                        st.info("🥵 It's more humid or warmer than it looks today.")
                    else:
                        st.info("🥶 It feels chillier than the actual temperature. Bundle up!")

                st.markdown(f"💧 **Humidity:** {humidity}%")
                st.markdown(f"💨 **Wind Speed:** {wind} m/s")
                st.markdown(f"🌅 **Sunrise:** {sunrise}")
                st.markdown(f"🌇 **Sunset:** {sunset}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

        
                
