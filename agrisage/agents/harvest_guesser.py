"""
Harvest Guesser Agent (📈 దిగుబడి అంచనాదారు)
Job: Predicts if crop harvest will go Up or Down using a simple scikit-learn model.
Analogy: Like an experienced grandmother who glances at the field and smiles: 'This year we will fill all grain sacks!'
"""

from pathlib import Path
import pandas as pd
import numpy as np

class HarvestGuesser:
    def __init__(self, data_path: Path = None):
        self.name = "Harvest Guesser 📈"
        if data_path is None:
            self.data_path = Path(__file__).resolve().parent.parent / "data" / "sample_crops.csv"
        else:
            self.data_path = data_path
        
        self.model = None
        self._train_simple_model()

    def _train_simple_model(self):
        """Trains a simple Random Forest or Linear model on the sample crops CSV."""
        try:
            from sklearn.ensemble import RandomForestRegressor

            if self.data_path.exists():
                df = pd.read_csv(self.data_path)
                moisture_map = {"Dry": 1, "Normal": 2, "Wet": 3}
                df["moisture_val"] = df["soil_moisture"].map(moisture_map).fillna(2)

                X = df[["temperature", "rainfall_mm", "moisture_val"]]
                y = df["yield_change_pct"]

                self.model = RandomForestRegressor(n_estimators=10, random_state=42)
                self.model.fit(X, y)
        except Exception:
            self.model = None

    def predict_yield(self, crop: str, growth_stage: str, soil_moisture: str, 
                      temperature: float = 30.0, rainfall_mm: float = 0.0, 
                      disease_status: str = "green", past_crop: str = "") -> dict:
        """
        Estimates yield percentage increase or decrease (+15% or -10%) and gives traffic light status.
        """
        # Base model prediction
        moisture_num = 1 if "dry" in soil_moisture.lower() else (3 if "wet" in soil_moisture.lower() else 2)
        base_change = 5.0

        if self.model is not None:
            try:
                features = np.array([[temperature, rainfall_mm, moisture_num]])
                base_change = float(self.model.predict(features)[0])
            except Exception:
                base_change = 5.0

        # Penalize or reward based on plant health from Leaf Doctor
        if disease_status == "red":
            base_change -= 18.0  # Disease outbreak causes yield loss
        elif disease_status == "yellow":
            base_change -= 6.0   # Mild deficiency
        else:
            base_change += 4.0   # Healthy leaves boost photosynthesis

        # Crop rotation bonus (e.g. legumes/groundnut followed by rice/cotton improves soil)
        if past_crop and "groundnut" in past_crop.lower():
            base_change += 5.0  # Nitrogen fixation benefit

        yield_pct = round(base_change, 1)

        # Classify Status
        if yield_pct >= 5.0:
            status = "green"
            trend_en = f"Yield Likely Up (+{yield_pct}%) 📈"
            trend_te = f"దిగుబడి పెరిగే అవకాశం (+{yield_pct}%) 📈"
            reason_en = "Healthy plant condition, favorable moisture, and good crop rotation support high yields."
            reason_te = "ఆరోగ్యకరమైన మొక్క, సరైన తేమ మరియు నేల బలం వలన అధిక దిగుబడి వచ్చే అవకాశం ఉంది."
        elif yield_pct >= -5.0:
            status = "yellow"
            trend_en = f"Yield Stable ({yield_pct}%) 📊"
            trend_te = f"దిగుబడి సాధారణంగా ఉంటుంది ({yield_pct}%) 📊"
            reason_en = "Average harvest expected. Timely fertilizer and weeding can boost results further."
            reason_te = "దిగుబడి సాధారణంగా ఉంటుంది. సమయానికి ఎరువులు మరియు కలుపు నివారణ చేపడితే దిగుబడి పెరుగుతుంది."
        else:
            status = "red"
            trend_en = f"Yield May Drop ({yield_pct}%) 📉"
            trend_te = f"దిగుబడి తగ్గే ప్రమాదం ({yield_pct}%) 📉"
            reason_en = "Disease stress or improper moisture could reduce harvest. Immediate corrective care needed!"
            reason_te = "తెగులు లేదా నీటి అసమతుల్యత వల్ల దిగుబడి తగ్గే ప్రమాదం ఉంది. వెంటనే తగిన చర్యలు చేపట్టండి!"

        return {
            "status": status,
            "predicted_change_pct": yield_pct,
            "trend_en": trend_en,
            "trend_te": trend_te,
            "reason_en": reason_en,
            "reason_te": reason_te
        }

