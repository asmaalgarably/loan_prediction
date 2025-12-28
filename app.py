import streamlit as st
import requests

st.set_page_config(page_title="Loan Approval AI", page_icon="💰")
st.title("🏦 Smart Loan Approval System")

st.markdown("Enter client details to check loan eligibility:")

# تقسيم الواجهة لأعمدة
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    income = st.number_input("Applicant Monthly Income ($)", min_value=0)
    loan_amt = st.number_input("Loan Amount ($)", min_value=0)

with col2:
    self_emp = st.selectbox("Self Employed", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    property_area = st.selectbox(
        "Property Area", ["Urban", "Semiurban", "Rural"])
    credit_hist = st.selectbox("Credit History Clean?", ["Yes", "No"])
    term = st.number_input("Term (Days)", value=360)

# تحويل النصوص لأرقام قبل إرسالها للـ API (Mapping)
gender_val = 1 if gender == "Male" else 0
married_val = 1 if married == "Yes" else 0
edu_val = 0 if education == "Graduate" else 1
self_val = 1 if self_emp == "Yes" else 0
cred_val = 1.0 if credit_hist == "Yes" else 0.0
area_map = {"Urban": 0, "Rural": 1, "Semiurban": 2}
dep_map = {"0": 0, "1": 1, "2": 2, "3+": 3}

if st.button("Check Eligibility"):
    payload = {
        "Gender": gender_val, "Married": married_val, "Dependents": dep_map[dependents],
        "Education": edu_val, "Self_Employed": self_val, "ApplicantIncome": float(income),
        "CoapplicantIncome": 0.0, "LoanAmount": float(loan_amt),
        "Loan_Amount_Term": float(term), "Credit_History": cred_val,
        "Property_Area": area_map[property_area]
    }

    res = requests.post("http://127.0.0.1:8000/predict", json=payload)
    result = res.json()

    if "OK" in result['loan_sataus']:
        st.success(f"Result: {result['loan_sataus']}")
    else:
        st.error(f"Result: {result['loan_sataus']}")
