🚀 Overview
The Kayonza Smart Weather Station is a hybrid desktop and web application designed to support agriculture in the Eastern Province of Rwanda. It combines live satellite data with a custom AI model to provide accurate hyper-local weather forecasts and scientific farming advice.

This system helps farmers and agronomists make data-driven decisions by calculating Water Demand (ET₀) and Soil Moisture using FAO-56 standards.

🌟 Key Features
📡 Live Satellite Sync: Connects to the Open-Meteo API for real-time data on Rainfall, Temperature, and Soil Moisture.

🤖 AI Refinement: Uses a Machine Learning model (RandomForest) to refine satellite estimates based on local IOD/ENSO climate patterns.

🚜 Scientific Agri-Advice:

Calculates crop water demand (Evapotranspiration - ET₀).

Provides daily judgments (e.g., "Perfect Planting Day" vs. "Excess Rain Alert").

Based on UN FAO-56 Penman-Monteith standards.

🕰️ History & Future: Access 92 days of historical data and 16 days of future forecasts.

🔄 Hybrid Connectivity:

Desktop App: Works offline (using simulation/AI) and auto-syncs when internet is available.

Web Dashboard: For remote access via mobile phones.

🛠️ Technical Stack
Language: Python 3.10+

GUI Framework: Tkinter (Desktop), Streamlit (Web)

Data Science: Pandas, NumPy, Scikit-Learn, Joblib

API: Open-Meteo Agriculture API

Build Tool: PyInstaller (to generate .exe)

📂 Project Structure
app_dashboard.py: The main source code for the Desktop Application (Tkinter).

kayonza_web_pro.py: The source code for the Web Dashboard (Streamlit).

outputs/kayonza_brain.pkl: The pre-trained AI model used for rainfall prediction.

KayonzaWeatherApp.exe: The compiled standalone application for Windows.

💻 How to Run (For Developers)
1. Prerequisites
Ensure you have Python installed. Install the required dependencies:

Bash

pip install pandas numpy requests joblib scikit-learn streamlit
2. Running the Desktop App (Windows)
This launches the offline-capable graphical interface.

Bash

python app_dashboard.py
3. Running the Web Dashboard
This launches the remote-access web interface.

Bash

streamlit run kayonza_web_pro.py
📦 Installation for End-Users (Windows)
If you do not have Python installed, you can run the standalone application:

Download the Kayonza_Weather_System folder.

Open the folder and double-click KayonzaWeatherApp.exe.

Note: Ensure background.png and the outputs folder are in the same directory as the .exe.

🧠 The AI Model
The system uses a pre-trained kayonza_brain.pkl model.

Inputs: Satellite Rain, Indian Ocean Dipole (IOD), ENSO Index.

Output: Corrected Rainfall Probability.

Goal: To reduce the error margin of raw satellite data for the specific topography of Kayonza District.

📜 License
This project is open-source and developed for educational and community development purposes.
