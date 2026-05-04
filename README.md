# 🌊 Flood Risk Prediction System

## Overview
Predicts flood risk level (Low / Medium / High) based on 20 environmental,
infrastructure and human factors using a Random Forest model.

## Folder Structure
```
flood_risk/
├── train.csv             ← place your dataset here
├── train_model.ipynb     ← run this first in Jupyter
├── app.py                ← run with streamlit
├── requirements.txt
│
│   (created after running notebook)
├── flood_model.pkl
├── flood_encoder.pkl
└── flood_features.pkl
```

## How to Run

### Step 1 — Train Model (Jupyter Notebook)
```
1. Place train.csv in this folder
2. Open train_model.ipynb
3. Run all cells (Shift + Enter)
4. You will see 3 .pkl files created
```

### Step 2 — Run Streamlit App
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
Kaggle 2024 Flood Prediction Competition
- 1.1 million rows
- 20 features (all integer scores 0-10)
- Target: FloodProbability (converted to Low/Medium/High)

## Future Upgrades
- Add time series forecasting for seasonal flood prediction
- Integrate real-time rainfall API
- Add India district-wise map visualization
- Add NLP for flood news analysis
