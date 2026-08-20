"""
Downloads the 6 CNN model weight files from Hugging Face into
ai_pipeline/models_store/. Run this once after cloning the repo.

Usage: python download_models.py
"""
from huggingface_hub import hf_hub_download
import shutil
import os

REPO_ID = "asif1120/vehicle-damage-cnn-models"
DEST_DIR = os.path.join("ai_pipeline", "model_store")

FILES = [
    "door_damage_cnn.keras",
    "headlight_damage_classifierfinal.keras",
    "hooduuuu_cnn_89.h5",
    "tire_damage2.keras",
    "vehicle_damage_modelbumper.keras",
    "windsheild.keras",
]

os.makedirs(DEST_DIR, exist_ok=True)

for filename in FILES:
    print(f"Downloading {filename}...")
    downloaded_path = hf_hub_download(repo_id=REPO_ID, filename=filename)
    dest_path = os.path.join(DEST_DIR, filename)
    shutil.copy(downloaded_path, dest_path)
    print(f"  -> saved to {dest_path}")

print("\nAll CNN models downloaded. Make sure best.pt is also in ai_pipeline/models_store/.")