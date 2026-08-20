from ai_pipeline.part_weights import PART_WEIGHT, SEVERITY_PERCENT


def calculate_claim_amount(market_price, detections):
    total = 0.0
    for det in detections:
        part = det["part_name"]
        severity = det["severity"]
        weight = PART_WEIGHT.get(part, 0.0)
        percent = SEVERITY_PERCENT.get(severity, 0.0)
        total += float(market_price) * weight * percent
    return round(total, 2)


def annotate_detection_amounts(detections, market_price):
    """
    Attaches a .amount attribute to each DamageDetection (or dict) so
    templates can show a per-part rupee breakdown, not just the total.
    """
    for d in detections:
        part = d.part_name if hasattr(d, "part_name") else d["part_name"]
        severity = d.severity if hasattr(d, "severity") else d["severity"]

        weight = PART_WEIGHT.get(part, 0.0)
        percent = SEVERITY_PERCENT.get(severity, 0.0)
        amount = round(float(market_price) * weight * percent, 2)

        if hasattr(d, "part_name"):
            d.amount = amount
        else:
            d["amount"] = amount

    return detections