# 🌾 AgriSage AI - Smart Farming Helper
> **A multi-agent agricultural helper that gives clear, daily crop guidance in English and Telugu.**

---

## 📖 The Big Idea (Explain Like I'm 5)
Imagine a small village clubhouse where **5 friendly helper friends** sit around a big **Chalkboard (Notice Board)**:
1. 🩺 **Leaf Doctor:** Looks at a photo of a leaf and says if it's healthy or has a plant sickness.
2. ☀️ **Weather Watcher:** Checks if it's going to be hot or rainy today (with automatic offline backup).
3. 💧 **Water Helper:** Measures the exact amount of water your plant needs using math.
4. 📈 **Harvest Guesser:** Tells you if harvest yield is likely to go **Up (+15%) 📈** or **Down (-12%) 📉**.
5. 🧑‍🌾 **Farm Advisor (The Boss):** Reads everyone's notes from the chalkboard and writes down **3 simple things for the farmer to do today**!

---

## 📁 Project Structure

```text
agrisage/
├── app.py                      # 🌟 Main Streamlit Dashboard (One page, big buttons, clean cards)
│
├── agents/                     # 👥 The 5 Helper Agents (one small Python file each)
│   ├── leaf_doctor.py          # 🩺 Leaf photo disease scanner (Healthy / Mild / Sick)
│   ├── weather_watcher.py      # ☀️ Open-Meteo weather API reader (+ offline fallback)
│   ├── water_helper.py         # 💧 Scikit-Learn regression irrigation model
│   ├── harvest_guesser.py      # 📈 Scikit-Learn Random Forest yield predictor
│   └── farm_advisor.py         # 🧑‍🌾 The Boss: combines all 4 on the Notice Board
│
├── data/
│   ├── sample_crops.csv        # 📊 Dataset for training irrigation and yield models
│   └── sample_leaves/          # 🍃 Test leaf photos for easy demo
│
├── locales/
│   ├── en.json                 # 🇬🇧 Complete English translations
│   └── te.json                 # 🇮🇳 Complete Telugu (తెలుగు) translations
│
├── create_sample_leaves.py     # 🎨 Utility to generate demo sample leaf images
├── test_agents.py              # 🧪 Automated unit tests for all 5 agents
├── requirements.txt            # 📦 Required Python packages
├── run.bat                     # ⚡ One-click Windows starter script
└── README.md                   # 📘 This documentation file
```

---

## 🚀 How To Run (In 2 Simple Steps)

### Method 1: One-Click (Windows)
Double-click the **`run.bat`** file inside the `agrisage` folder. It will install packages, generate demo leaves, and launch the dashboard automatically!

### Method 2: From Terminal / Command Prompt
1. Open your terminal and navigate to the project directory:
   ```bash
   cd c:\Users\avina\Desktop\hackathon2\agrisage
   ```

2. Install the lightweight requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Generate demo leaves:
   ```bash
   python create_sample_leaves.py
   ```

4. Launch the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 🧪 Testing the 5 Agents

We included a standalone test script that verifies each helper independently in 1 second:
```bash
python test_agents.py
```
Expected output:
```text
🌾 AGRISAGE AI - TESTING THE 5 HELPER AGENTS 🌾
1️⃣ Testing Leaf Doctor 🩺...           ✅ Passed!
2️⃣ Testing Weather Watcher ☀️...      ✅ Passed!
3️⃣ Testing Water Helper 💧...          ✅ Passed!
4️⃣ Testing Harvest Guesser 📈...       ✅ Passed!
5️⃣ Testing Farm Advisor 🧑‍🌾...         ✅ Passed!
✨ ALL 5 AGENTS TESTED AND PASSING BEAUTIFULLY! ✨
```

---

## 🇮🇳 Complete Telugu (తెలుగు) Support
- **Top Language Switcher:** Instant toggle between `English` and `తెలుగు`.
- **Zero Hardcoded Strings:** Every word lives inside `locales/en.json` and `locales/te.json`.
- **Noto Sans Telugu Font:** Integrated Google Font ensures crisp rendering of all Telugu vowels and conjuncts without missing boxes.
- **🔊 Browser Read-Aloud:** Uses the standard Web Speech API (`te-IN` voice for Telugu and `en-IN` for English) so farmers can listen to today's advice with one click.

---

## 🎓 College Viva / Presentation Q&A Guide

**Q1: How do your agents communicate?**
> *"Our agents communicate using a lightweight **Notice Board pattern** (a shared Python dictionary). Each helper has a single responsibility, writes its findings to `notice_board`, and the Farm Advisor agent reads the board to formulate the final advice. There is no complicated database or microservice overhead."*

**Q2: Which machine learning models are used?**
> *"For watering and yield prediction, we use lightweight Scikit-Learn models (`LinearRegression` and `RandomForestRegressor`) trained on realistic crop agronomy data (`sample_crops.csv`). For leaf disease detection, we use a color-metric chlorosis and necrosis analysis on leaf chlorophyll with standard agricultural remedies."*

**Q3: What happens if there is no internet during the demo?**
> *"Weather Watcher uses Open-Meteo free API when online, but contains a graceful fallback dataset that activates automatically if the network drops. The app will never crash during an exam or demo!"*

