import os
import json
import joblib
import torch
import torch.nn as nn
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Neural Network
class SentinelMultiTargetMLP(nn.Module):
    def __init__(self, num_bacteria_classes, embedding_dim, num_clinical_features, num_targets):
        super(SentinelMultiTargetMLP, self).__init__()
        self.bacteria_embedding = nn.Embedding(num_embeddings=num_bacteria_classes, embedding_dim=embedding_dim)
        
        input_dim = embedding_dim + num_clinical_features
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            
            nn.Linear(128, num_targets)
        )

    def forward(self, clinical_features, bacteria_idx):
        embedded_bacteria = self.bacteria_embedding(bacteria_idx)
        combined_features = torch.cat([clinical_features, embedded_bacteria], dim=1)
        return self.network(combined_features)

# Model Loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_DIR = os.path.join(BASE_DIR, "weights")

def load_json(filename):
    with open(os.path.join(WEIGHTS_DIR, filename), 'r') as f:
        return json.load(f)

print("\n[ML Subsystem] Loading Sentinel-GNN Production Artifacts...")

dataset_meta = load_json("dataset_metadata.json")
BACTERIA_MAP = load_json("bacteria_mapping.json")
FEATURE_COLS = load_json("feature_columns.json")
TARGET_COLS = load_json("target_columns.json")

scaler = joblib.load(os.path.join(WEIGHTS_DIR, "clinical_scaler.pkl"))
infection_imputer = joblib.load(os.path.join(WEIGHTS_DIR, "infection_imputer.pkl"))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SentinelMultiTargetMLP(
    num_bacteria_classes=dataset_meta.get("num_bacteria_classes", 19),
    embedding_dim=dataset_meta.get("embedding_dim", 8),
    num_clinical_features=len(FEATURE_COLS),
    num_targets=len(TARGET_COLS)
).to(device)

model.load_state_dict(torch.load(os.path.join(WEIGHTS_DIR, "best_model.pth"), map_location=device))
model.eval()

print("[ML Subsystem] Artifacts successfully loaded and model is in EVAL mode.")

# Inference
def run_mlp_inference(patient_profile: dict, isolate_id: str) -> dict:
    try:
        raw_freq = patient_profile.get("Infection_Freq", None)
        if raw_freq is None or str(raw_freq).strip() == "":
            raw_freq = np.nan

        freq_imputed = infection_imputer.transform([[float(raw_freq)]])[0][0]

        feature_dict = {
            "Age": float(patient_profile.get("Age", 50.0)),
            "Gender": float(patient_profile.get("Gender", 0.0)),
            "Diabetes": float(patient_profile.get("Diabetes", 0.0)),
            "Hypertension": float(patient_profile.get("Hypertension", 0.0)),
            "Hospital_before": float(patient_profile.get("Hospital_before", 0.0)),
            "Infection_Freq": float(freq_imputed)
        }

        raw_clinical_array = np.array([[feature_dict[col] for col in FEATURE_COLS]])

        scaled_clinical_array = scaler.transform(raw_clinical_array)

        clinical_tensor = torch.tensor(scaled_clinical_array, dtype=torch.float32).to(device)

        bacteria_int = BACTERIA_MAP.get(isolate_id.strip(), 0)
        bacteria_tensor = torch.tensor([bacteria_int], dtype=torch.long).to(device)

        with torch.no_grad():
            logits = model(clinical_tensor, bacteria_tensor)
            probabilities = torch.sigmoid(logits)[0].cpu().numpy()

        results = {}
        for i, drug_name in enumerate(TARGET_COLS):
            prob = float(probabilities[i])
            is_resistant = bool(prob >= 0.5)

            results[drug_name.upper()] = {
                "is_resistant": is_resistant,
                "confidence": prob
            }

        return results

    except Exception as e:
        logger.error(f"ML Inference Error: {str(e)}")
        return {drug.upper(): {"is_resistant": True, "confidence": 1.0} for drug in TARGET_COLS}