# 📊 Skill-Course Matching Streamlit App

This project is a **multi-page Streamlit application** that analyzes various datasets including course information, job postings, and other student/HR-related datasets. A key highlight is matching courses with in-demand skills from job data using preprocessed and weighted scoring techniques.

---

## 📁 Project Structure

```
.
├── Home.py                     # Landing page for Streamlit
├── app/
│   ├── core.py                 # Shared backend logic
│   └── data/                   # CSV datasets (raw + processed)
│       ├── 1_courses.csv
│       ├── 2_jobs.csv
│       ├── courses_preprocessed.csv
│       ├── jobs_preprocessed.csv
│       └── ... other datasets
├── pages/
│   ├── Task1.py - Task5.py     # Each task is a separate page in the app
├── preprocess.py               # Preprocess CSVs (skills extraction & scoring)
├── requirements.txt            # Required Python libraries
└── run_app.sh                  # Script to preprocess and run the app
```

---

## 🚀 Features

- Match courses with in-demand job skills using weighted frequency scoring
- Preprocessing of raw datasets into enriched formats (`skills_list`, `score`)
- Filter courses interactively by:
  - Partner
  - Level
  - Certificate Type
  - Credit Eligibility
  - Rating
  - Skills
- Modular, multi-page layout (`pages/TaskX.py`)

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Armaan-Indani/FDS_Project.git
cd FDS_Project/
```

### 2. Create a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Preprocess the Raw Data
This step parses `skills_list` and computes skill scores.
```bash
python preprocess.py
```

Or you can run everything in one step (preprocess + app):
```bash
./run_app.sh
```

### 5. Run the Streamlit App
```bash
streamlit run Home.py
```

---

## ✅ Requirements

Listed in `requirements.txt`. Core libraries include:
- `streamlit`
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `plotly`

---

## 📌 Notes

- Pages like `Task1.py`, `Task2.py`, etc., represent individual assignments or features.
- Place new datasets in `app/data/`.
- Preprocessing must be re-run if raw files (`1_courses.csv`, `2_jobs.csv`) are updated.

---