import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import numpy as np
import joblib
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load saved models and encoders from approvalloan1.py paths
model_path = "logistic_regression_model.pkl"
scaler_path = "scaler.pkl"
encoder_path = "label_encoders.pkl"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(encoder_path)

st.set_page_config(page_title="Banking Loan Approval System", layout="wide")

st.title("🏦 Banking Loan Approval System")
st.subheader("Enter Applicant Details Below:")

def calculate_monthly_installment(loan_amount, loan_duration, interest_rate):
    loan_duration_months = int(loan_duration.split()[0])
    monthly_interest_rate = interest_rate / 12
    if monthly_interest_rate == 0:
        return loan_amount / loan_duration_months
    else:
        return (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_duration_months)

def calculate_total_payment(loan_amount, loan_duration, interest_rate):
    monthly_installment = calculate_monthly_installment(loan_amount, loan_duration, interest_rate)
    total_payment = monthly_installment * int(loan_duration.split()[0])
    return total_payment

def calculate_checks(loan_duration, total_payment):
    loan_duration_months = int(loan_duration.split()[0])
    num_checks = loan_duration_months // 3
    check_value = total_payment / num_checks if num_checks > 0 else 0
    return num_checks, check_value

col1, col2 = st.columns(2)

with col1:
    application_date = st.date_input("**Application Date**", datetime.date.today())
    age = st.number_input("**Age**", min_value=20, step=1)
    annual_income = st.number_input("**Annual Income (EGP)**", min_value=50000, step=1000)
    credit_score = st.slider("**Credit Score**", 300, 850, 600)
    education_level = st.selectbox("**Education Level**", ["Bachelor", "Doctorate", "High School", "Master"])
    experience = st.number_input("**Experience (Years)**", min_value=3, step=1)
    loan_amount = st.number_input("**Loan Amount (EGP)**", min_value=10000, step=5000)
    loan_duration = st.selectbox("**Loan Duration**", ["24 months", "36 months", "60 months", "84 months", "120 months"])
    interest_rate = st.slider("**Interest Rate (%)**", 0.01, 1.0, 0.05)

with col2:
    marital_status = st.selectbox("**Marital Status**", ["Married", "Single", "Divorced"])
    home_ownership = st.selectbox("**Home Ownership Status**", ["Own", "Rent", "Other"])
    monthly_debt = st.number_input("**Monthly Debt Payments (EGP)**", min_value=0, step=100)
    credit_utilization = st.slider("**Credit Card Utilization Rate**", 0.0, 1.0, 0.3)
    credit_inquiries = st.number_input("**Number of Credit Inquiries**", min_value=0, step=1)
    loan_purpose = st.number_input("**Loan Purpose (Numeric)**", min_value=1, step=1)
    payment_history = st.number_input("**Payment History (Numeric)**", min_value=1, step=1)
    checking_balance = st.number_input("**Checking Account Balance (EGP)**", min_value=0, step=1000)

# Additional fields
st.subheader("Additional Financial Details")
total_assets = st.number_input("**Total Assets (EGP)**", min_value=0, step=5000)
total_liabilities = st.number_input("**Total Liabilities (EGP)**", min_value=0, step=5000)
monthly_income = st.number_input("**Monthly Income (EGP)**", min_value=0, step=1000)
utility_bills = st.number_input("**Utility Bills Payment History (EGP)**", min_value=0, step=100)
job_tenure = st.number_input("**Job Tenure (Years)**", min_value=0, step=1)
monthly_loan_payment = st.number_input("**Monthly Loan Payment (EGP)**", min_value=0, step=1000)
risk_score = st.number_input("**Risk Score (Numeric)**", min_value=1, step=1)

if st.button("Predict Loan Approval"):
    if age >= 20 and annual_income >= 50000 and experience >= 3 and loan_amount >= 10000:
        monthly_installment = calculate_monthly_installment(loan_amount, loan_duration, interest_rate)
        total_payment = calculate_total_payment(loan_amount, loan_duration, interest_rate)
        num_checks, check_value = calculate_checks(loan_duration, total_payment)
        
        st.success("✅ Loan Approved!")
        st.table({
            "Loan Amount (EGP)": [loan_amount],
            "Interest Rate (%)": [interest_rate * 100],
            "Duration (Months)": [loan_duration],
            "Monthly Installment (EGP)": [round(monthly_installment, 2)],
            "Total Payment (EGP)": [round(total_payment, 2)],
            "Number of Quarterly Checks": [num_checks],
            "Check Value (EGP)": [round(check_value, 2)]
        })
    else:
        st.error("❌ Loan cannot be processed due to invalid inputs.")
