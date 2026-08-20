import os
import numpy as np
import keras
from ultralytics import YOLO
from PIL import Image

from .class_mappings import CLASS_ORDER, YOLO_LABEL_TO_PART_KEY

MODELS_DIR = os.path.join(os.path.dirname(__file__), "model_store")

CNN_FILENAMES = {
    "bumper": "vehicle_damage_modelbumper.keras",
    "tire": "tire_damage2.keras",
    "headlight": "headlight_damage_classifierfinal.keras",
    "door": "door_damage_cnn.keras",
    "hood": "hooduuuu_cnn_89.h5",
    "windshield": "windsheild.keras",
}

# Module-level cache - populated once, reused across every request.
_yolo_model = None
_cnn_models = {}


def load_models():
    """Load YOLO + all 6 CNNs into memory once. Call this at Django startup."""
    global _yolo_model, _cnn_models

    if _yolo_model is None:
        _yolo_model = YOLO(os.path.join(MODELS_DIR, "best.pt"))

    for part_key, filename in CNN_FILENAMES.items():
        if part_key not in _cnn_models:
            _cnn_models[part_key] = keras.models.load_model(
                os.path.join(MODELS_DIR, filename)
            )


def _classify_crop(part_key, crop_img):
    """Run one cropped part image through its matching CNN, return (severity, confidence)."""
    model = _cnn_models[part_key]

    img = crop_img.resize((224, 224))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)

    pred = model.predict(arr, verbose=0)[0]
    top_index = int(np.argmax(pred))

    severity = CLASS_ORDER[part_key][top_index]
    confidence = float(pred[top_index])
    return severity, confidence


def run_pipeline(image_path):
    """
    Full pipeline: YOLO detects parts -> crop each -> classify with matching CNN.
    Returns a list of dicts, one per detected part.
    """
    if _yolo_model is None:
        load_models()

    results = _yolo_model(image_path)[0]
    original_image = Image.open(image_path).convert("RGB")

    detections = []

    for box in results.boxes:
        yolo_label = results.names[int(box.cls[0])]
        part_key = YOLO_LABEL_TO_PART_KEY.get(yolo_label)

        if part_key is None:
            # YOLO detected something we don't have a CNN for - skip safely
            continue

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        yolo_confidence = float(box.conf[0])

        crop = original_image.crop((x1, y1, x2, y2))
        severity, severity_confidence = _classify_crop(part_key, crop)

        detections.append({
            "part_name": part_key,
            "yolo_confidence": yolo_confidence,
            "severity": severity,
            "severity_confidence": severity_confidence,
            "bbox": (x1, y1, x2, y2),
        })

    return detections