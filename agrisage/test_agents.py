"""
AgriSage AI - Simple Unit Tests for All 5 Agents
Run this with:
    python test_agents.py
"""

import sys
from pathlib import Path
from PIL import Image
from io import BytesIO

# Add current directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from agents.leaf_doctor import LeafDoctor
from agents.weather_watcher import WeatherWatcher
from agents.water_helper import WaterHelper
from agents.harvest_guesser import HarvestGuesser
from agents.farm_advisor import FarmAdvisor

def run_tests():
    print("=" * 60)
    print("🌾 AGRISAGE AI - TESTING THE 5 HELPER AGENTS 🌾")
    print("=" * 60)

    # 1. Test Leaf Doctor
    print("\n1️⃣ Testing Leaf Doctor 🩺...")
    doctor = LeafDoctor()
    
    # 1a. Test without image
    res_no_img = doctor.diagnose(None, crop_name="Rice")
    assert res_no_img["status"] == "yellow"
    print("   ✅ No-image fallback test passed.")

    # 1b. Test with green leaf image
    img = Image.new("RGB", (64, 64), color=(34, 139, 34)) # Forest green
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    res_green = doctor.diagnose(img_bytes.getvalue(), crop_name="Rice")
    assert res_green["status"] == "green"
    print(f"   ✅ Green leaf diagnosis: {res_green['diagnosis_en']} ({res_green['diagnosis_te']})")

    # 2. Test Weather Watcher
    print("\n2️⃣ Testing Weather Watcher ☀️...")
    watcher = WeatherWatcher()
    weather_res = watcher.get_weather("Hyderabad")
    assert "temperature" in weather_res
    assert weather_res["status"] in ["green", "yellow", "red"]
    print(f"   ✅ Weather checked: {weather_res['temperature']}°C, Status: {weather_res['status']} ({weather_res['source']})")

    # 3. Test Water Helper
    print("\n3️⃣ Testing Water Helper 💧...")
    water_helper = WaterHelper()
    water_res = water_helper.calculate_water(
        crop="Rice",
        growth_stage="Growing",
        soil_type="Clay Soil",
        soil_moisture="Dry",
        temperature=weather_res["temperature"],
        rainfall_mm=weather_res["rainfall_mm"]
    )
    assert water_res["recommended_liters"] > 0
    print(f"   ✅ Recommended watering: {water_res['recommended_liters']} L/acre (Status: {water_res['status']})")

    # 4. Test Harvest Guesser
    print("\n4️⃣ Testing Harvest Guesser 📈...")
    guesser = HarvestGuesser()
    harvest_res = guesser.predict_yield(
        crop="Rice",
        growth_stage="Growing",
        soil_moisture="Normal",
        temperature=weather_res["temperature"],
        rainfall_mm=weather_res["rainfall_mm"],
        disease_status=res_green["status"],
        past_crop="Groundnut"
    )
    assert "predicted_change_pct" in harvest_res
    print(f"   ✅ Yield Prediction: {harvest_res['trend_en']} ({harvest_res['trend_te']})")

    # 5. Test Farm Advisor (The Boss)
    print("\n5️⃣ Testing Farm Advisor 🧑‍🌾 (The Boss)...")
    advisor = FarmAdvisor()
    
    # Simple shared notice board (Python dict)
    notice_board = {
        "leaf_doctor": res_green,
        "weather_watcher": weather_res,
        "water_helper": water_res,
        "harvest_guesser": harvest_res
    }

    final_advice = advisor.advise(notice_board, crop="Rice", growth_stage="Vegetative / Growing")
    assert "step1" in final_advice
    assert "step2" in final_advice
    assert "step3" in final_advice
    assert "speech_text_en" in final_advice
    assert "speech_text_te" in final_advice

    print("\n🎉 The Notice Board Summary from The Boss:")
    print(f"   • Step 1: {final_advice['step1']['title_en']}")
    print(f"   • Step 2: {final_advice['step2']['title_en']}")
    print(f"   • Step 3: {final_advice['step3']['title_en']}")
    print(f"   • Telugu Speech: {final_advice['speech_text_te'][:60]}...")

    print("\n" + "=" * 60)
    print("✨ ALL 5 AGENTS TESTED AND PASSING BEAUTIFULLY! ✨")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

