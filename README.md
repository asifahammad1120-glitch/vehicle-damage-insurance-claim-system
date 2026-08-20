# Vehicle Damage Detection & Insurance Claim Assessment System

An AI-powered web application that automates vehicle accident claim assessment. Upload an accident photo, and the system detects damaged parts, classifies each part's damage severity, and estimates a claim amount — replacing manual inspection with a YOLOv8 + CNN pipeline wrapped in a full Django web app.

Built as part of an AI/ML internship project simulating a real-world insurance claim workflow.

## How it works

1. **YOLOv8** detects and localizes damaged vehicle parts in the uploaded image (bumper, door, hood, windshield, headlight, tire), drawing a bounding box around each.
2. Each detected region is **cropped** and routed to a **dedicated CNN classifier** — one CNN per part, not a single shared model — since each part's damage patterns look completely different.
3. Each CNN classifies its crop into one of four severity levels: **No Damage / Minor / Moderate / Major**.
4. The system calculates an estimated claim amount using a **weighted per-part formula**: each part contributes a percentage of the vehicle's market price based on (a) how much of the vehicle's value that part represents, and (b) the severity detected.
5. The claim goes through a full **review workflow**: submitted by a user, routed to their selected insurance company, reviewed and approved/rejected by the company, with a downloadable PDF report.

### A design detail worth knowing

Each of the 6 CNNs was trained independently (by different people, at different times), so their output class *order* isn't guaranteed to match. Verifying this mattered: the windshield model's classes came out in a different order (`no_damage, major, minor, moderate`) than the other five (`major, minor, moderate, no_damage`) — an artifact of how its training folders were named alphabetically. The inference pipeline maps each model's output through its own explicit class order rather than assuming uniformity, which is a easy mistake to make and a hard one to catch, since it fails silently rather than throwing an error.

## Features

- **AI damage pipeline**: YOLOv8 part detection + 6 independent CNN severity classifiers
- **Weighted claim estimation**: per-part rupee breakdown, not just a single opaque total
- **Three user roles**: claimants, insurance companies, and admin — each with their own workflow
- **Insurance company onboarding**: self-registration with admin approval before a company can review claims
- **Admin vehicle management**: add/edit/delete vehicle brands, years, and market prices
- **PDF claim reports**: downloadable, generated server-side
- **Clean, responsive UI**: Bootstrap-based throughout, with a custom-designed auth flow

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Object Detection | YOLOv8 (Ultralytics) |
| Damage Classification | TensorFlow / Keras (6 CNN models) |
| Database | SQLite (dev) |
| PDF Generation | xhtml2pdf |
| Frontend | Bootstrap 5, custom CSS |
| Model Hosting | Hugging Face Hub (CNN weights, ~950MB total) |

## Screenshots

> Add screenshots to a `screenshots/` folder and reference them here, e.g.:
> `![Claim detail page](screenshots/claim-detail.png)`

Suggested screenshots to include:
- The claim submission form
- Claim detail page showing detected parts, severity badges, and per-part amounts
- Company review dashboard with Approve/Reject
- The login/signup pages

## Project structure

```
vehicle_claim_system/
├── ai_pipeline/          # YOLO + 6 CNN inference logic (model-agnostic of Django views)
│   ├── model_store/      # best.pt lives here; CNN weights downloaded via script
│   ├── inference.py       # model loading + prediction pipeline
│   ├── class_mappings.py  # per-model severity class order (see design note above)
│   └── part_weights.py    # claim calculation weights/percentages
├── claims/                # Claim submission, detail views, PDF generation
├── companies/             # Insurance company registration, approval, review dashboard
├── claim_admin/           # Admin vehicle management (CRUD)
├── users/                 # Auth (signup/login)
├── templates/             # Shared base template
├── download_models.py     # Fetches CNN weights from Hugging Face
└── requirements.txt
```

## Getting started

### Prerequisites
- Python 3.11+ (required — the CNN model files need Keras 3.13+, which requires Python 3.11+)
- A Hugging Face account is *not* required to download the models (public repo)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/asifahammad1120-glitch/vehicle-damage-insurance-claim-system.git
cd vehicle-damage-insurance-claim-system

# 2. Create and activate a virtual environment (Python 3.11+)
py -3.11 -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the CNN model weights (~950MB, hosted on Hugging Face)
python download_models.py

# 5. Set up environment variables
copy .env.example .env      # Windows
# cp .env.example .env       # macOS/Linux
# Edit .env and set a SECRET_KEY (any random string works for local dev)

# 6. Set up the database
python manage.py migrate
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

The YOLO weights (`best.pt`, ~6MB) are included directly in this repo under `ai_pipeline/model_store/` — only the 6 larger CNN files need the separate download step.

## Claim calculation methodology

Each detected part contributes to the claim amount based on:
```
part_amount = vehicle_market_price × part_weight × severity_percentage
```
Where `part_weight` is an estimated share of the vehicle's value that part represents (e.g. door ≈ 8%, headlight ≈ 2%), and `severity_percentage` follows Minor=10%, Moderate=40%, Major=70%, No Damage=0%.

**Note:** part weights are estimated for demo purposes, not real insurer repair-cost data — a production system would source these from actual repair-cost datasets.

## Known limitations

- Part weights and CNN class thresholds are estimates, not calibrated against real insurance data
- YOLO's headlight detection is the weakest-performing class (~0.77 mAP50 vs ~0.88 overall) due to limited/angled training examples
- Some CNNs show occasional overconfidence on severe damage — a common symptom of limited training data diversity per class

## Acknowledgments

Built during an AI/ML internship at Singularis Software Technologies.
