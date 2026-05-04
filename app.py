import streamlit as st
import pickle
import numpy as np

# ── Load model, encoder, features ──────────────────────────────────────────
with open('flood_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('flood_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

with open('flood_features.pkl', 'rb') as f:
    feature_cols = pickle.load(f)

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Flood Risk Predictor", page_icon="🌊", layout="wide")

st.title("🌊 Flood Risk Prediction System")
st.markdown("Rate each factor from **0 (Very Low)** to **10 (Very High)** to predict flood risk.")
st.markdown("---")

# ── Input fields ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌧️ Weather & Geography")
    MonsoonIntensity      = st.slider("Monsoon Intensity",               0, 10, 5)
    TopographyDrainage    = st.slider("Topography & Drainage",           0, 10, 5)
    CoastalVulnerability  = st.slider("Coastal Vulnerability",           0, 10, 5)
    Landslides            = st.slider("Landslide Risk",                  0, 10, 5)
    Watersheds            = st.slider("Watershed Condition",             0, 10, 5)

    st.subheader("🏗️ Infrastructure")
    RiverManagement             = st.slider("River Management Quality",  0, 10, 5)
    DamsQuality                 = st.slider("Dams Quality",              0, 10, 5)
    DrainageSystems             = st.slider("Drainage Systems",          0, 10, 5)
    DeterioratingInfrastructure = st.slider("Deteriorating Infrastructure", 0, 10, 5)

with col2:
    st.subheader("🌳 Environment")
    Deforestation         = st.slider("Deforestation Level",             0, 10, 5)
    Urbanization          = st.slider("Urbanization Level",              0, 10, 5)
    Siltation             = st.slider("Siltation Level",                 0, 10, 5)
    WetlandLoss           = st.slider("Wetland Loss",                    0, 10, 5)
    AgriculturalPractices = st.slider("Poor Agricultural Practices",     0, 10, 5)

    st.subheader("👥 Human Factors")
    ClimateChange                   = st.slider("Climate Change Impact",         0, 10, 5)
    Encroachments                   = st.slider("Encroachments",                 0, 10, 5)
    IneffectiveDisasterPreparedness = st.slider("Ineffective Disaster Prep",     0, 10, 5)
    PopulationScore                 = st.slider("Population Density Score",      0, 10, 5)
    InadequatePlanning              = st.slider("Inadequate Planning",           0, 10, 5)
    PoliticalFactors                = st.slider("Political Factors",             0, 10, 5)

# ── Predict button ──────────────────────────────────────────────────────────
st.markdown("---")
if st.button("🌊 Predict Flood Risk", type="primary"):

    # Must match exact training order
    input_data = np.array([[
        MonsoonIntensity, TopographyDrainage, RiverManagement,
        Deforestation, Urbanization, ClimateChange, DamsQuality,
        Siltation, AgriculturalPractices, Encroachments,
        IneffectiveDisasterPreparedness, DrainageSystems,
        CoastalVulnerability, Landslides, Watersheds,
        DeterioratingInfrastructure, PopulationScore, WetlandLoss,
        InadequatePlanning, PoliticalFactors
    ]])

    prediction  = model.predict(input_data)[0]
    risk_label  = le.inverse_transform([prediction])[0]
    proba       = model.predict_proba(input_data)[0]
    confidence  = round(max(proba) * 100, 2)

    st.markdown("---")

    # Show result
    if risk_label == "High":
        st.error(f"🚨 FLOOD RISK: HIGH  —  Confidence: {confidence}%")
        st.markdown("### ⚠️ Immediate Actions Required")
        st.write("• Alert local disaster management authority immediately")
        st.write("• Evacuate low-lying areas near rivers and coasts")
        st.write("• Stock emergency supplies (water, food, medicines)")
        st.write("• Strengthen river embankments and drainage systems")
    elif risk_label == "Medium":
        st.warning(f"⚠️ FLOOD RISK: MEDIUM  —  Confidence: {confidence}%")
        st.markdown("### 📋 Precautionary Actions")
        st.write("• Monitor weather forecasts closely")
        st.write("• Check drainage systems for blockages")
        st.write("• Keep emergency contacts ready")
        st.write("• Avoid construction in low-lying areas")
    else:
        st.success(f"✅ FLOOD RISK: LOW  —  Confidence: {confidence}%")
        st.write("Current conditions indicate low flood risk.")
        st.write("Continue regular monitoring of weather and river levels.")

    # Probability breakdown
    st.markdown("---")
    st.subheader("📊 Risk Probability Breakdown")
    for cls, prob in zip(le.classes_, proba):
        color = "🔴" if cls == "High" else "🟡" if cls == "Medium" else "🟢"
        st.progress(int(prob * 100), text=f"{color} {cls} Risk: {prob*100:.1f}%")

    # Top risk factors
    st.markdown("---")
    st.subheader("🔍 Your Top Risk Factors")
    values = {
        "Monsoon Intensity":            MonsoonIntensity,
        "Deforestation":                Deforestation,
        "Urbanization":                 Urbanization,
        "Ineffective Disaster Prep":    IneffectiveDisasterPreparedness,
        "Deteriorating Infrastructure": DeterioratingInfrastructure,
        "Inadequate Planning":          InadequatePlanning,
        "Wetland Loss":                 WetlandLoss,
        "Encroachments":                Encroachments,
    }
    top_risks = sorted(values.items(), key=lambda x: x[1], reverse=True)[:3]
    for factor, val in top_risks:
        if val >= 7:
            st.warning(f"⚠️ {factor}: {val}/10 — This is a major contributing factor")
        elif val >= 4:
            st.info(f"ℹ️ {factor}: {val}/10 — Moderate concern")
