import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="AgriSage AI - Smart Farming Helper",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Base Directory & Translations Loader
BASE_DIR = Path(__file__).resolve().parent
LOCALES_DIR = BASE_DIR / "locales"
DATA_DIR = BASE_DIR / "data"

# Import our 5 Helper Agents
from agents.leaf_doctor import LeafDoctor
from agents.weather_watcher import WeatherWatcher
from agents.water_helper import WaterHelper
from agents.harvest_guesser import HarvestGuesser
from agents.farm_advisor import FarmAdvisor

@st.cache_data
def load_translations():
    """Reads language files once and caches them for lightning-fast switching."""
    with open(LOCALES_DIR / "en.json", "r", encoding="utf-8") as f:
        en = json.load(f)
    with open(LOCALES_DIR / "te.json", "r", encoding="utf-8") as f:
        te = json.load(f)
    return {"English": en, "తెలుగు": te}

translations = load_translations()

@st.cache_resource
def get_agents():
    """Initializes our 5 helper agents once."""
    return {
        "doctor": LeafDoctor(),
        "weather": WeatherWatcher(),
        "water": WaterHelper(),
        "guesser": HarvestGuesser(),
        "advisor": FarmAdvisor()
    }

agents = get_agents()

# 3. Session State Initialization
if "lang" not in st.session_state:
    st.session_state.lang = "English"

if "notice_board" not in st.session_state:
    st.session_state.notice_board = None

if "play_audio_trigger" not in st.session_state:
    st.session_state.play_audio_trigger = 0

# 4. Inject Noto Sans Telugu Font & Child-Friendly Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;600;700&family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], font, div, span, p, h1, h2, h3, h4, h5, h6, button, label {
        font-family: 'Nunito', 'Noto Sans Telugu', sans-serif !important;
    }
    
    .top-banner {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 2px solid #81c784;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
        color: #1b5e20;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .agent-card {
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        text-align: center;
        height: 100%;
    }
    .agent-avatar {
        font-size: 2.6rem;
        margin-bottom: 6px;
    }
    .agent-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #2e7d32;
        margin-bottom: 4px;
    }
    .agent-role {
        font-size: 0.85rem;
        color: #555;
        line-height: 1.3;
    }

    /* Notice Board Note Cards */
    .notice-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 16px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
        min-height: 220px;
    }
    .notice-card-header {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Traffic Light Badges */
    .badge-green {
        background-color: #28a745;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .badge-yellow {
        background-color: #ffc107;
        color: #212529;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .badge-red {
        background-color: #dc3545;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }

    /* Step Action Cards */
    .step-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px;
        border-left: 6px solid #2e7d32;
        box-shadow: 0 3px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    .step-card-red {
        border-left: 6px solid #dc3545;
    }
    .step-card-yellow {
        border-left: 6px solid #ffc107;
    }
    .step-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1b5e20;
        margin-bottom: 6px;
    }
    .step-desc {
        font-size: 1.0rem;
        color: #333333;
        line-height: 1.45;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 5. Language Selector
header_col1, header_col2 = st.columns([3, 1])

with header_col2:
    selected_lang = st.radio(
        label="🌐 Language / భాష",
        options=["English", "తెలుగు"],
        index=0 if st.session_state.lang == "English" else 1,
        horizontal=True,
        key="lang_toggle"
    )
    st.session_state.lang = selected_lang

t = translations[st.session_state.lang]

def tr(key: str, default: str = "") -> str:
    return t.get(key, default or key)

with header_col1:
    st.title(tr("app_title"))
    st.caption(f"✨ {tr('app_tagline')}")

st.markdown(f'<div class="top-banner">{tr("welcome_banner")}</div>', unsafe_allow_html=True)

# 6. Meet The 5 Helper Friends (Overview Cards)
st.subheader(f"👥 {tr('agent_title')}")
st.write(tr("agent_subtitle"))

col1, col2, col3, col4, col5 = st.columns(5)
agents_meta = [
    {"emoji": "🩺", "name_key": "agent_1_name", "role_key": "agent_1_role"},
    {"emoji": "☀️", "name_key": "agent_2_name", "role_key": "agent_2_role"},
    {"emoji": "💧", "name_key": "agent_3_name", "role_key": "agent_3_role"},
    {"emoji": "📈", "name_key": "agent_4_name", "role_key": "agent_4_role"},
    {"emoji": "🧑‍🌾", "name_key": "agent_5_name", "role_key": "agent_5_role"},
]

for col, meta in zip([col1, col2, col3, col4, col5], agents_meta):
    with col:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-avatar">{meta["emoji"]}</div>
                <div class="agent-name">{tr(meta["name_key"])}</div>
                <div class="agent-role">{tr(meta["role_key"])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

# 7. Step 1: Farmer Input Form
st.subheader(tr("inputs_header"))

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    crop_options = ["Rice", "Cotton", "Chilli", "Maize", "Groundnut", "Tomato"]
    selected_crop = st.selectbox(
        tr("crop_label"), 
        options=crop_options,
        format_func=lambda x: f"{x} ({tr('crop_' + x.lower())})"
    )
    
    stage_options = ["Seed", "Growing", "Flowering", "Harvest"]
    selected_stage = st.selectbox(
        tr("growth_stage_label"), 
        options=stage_options,
        format_func=lambda x: tr(f"stage_{x.lower()}")
    )

with input_col2:
    soil_options = ["Red", "Black", "Sandy", "Clay"]
    selected_soil = st.selectbox(
        tr("soil_type_label"), 
        options=soil_options,
        format_func=lambda x: tr(f"soil_{x.lower()}")
    )
    
    moisture_options = ["Dry", "Normal", "Wet"]
    selected_moisture = st.selectbox(
        tr("soil_moisture_label"), 
        options=moisture_options,
        format_func=lambda x: tr(f"moisture_{x.lower()}")
    )

with input_col3:
    city_input = st.text_input(tr("city_label"), value="Hyderabad")
    past_crops = ["None", "Groundnut", "Rice"]
    selected_past_crop = st.selectbox(
        tr("past_crop_label"),
        options=past_crops,
        format_func=lambda x: tr(f"past_crop_{x.lower()}")
    )

# Leaf Photo Options: Upload or Quick Test Leaves
st.markdown(f"<b>🌱 {tr('leaf_photo_label')}</b>", unsafe_allow_html=True)
leaf_source_choice = st.radio(
    label=tr("sample_leaf_label"),
    options=["sample_healthy", "sample_sick", "custom_upload"],
    format_func=lambda x: tr(f"sample_leaf_{x.replace('sample_', '') if 'sample_' in x else 'custom'}"),
    horizontal=True,
    key="leaf_choice_radio"
)

active_leaf_image = None
sample_dir = DATA_DIR / "sample_leaves"

if leaf_source_choice == "custom_upload":
    uploaded_leaf = st.file_uploader(tr("leaf_photo_label"), type=["jpg", "jpeg", "png"])
    if uploaded_leaf is not None:
        active_leaf_image = uploaded_leaf
        st.image(uploaded_leaf, caption="📷 Uploaded Leaf Preview", width=180)
elif leaf_source_choice == "sample_healthy":
    healthy_path = sample_dir / "healthy_leaf.png"
    if healthy_path.exists():
        active_leaf_image = healthy_path.read_bytes()
        st.image(healthy_path, caption="🟢 Healthy Leaf Sample", width=180)
elif leaf_source_choice == "sample_sick":
    sick_path = sample_dir / "sick_leaf.png"
    if sick_path.exists():
        active_leaf_image = sick_path.read_bytes()
        st.image(sick_path, caption="🔴 Diseased Leaf Sample", width=180)

submit_clicked = st.button(tr("btn_submit"), type="primary", use_container_width=True)

# 8. Step 4 Execution: Connecting Agents on the Shared Notice Board
if submit_clicked:
    with st.spinner(tr("loading_message")):
        notice_board = {}

        # 1. Weather Watcher
        notice_board["weather_watcher"] = agents["weather"].get_weather(city_name=city_input)

        # 2. Leaf Doctor
        notice_board["leaf_doctor"] = agents["doctor"].diagnose(
            image_input=active_leaf_image,
            crop_name=selected_crop
        )

        # 3. Water Helper
        notice_board["water_helper"] = agents["water"].calculate_water(
            crop=selected_crop,
            growth_stage=selected_stage,
            soil_type=selected_soil,
            soil_moisture=selected_moisture,
            temperature=notice_board["weather_watcher"]["temperature"],
            rainfall_mm=notice_board["weather_watcher"]["rainfall_mm"]
        )

        # 4. Harvest Guesser
        notice_board["harvest_guesser"] = agents["guesser"].predict_yield(
            crop=selected_crop,
            growth_stage=selected_stage,
            soil_moisture=selected_moisture,
            temperature=notice_board["weather_watcher"]["temperature"],
            rainfall_mm=notice_board["weather_watcher"]["rainfall_mm"],
            disease_status=notice_board["leaf_doctor"]["status"],
            past_crop=selected_past_crop
        )

        # 5. Farm Advisor (The Boss)
        notice_board["farm_advisor"] = agents["advisor"].advise(
            notice_board=notice_board,
            crop=selected_crop,
            growth_stage=selected_stage
        )

        st.session_state.notice_board = notice_board

# 9. Render Notice Board & Final Advice
st.divider()

if st.session_state.notice_board is None:
    st.info(f"💡 {tr('prompt_action')}")
else:
    nb = st.session_state.notice_board
    is_te = (st.session_state.lang == "తెలుగు")

    st.subheader(tr("results_header"))

    # Display 4 Helper Notes on the Notice Board
    n_col1, n_col2, n_col3, n_col4 = st.columns(4)

    # Note 1: Leaf Doctor
    with n_col1:
        doc = nb["leaf_doctor"]
        b_class = f"badge-{doc['status']}"
        st.markdown(
            f"""
            <div class="notice-card">
                <div class="notice-card-header">
                    <span>🩺 {tr('agent_1_name')}</span>
                    <span class="{b_class}">● {doc['status'].upper()}</span>
                </div>
                <p><b>{doc['diagnosis_te'] if is_te else doc['diagnosis_en']}</b></p>
                <p style="font-size:0.9rem; color:#444;">{doc['details_te'] if is_te else doc['details_en']}</p>
                <hr style="margin: 8px 0;"/>
                <p style="font-size:0.85rem; color:#2e7d32;"><b>💡 {doc['remedy_te'] if is_te else doc['remedy_en']}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Note 2: Weather Watcher
    with n_col2:
        wea = nb["weather_watcher"]
        b_class = f"badge-{wea['status']}"
        st.markdown(
            f"""
            <div class="notice-card">
                <div class="notice-card-header">
                    <span>☀️ {tr('agent_2_name')}</span>
                    <span class="{b_class}">● {wea['status'].upper()}</span>
                </div>
                <p><b>{wea['summary_te'] if is_te else wea['summary_en']}</b></p>
                <p style="font-size:0.9rem; color:#444;">
                    🌡️ {wea['temperature']}°C &nbsp;|&nbsp; 💧 {wea['humidity']}%<br/>
                    🌧️ {wea['rainfall_mm']} mm Rain &nbsp;|&nbsp; 💨 {wea['wind_speed']} km/h
                </p>
                <hr style="margin: 8px 0;"/>
                <p style="font-size:0.85rem; color:#2e7d32;"><b>💡 {wea['advice_te'] if is_te else wea['advice_en']}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Note 3: Water Helper
    with n_col3:
        wat = nb["water_helper"]
        b_class = f"badge-{wat['status']}"
        st.markdown(
            f"""
            <div class="notice-card">
                <div class="notice-card-header">
                    <span>💧 {tr('agent_3_name')}</span>
                    <span class="{b_class}">● {wat['status'].upper()}</span>
                </div>
                <p><b>{wat['summary_te'] if is_te else wat['summary_en']}</b></p>
                <p style="font-size:0.9rem; color:#444;">{wat['action_te'] if is_te else wat['action_en']}</p>
                <hr style="margin: 8px 0;"/>
                <p style="font-size:0.85rem; color:#2e7d32;"><b>🎯 {wat['recommended_liters']} L / acre</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Note 4: Harvest Guesser
    with n_col4:
        har = nb["harvest_guesser"]
        b_class = f"badge-{har['status']}"
        st.markdown(
            f"""
            <div class="notice-card">
                <div class="notice-card-header">
                    <span>📈 {tr('agent_4_name')}</span>
                    <span class="{b_class}">● {har['status'].upper()}</span>
                </div>
                <p><b>{har['trend_te'] if is_te else har['trend_en']}</b></p>
                <p style="font-size:0.9rem; color:#444;">{har['reason_te'] if is_te else har['reason_en']}</p>
                <hr style="margin: 8px 0;"/>
                <p style="font-size:0.85rem; color:#2e7d32;"><b>📊 Expected Change: {har['predicted_change_pct']}%</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # The Boss Card: Top 3 Action Steps from Farm Advisor
    adv = nb["farm_advisor"]
    st.markdown("<br/>", unsafe_allow_html=True)
    
    advice_header_col1, advice_header_col2 = st.columns([2, 1])
    with advice_header_col1:
        st.subheader(f"🧑‍🌾 {tr('advice_header')}")

    # Web Speech API Browser Voice Synthesizer
    speech_text = adv["speech_text_te"] if is_te else adv["speech_text_en"]
    voice_lang = "te-IN" if is_te else "en-IN"

    # Clean escaped text for safe JS string passing
    escaped_speech = json.dumps(speech_text)

    # Render Browser Speech Buttons via Web Speech API
    components.html(
        f"""
        <div style="font-family: sans-serif; display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
            <button id="btnPlay" onclick="speakAdvice()" style="
                background-color: #2e7d32;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                🔊 {tr('btn_read_aloud')}
            </button>
            <button id="btnStop" onclick="stopAdvice()" style="
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.15);
            ">
                ⏹️ {tr('btn_stop_audio')}
            </button>
            <span id="speechStatus" style="font-size: 13px; color: #555; margin-left: 6px;"></span>
        </div>

        <script>
        function speakAdvice() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const text = {escaped_speech};
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = '{voice_lang}';
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                
                document.getElementById('speechStatus').innerText = "🔊 Speaking...";
                
                utterance.onend = function() {{
                    document.getElementById('speechStatus').innerText = "";
                }};
                utterance.onerror = function() {{
                    document.getElementById('speechStatus').innerText = "";
                }};

                window.speechSynthesis.speak(utterance);
            }} else {{
                alert("Speech synthesis is not supported in this browser.");
            }}
        }}

        function stopAdvice() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                document.getElementById('speechStatus').innerText = "";
            }}
        }}
        </script>
        """,
        height=60
    )

    # Render The 3 Action Cards
    steps = [adv["step1"], adv["step2"], adv["step3"]]
    overall_badge_class = f"step-card-{adv.get('overall_status', 'green')}"
    for s in steps:
        title = s["title_te"] if is_te else s["title_en"]
        desc = s["desc_te"] if is_te else s["desc_en"]
        st.markdown(
            f"""
            <div class="step-card {overall_badge_class}">
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Notice Board Raw JSON View (Great for Viva/Evaluation)
    with st.expander(tr("raw_json_view")):
        st.json(nb)
