import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model/housing_model.pkl")

st.set_page_config(page_title="House Price Predictor", page_icon="🏠")
st.title("🏠 House Price Prediction App")
st.write("Fill in the property details below to get an estimated price.")

# --- Input Form ---
col1, col2 = st.columns(2)

with col1:
    bed = st.number_input("🛏 Bedrooms", min_value=1, max_value=50, value=3)
    bath = st.number_input("🚿 Bathrooms", min_value=1, max_value=50, value=2)
    house_size = st.number_input("📐 House Size (sq ft)", min_value=100.0, max_value=50000.0, value=1500.0, step=50.0)
    acre_lot = st.number_input("🌿 Lot Size (acres)", min_value=0.0, max_value=1000.0, value=0.5, step=0.1)

with col2:
    status = st.selectbox("📋 Property Status", ["for_sale", "ready_to_build", "sold"])
    state = st.selectbox("🗺 State", [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
        'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
        'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Brunswick', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
        'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ])
    city = st.text_input("🏙 City", value="New York")
    zip_code = st.number_input("📮 Zip Code", min_value=0, max_value=99999, value=10001)

st.divider()

# These are numeric IDs in the dataset — use defaults (median-like values)
brokered_by = st.number_input("🏢 Brokered By (Agent ID)", min_value=0.0, value=50000.0, step=1.0)
street = st.number_input("🏘 Street ID", min_value=0.0, value=1000000.0, step=1.0)

# --- Predict ---
if st.button("💰 Predict Price", use_container_width=True):
    input_data = pd.DataFrame([{
        "brokered_by": brokered_by,
        "status": status,
        "bed": bed,
        "bath": bath,
        "acre_lot": acre_lot,
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "house_size": house_size
    }])

    try:
        prediction = model.predict(input_data)
        st.success(f"### 💵 Estimated Price: ${prediction[0]:,.2f}")
        st.balloons()
    except Exception as e:
        st.error(f"Prediction error: {e}")