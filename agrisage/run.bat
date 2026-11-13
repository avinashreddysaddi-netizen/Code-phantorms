@echo off
echo ====================================================
echo   Starting AgriSage AI - Smart Farming Helper 🌾
echo ====================================================
echo.
echo 1. Checking and installing required packages...
pip install -r requirements.txt
echo.
echo 2. Generating demo sample leaf images...
python create_sample_leaves.py
echo.
echo 3. Launching Streamlit Dashboard...
streamlit run app.py
pause

