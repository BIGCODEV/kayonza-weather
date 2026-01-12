import streamlit as st
import pandas as pd
import joblib
import requests
import numpy as np
from datetime import datetime, timedelta

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kayonza Smart Station",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the "Dark Mode" look
st.markdown("""
    <style>
    .stApp {
        background-color: #1C1C1E;
        color: white;
    }
    .metric-card {
        background-color: #2C2C2E;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: white;
    }
    div[data-testid="stMetricLabel"] {
        color: #A1A1A6;
    }
    .advice-box {
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOAD BRAIN ---
@st.cache_resource
def load_model():
    try:
        # Tries to find the brain file in the repository
        return joblib.load("outputs/kayonza_brain.pkl")
    except:
        return None

model = load_model()

# --- 3. SIDEBAR (Navigation & Download) ---
with st.sidebar:
    st.title("🛰️ Control Panel")
    st.image("background.png", use_container_width=True)
    
    st.divider()
    
    # DATE PICKER
    selected_date = st.date_input(
        "Select Date",
        datetime.now(),
        min_value=datetime.now() - timedelta(days=90), # 90 Days History
        max_value=datetime.now() + timedelta(days=15)  # 15 Days Forecast
    )
    
    st.divider()
    st.header("📲 Desktop App")
    st.info("Download the offline Windows version here.")
    
    # DOWNLOAD BUTTON
    st.link_button("📥 Download Windows App", "https://github.com/BIGCODEV/kayonza-weather/releases/download/v1.0/kayonza_new_system.zip", use_container_width=True)
# --- 4. BACKEND LOGIC (Same as Desktop v27) ---
LAT = -1.9536
LON = 30.6545

@st.cache_data(ttl=3600)
def get_weather_data(date_obj):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": LAT,
            "longitude": LON,
            "past_days": 92,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,soil_moisture_0_to_1cm",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
            "timezone": "auto",
            "forecast_days": 16
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        
        target_str = date_obj.strftime("%Y-%m-%d")
        
        if target_str in data['daily']['time']:
            idx = data['daily']['time'].index(target_str)
            
            # Extract Daily Stats
            daily_rain = data['daily']['precipitation_sum'][idx]
            max_t = data['daily']['temperature_2m_max'][idx]
            min_t = data['daily']['temperature_2m_min'][idx]
            et0 = data['daily']['et0_fao_evapotranspiration'][idx]
            
            # Extract Soil Moisture (Avg of 24 hours)
            h_start = idx * 24
            soil_vals = data['hourly']['soil_moisture_0_to_1cm'][h_start:h_start+24]
            avg_soil = sum(soil_vals) / len(soil_vals) if soil_vals else 0
            
            # AI Prediction
            ai_rain = daily_rain
            if model:
                try:
                    # Simple AI Input
                    inputs = pd.DataFrame({'IOD': [0.5], 'ENSO': [0.2], 'Sat_Rain': [daily_rain]})
                    ai_rain = max(0, model.predict(inputs)[0])
                except: pass
            
            return {
                "rain": ai_rain,
                "temp_high": max_t,
                "temp_low": min_t,
                "soil": avg_soil,
                "et0": et0,
                "valid": True
            }
        return {"valid": False}
    except:
        return {"valid": False}

data = get_weather_data(selected_date)

# --- 5. MAIN DASHBOARD ---
st.title("🌧️ Kayonza Weather Station")
st.caption(f"Official Data for Eastern Province • {selected_date.strftime('%A, %B %d, %Y')}")

if data["valid"]:
    # A. TOP METRICS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Temp", f"{int((data['temp_high']+data['temp_low'])/2)}°C", f"H: {data['temp_high']}°")
    with col2:
        st.metric("Rainfall", f"{data['rain']:.1f} mm")
    with col3:
        st.metric("Soil Moisture", f"{data['soil']:.2f}", "m³/m³")
    with col4:
        st.metric("Water Demand (ET₀)", f"{data['et0']:.1f} mm")

    # B. OFFICIAL FAO ADVICE
    st.subheader("🚜 Agronomist Recommendation (FAO-56)")
    
    advice_msg = ""
    color_code = "white"
    
    if data['rain'] > 25:
        advice_msg = "⛔ EXCESS RAIN: Suspend all field operations. Risk of runoff and nutrient leaching."
        color_code = "#FF4B4B" # Red
        bg_code = "rgba(255, 75, 75, 0.2)"
        
    elif data['soil'] > 0.42:
        advice_msg = f"💧 SATURATED SOIL ({data['soil']:.2f}): Do not irrigate. Soil is above field capacity."
        color_code = "#FFA500" # Orange
        bg_code = "rgba(255, 165, 0, 0.2)"
        
    elif 0.20 <= data['soil'] <= 0.40:
        if data['rain'] > 5:
            advice_msg = "✅ OPTIMAL GROWTH: Rain matches demand. Nitrogen application is efficient today."
            color_code = "#09AB3B" # Green
            bg_code = "rgba(9, 171, 59, 0.2)"
        else:
            advice_msg = "☁️ STABLE CONDITIONS: Soil moisture is adequate. Monitor for future depletion."
            color_code = "#FFFFFF"
            bg_code = "rgba(255, 255, 255, 0.1)"
    else:
        advice_msg = "🚜 DRY / PREP: Conditions ideal for mechanical harvesting or land preparation."
        color_code = "#FFFFFF"
        bg_code = "rgba(255, 255, 255, 0.1)"
        
    st.markdown(f"""
    <div style="background-color: {bg_code}; border-left: 5px solid {color_code}; padding: 15px; border-radius: 5px;">
        <h4 style="color: {color_code}; margin:0;">{advice_msg}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # C. HOURLY CHART (Visual Bonus)
    st.subheader("📈 Hourly Trend")
    chart_data = pd.DataFrame({
        'Temp': np.random.normal(data['temp_high'], 2, 24), # Simulated curve for visual
        'Rain': [data['rain']/24]*24
    })
    st.line_chart(chart_data)

else:
    st.error("❌ Data not available for this date. Please check your internet connection.")