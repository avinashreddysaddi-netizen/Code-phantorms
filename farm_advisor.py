"""
Farm Advisor Agent (🧑‍🌾 రైతు సలహాదారు - The Boss)
Job: Reads all 4 helper notes from the notice board, checks the crop growth stage,
     and creates the top 3 simple 'Do this today' action steps!
Analogy: Like the head chef in a village kitchen who tastes everything from the sous chefs
         and writes today's 3 special recipes on the chalkboard!
"""

class FarmAdvisor:
    def __init__(self):
        self.name = "Farm Advisor 🧑‍🌾 (The Boss)"

    def advise(self, notice_board: dict, crop: str, growth_stage: str) -> dict:
        """
        Reads the shared notice board dictionary and produces 3 simple action steps
        for today in both English and Telugu.
        """
        leaf_doc = notice_board.get("leaf_doctor", {})
        weather = notice_board.get("weather_watcher", {})
        water = notice_board.get("water_helper", {})
        yield_guess = notice_board.get("harvest_guesser", {})

        stage_clean = growth_stage.lower()

        # Step 1: Water Action Today
        step1_title_en = "1. Watering Action Today 💧"
        step1_title_te = "1. ఈరోజు నీటి నిర్వహణ 💧"
        step1_desc_en = f"{water.get('action_en', '')} {water.get('summary_en', '')}"
        step1_desc_te = f"{water.get('action_te', '')} {water.get('summary_te', '')}"

        # Step 2: Plant Protection & Health
        step2_title_en = "2. Plant Medicine & Spray 🌿"
        step2_title_te = "2. పంట మందులు & రక్షణ 🌿"
        step2_desc_en = f"Diagnosis: {leaf_doc.get('diagnosis_en', 'Healthy')}. Action: {leaf_doc.get('remedy_en', 'Keep regular vigil.')}"
        step2_desc_te = f"రోగ నిర్ధారణ: {leaf_doc.get('diagnosis_te', 'ఆరోగ్యంగా ఉంది')}. చేయాల్సిన పని: {leaf_doc.get('remedy_te', 'నిరంతరం పరిశీలించండి.')}"

        # Step 3: Stage-Specific Nutrient & Field Care
        step3_title_en = f"3. Care for {growth_stage} Stage 🌱"
        step3_title_te = f"3. {growth_stage} దశ పోషణ మరియు రక్షణ 🌱"

        if "seed" in stage_clean:
            step3_desc_en = "Treat seeds with Trichoderma (5g/kg) before sowing. Maintain shallow soil moisture for high germination."
            step3_desc_te = "విత్తనాలను ట్రైకోడెర్మా (5 గ్రా/కేజీ) తో విత్తనశుద్ధి చేయండి. మొలకలు బాగా రావడానికి తేలికపాటి తేమ ఉండేలా చూడండి."
        elif "growing" in stage_clean:
            step3_desc_en = "Apply top-dressing nitrogen/urea in splits. Complete manual weeding or intercultural hoeing to remove nutrient theft."
            step3_desc_te = "యూరియా మరియు నత్రజని ఎరువులను విడతలవారీగా వేయండి. కలుపు తీత పూర్తి చేసి మొక్కలకు బలం చేకూర్చండి."
        elif "flowering" in stage_clean:
            step3_desc_en = "Do not let soil dry out during flowering! Spray 13-0-45 (Potassium Nitrate @ 10g/L) to prevent flower drop."
            step3_desc_te = "పూత సమయంలో నేల ఆరిపోకుండా చూడండి! పూత రాలకుండా ఉండేందుకు 13-0-45 ఎరువును (10 గ్రా/లీ) పిచికారీ చేయండి."
        elif "harvest" in stage_clean:
            step3_desc_en = "Stop irrigation 10-14 days before harvest. Ensure clean, dry threshing floor and harvest in morning sunlight."
            step3_desc_te = "కోతకు 10-14 రోజుల ముందు నీరు పెట్టడం ఆపండి. ఉదయం వేళల్లో కోత కోసి ఎండలో ఆరబెట్టండి."
        else:
            step3_desc_en = "Apply organic compost or vermicompost around root zones to maintain soil biology."
            step3_desc_te = "మొక్కల మొదళ్ల వద్ద సేంద్రియ ఎరువు లేదా వర్మీ కంపోస్ట్ వేయండి."

        # Overall Status (Traffic Light)
        statuses = [leaf_doc.get("status", "green"), weather.get("status", "green"), 
                    water.get("status", "green"), yield_guess.get("status", "green")]
        if "red" in statuses:
            overall_status = "red"
        elif "yellow" in statuses:
            overall_status = "yellow"
        else:
            overall_status = "green"

        # Read-Aloud Voice Scripts for Web Speech API
        speech_text_en = (
            f"Hello Farmer! Here is your daily advice for {crop}. "
            f"First: {water.get('action_en', '')} "
            f"Second: For plant health, {leaf_doc.get('remedy_en', '')} "
            f"Third: For the current stage, {step3_desc_en}"
        )

        speech_text_te = (
            f"రైతు సోదరా నమస్కారం. మీ {crop} పంట కోసం ముఖ్యమైన సలహాలు. "
            f"మొదటిది: {water.get('action_te', '')} "
            f"రెండవది: {leaf_doc.get('remedy_te', '')} "
            f"మూడవది: {step3_desc_te}"
        )

        return {
            "overall_status": overall_status,
            "step1": {"title_en": step1_title_en, "title_te": step1_title_te, "desc_en": step1_desc_en, "desc_te": step1_desc_te},
            "step2": {"title_en": step2_title_en, "title_te": step2_title_te, "desc_en": step2_desc_en, "desc_te": step2_desc_te},
            "step3": {"title_en": step3_title_en, "title_te": step3_title_te, "desc_en": step3_desc_en, "desc_te": step3_desc_te},
            "speech_text_en": speech_text_en,
            "speech_text_te": speech_text_te
        }

