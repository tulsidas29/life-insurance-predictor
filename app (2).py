import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Insure AI Predictor",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background-color:#0E1117;
}

.hero{
    text-align:center;
    padding:25px;
    border-radius:15px;
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    margin-bottom:20px;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>INSURE AI PREDICTOR</h1>
<h4>Protect Your Future With AI</h4>
</div>
""", unsafe_allow_html=True)

with open("insurance_model.pkl", "rb") as file:
    model = pickle.load(file)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Applicant Information")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    income = st.number_input(
        "Annual Income",
        min_value=0,
        value=50000
    )

    credit_score = st.number_input(
        "Credit Score",
        min_value=0,
        max_value=1000,
        value=700
    )

with col2:

    st.subheader("Health And Employment Information")

    smoker = st.selectbox(
        "Smoker",
        [0, 1]
    )

    medical_history = st.selectbox(
        "Medical History",
        [0, 1]
    )

    employment_years = st.number_input(
        "Employment Years",
        min_value=0,
        value=5
    )

st.markdown("---")

if st.button(
    "Analyze Application",
    use_container_width=True
):

    data = pd.DataFrame({
        "Age": [age],
        "Annual_Income": [income],
        "Credit_Score": [credit_score],
        "Smoker": [smoker],
        "Medical_History": [medical_history],
        "Employment_Years": [employment_years]
    })

    data["Income_Age_Ratio"] = (
        data["Annual_Income"] /
        (data["Age"] + 1)
    )

    data["Risk_Score"] = (
        data["Smoker"] +
        data["Medical_History"]
    )

    data["Income_Experience"] = (
        data["Annual_Income"] *
        data["Employment_Years"]
    )

    prediction = model.predict(data)[0]

    try:
        probability = int(
            model.predict_proba(data)[0].max() * 100
        )
    except:
        probability = 90

    if probability >= 80:
        risk = "Low Risk"
    elif probability >= 60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("Insurance Approved")
    else:
        st.error("Insurance Rejected")

    st.metric(
        "Confidence Score",
        f"{probability}%"
    )

    st.info(
        f"Risk Level: {risk}"
    )

st.markdown("""
<div class='footer'>
© 2026 Life Insurance Approval Prediction System
</div>
""", unsafe_allow_html=True)