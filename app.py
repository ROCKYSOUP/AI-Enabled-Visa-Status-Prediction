import pandas as pd
import joblib
import streamlit as st
from datetime import timedelta

# -----------------------------
# Load model
# -----------------------------

model = joblib.load(r"C:\Users\agarw\OneDrive\Desktop\Infosys\models\visa_model.pkl")
model_columns = model.feature_names_in_

# -----------------------------
# Known categories
# -----------------------------

KNOWN_COUNTRIES = ["INDIA", "USA", "UK"]
KNOWN_VISA_TYPES = ["STUDENT", "WORK", "TOURIST"]

# -----------------------------
# Preprocessing
# -----------------------------

def preprocess_input(data):

    df = pd.DataFrame([data])

    # Convert date
    df["application_date"] = pd.to_datetime(df["application_date"])

    # Feature engineering (month)
    df["month"] = df["application_date"].dt.month

    # Drop raw date
    df = df.drop(columns=["application_date"])

    # One-hot encoding
    df = pd.get_dummies(df)

    # Align with model columns
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[model_columns]

    return df


# -----------------------------
# Prediction
# -----------------------------

def predict_processing_time(input_data):

    processed = preprocess_input(input_data)

    prediction = model.predict(processed)

    return round(prediction[0])


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("Visa Processing Date Estimator")

st.write("Enter application details:")

country = st.selectbox("Country of Application", KNOWN_COUNTRIES)
visa_type = st.selectbox("Visa Type", KNOWN_VISA_TYPES)
application_date = st.date_input("Application Date")


# -----------------------------
# Predict button
# -----------------------------

if st.button("Predict Completion Date"):

    input_data = {
        "country": country,
        "visa_type": visa_type,
        "application_date": str(application_date)
    }

    try:
        days = predict_processing_time(input_data)

        # Convert to completion date
        completion_date = application_date + timedelta(days=int(days))

        st.success(f"Estimated Processing Time: {days} days")
        st.success(f"Expected Completion Date: {completion_date}")

    except Exception as e:
        st.error("Prediction failed")
        st.write(str(e))