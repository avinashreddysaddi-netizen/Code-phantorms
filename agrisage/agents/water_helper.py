"""
Water Helper Agent (💧 నీటి సహాయకుడు)
Job: Decides how much water your crop needs based on soil moisture and weather.
Algorithm: Simple Scikit-Learn Regression on sample_crops.csv with safe fallback.
Analogy: Like a careful mother measuring the exact right amount of milk for a baby's bottle!
"""

from pathlib import Path
import pandas as pd
import numpy as np

class WaterHelper:
    def __init__(self, data_path: Path = None):
        self.name = "Water Helper 💧"
        if data_path is None:
            self.data_path = Path(__file__).resolve().parent.parent / "data" / "sample_crops.csv"
        else:
            self.data_path = data_path
        
        self.model = None
        self._train_simple_model()

    def _train_simple_model(self):
        """Trains a lightweight scikit-learn Linear Regression model."""
        try:
            from sklearn.linear_model import LinearRegression

            if self.data_path.exists():
                df = pd.read_csv(self.data_path)
                
                # Map categorical values to simple numbers
                moisture_map = {"Dry": 1, "Normal": 2, "Wet": 3}
                df["moisture_val"] = df["soil_moisture"].map(moisture_map).fillna(2)
                
                X = df[["temperature", "rainfall_mm", "moisture_val"]]
                y = df["water_needed_liters"]

                self.model = LinearRegression()
                self.model.fit(X, y)
        except Exception:
            self.model = None

    def calculate_water(self, crop: str, growth_stage: str, soil_type: str, 
                        soil_moisture: str, temperature: float = 30.0, rainfall_mm: float = 0.0) -> dict:
        """
        Calculates recommended watering in liters per acre and delivers traffic-light advice.
        """
        # 1. Base estimation using simple ML model or rule calculation
        moisture_num = 1 if "dry" in soil_moisture.lower() else (3 if "wet" in soil_moisture.lower() else 2)
        
        predicted_liters = 2000.0
        if self.model is not None:
            try:
                features = np.array([[temperature, rainfall_mm, moisture_num]])
                predicted_liters = float(self.model.predict(features)[0])
            except Exception:
                predicted_liters = 2000.0
        
        # Adjust based on soil type
        soil_lower = soil_type.lower()
        if "sandy" in soil_lower:
            predicted_liters *= 1.15  # Sandy soil drains quickly
        elif "clay" in soil_lower:
            predicted_liters *= 0.90  # Clay soil retains water

        # Stage adjustment
        stage_lower = growth_stage.lower()
        if "flowering" in stage_lower:
            predicted_liters *= 1.25  # Flowering requires high hydration
        elif "harvest" in stage_lower:
            predicted_liters *= 0.40  # Less water near harvest

        # Rainfall deduction
        if rainfall_mm > 5.0:
            predicted_liters = max(0.0, predicted_liters - (rainfall_mm * 150))

        liters_rounded = int(max(200, min(5000, round(predicted_liters, -1))))

        # Determine Traffic Light Status
        if "wet" in soil_moisture.lower() or rainfall_mm > 15.0:
            status = "red"
            advice_en = "Soil is already very wet! Stop watering immediately to prevent root rot."
            advice_te = "నేలలో తేమ చాలా ఎక్కువగా ఉంది! వేరుకుళ్లు రాకుండా ఉండడానికి నీరు పెట్టడం వెంటనే ఆపండి."
            rec_en = f"Give {liters_rounded} L/acre only after 2-3 sunny days."
            rec_te = f"2-3 రోజులు ఎండ వచ్చిన తర్వాత మాత్రమే ఎకరానికి {liters_rounded} లీటర్ల నీరు పెట్టండి."
        elif "dry" in soil_moisture.lower() or temperature > 34.0:
            status = "yellow"
            advice_en = f"Soil is dry and heat is high. Deep watering recommended."
            advice_te = f"నేల పొడిగా ఉంది మరియు వేడి ఎక్కువగా ఉంది. లోతుగా నీరు పెట్టడం మంచిది."
            rec_en = f"Give ~{liters_rounded} L/acre early morning or drip irrigation."
            rec_te = f"ఎకరానికి సుమారు {liters_rounded} లీటర్లు ఉదయాన్నే లేదా డ్రిప్ ద్వారా పెట్టండి."
        else:
            status = "green"
            advice_en = "Soil moisture is ideal. Continue regular scheduled irrigation."
            advice_te = "నేలలో తేమ చాలా బాగుంది. సాధారణ పద్ధతిలో నీరు పెట్టండి."
            rec_en = f"Give maintenance watering of ~{liters_rounded} L/acre."
            rec_te = f"సాధారణ రక్షణ కొరకు ఎకరానికి సుమారు {liters_rounded} లీటర్ల నీరు ఇవ్వండి."

        return {
            "status": status,
            "recommended_liters": liters_rounded,
            "soil_moisture": soil_moisture,
            "summary_en": rec_en,
            "summary_te": rec_te,
            "action_en": advice_en,
            "action_te": advice_te
        }

