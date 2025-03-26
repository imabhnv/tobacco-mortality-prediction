import streamlit as st
import numpy as np
import joblib  

# Load trained model & label encoders
model = joblib.load("mortality_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Streamlit UI
st.title("🚬 Tobacco Use & Mortality Prediction 🏥")

st.write("Enter the details below to predict mortality.")

# User Input Form
year = st.number_input("Year", min_value=2000, max_value=2030, value=2022)
icd10_code = st.text_input("ICD10 Code", "J40")  
icd10_diagnosis = st.text_input("ICD10 Diagnosis", "Bronchitis")  
diagnosis_type = st.text_input("Diagnosis Type", "Primary")  
metric = st.text_input("Metric", "Mortality Rate")  
sex = st.selectbox("Sex", ["Male", "Female"])  

# Economic & Age-related Inputs
tobacco_price = st.number_input("Tobacco Price Index", value=100.0)
retail_price = st.number_input("Retail Prices Index", value=105.0)
affordability = st.number_input("Affordability of Tobacco Index", value=80.0)
household_expenditure = st.number_input("Household Expenditure on Tobacco", value=200.0)
household_total = st.number_input("Household Expenditure Total", value=5000.0)

# Age Group Inputs
age_16_over = st.number_input("16 and Over", value=20.0)
age_16_24 = st.number_input("16-24", value=10.0)
age_25_34 = st.number_input("25-34", value=15.0)
age_35_49 = st.number_input("35-49", value=18.0)
age_50_59 = st.number_input("50-59", value=12.0)
age_60_over = st.number_input("60 and Over", value=8.0)

# **Convert User Input Using Saved LabelEncoders**
try:
    icd10_code_encoded = label_encoders["ICD10 Code"].transform([icd10_code])[0] if icd10_code in label_encoders["ICD10 Code"].classes_ else 0
    icd10_diagnosis_encoded = label_encoders["ICD10 Diagnosis"].transform([icd10_diagnosis])[0] if icd10_diagnosis in label_encoders["ICD10 Diagnosis"].classes_ else 0
    diagnosis_type_encoded = label_encoders["Diagnosis Type"].transform([diagnosis_type])[0] if diagnosis_type in label_encoders["Diagnosis Type"].classes_ else 0
    metric_encoded = label_encoders["Metric"].transform([metric])[0] if metric in label_encoders["Metric"].classes_ else 0
    sex_encoded = label_encoders["Sex_x"].transform([sex])[0] if sex in label_encoders["Sex_x"].classes_ else 0

    # Define correct feature order (17 features, same as model training)
    feature_order = [
        "Year", "ICD10 Code", "ICD10 Diagnosis", "Diagnosis Type", "Metric",  
        "Sex_x", "Tobacco Price\nIndex", "Retail Prices\nIndex", 
        "Affordability of Tobacco Index", "Household Expenditure on Tobacco", 
        "Household Expenditure Total", 
        "16 and Over", "16-24", "25-34", "35-49", "50-59", "60 and Over"
    ]

    # Convert user input into correct order
    input_data = np.array([[year, icd10_code_encoded, icd10_diagnosis_encoded, diagnosis_type_encoded, 
                            metric_encoded, sex_encoded, tobacco_price, retail_price, affordability,
                            household_expenditure, household_total,  
                            age_16_over, age_16_24, age_25_34, age_35_49, age_50_59, age_60_over]]).astype(float)

    # Ensure correct feature count before prediction
    if input_data.shape[1] != len(feature_order):
        st.error(f"⚠ Feature mismatch: Model expects {len(feature_order)} features, but {input_data.shape[1]} provided.")
    else:
        if st.button("🔍 Predict Mortality"):
            prediction = model.predict(input_data)
            st.success(f"📈 Predicted Mortality: {int(prediction[0])}")

except KeyError as e:
    st.error(f"⚠ Invalid input: {e}. Please enter correct values.")
except ValueError as e:
    st.error(f"⚠ Encoding Error: {e}. Please check input format.")
