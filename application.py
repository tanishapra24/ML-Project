import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import requests
import os
import random

# ✅ Streamlit Config
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🩺")
st.title("🩺 AI Health Assistant")

# ✅ Disease Symptoms and Tips
disease_symptoms = {
    "Diabetes": ["frequent urination", "excessive thirst", "weight loss", "fatigue"],
    "Heart Disease": ["chest pain", "shortness of breath", "fatigue", "swelling in legs"],
    "Parkinson’s": ["tremors", "slow movement", "rigidity", "imbalance"],
    "Migraine": ["headache", "nausea", "sensitivity to light"],
}

health_tips = {
    "Diabetes": ["Maintain a low-sugar diet.", "Exercise regularly.", "Monitor blood glucose levels.", "Stay hydrated.", "Regular check-ups are important."],
    "Heart Disease": ["Eat heart-healthy foods.", "Avoid trans fats.", "Exercise regularly.", "Monitor blood pressure.", "Manage stress effectively."],
    "Parkinson’s": ["Engage in physical activities.", "Eat a balanced diet.", "Practice speech exercises.", "Take prescribed medications.", "Join a support group."],
    "Migraine": ["Avoid triggers like bright lights.", "Stay hydrated.", "Manage stress.", "Get quality sleep.", "Use prescribed medication."]
}

youtube_links = {
    "Diabetes": "https://www.youtube.com/watch?v=UreXHz5lSPA",
    "Heart Disease": "https://www.youtube.com/watch?v=Fu1u11iRKAE",
    "Parkinson’s": "https://www.youtube.com/watch?v=_gtjIxb5ufE",
    "Migraine": "https://www.youtube.com/watch?v=3WfNODxZbGg"
}

# ✅ Appointment Links (Updated to Lybrate)
appointment_links = {
    "Diabetes": "https://www.lybrate.com/mumbai/diabetologists",
    "Heart Disease": "https://www.lybrate.com/mumbai/cardiologists",
    "Parkinson’s": "https://www.lybrate.com/mumbai/neurologists",
    "Migraine": "https://www.lybrate.com/mumbai/neurologists"
}

# ✅ Prediction Function
def predict_disease(symptoms, disease_name):
    if any(symptom in disease_symptoms[disease_name] for symptom in symptoms):
        return f"High chances of {disease_name}. Consult a doctor."
    else:
        return f"Low risk of {disease_name}, but stay cautious."

# ✅ PDF Generator
def generate_pdf(disease_name, prediction, symptoms):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{disease_name} Prediction Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Symptoms Entered: {', '.join(symptoms)}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction: {prediction}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Health Tips:", ln=True, align='L')
    for tip in health_tips[disease_name]:
        pdf.cell(200, 10, txt=f"- {tip}", ln=True)
    pdf_path = "disease_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

# ✅ Chatbot Function
def get_health_answer(question):
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "search", "srsearch": question, "format": "json"}
        search_response = requests.get(search_url, params=params)
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data["query"]["search"]:
                title = search_data["query"]["search"][0]["title"]
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '%20')}"
                summary_response = requests.get(summary_url)
                if summary_response.status_code == 200:
                    context = summary_response.json().get("extract", "")
                    if len(context) > 50:
                        return context
    except:
        pass

    fallback_responses = {
        "sugar": "According to WHO, sugar intake should be below 10% of total energy intake, ideally under 5%.",
        "heart": "Heart disease signs include chest pain, fatigue, and breathlessness. Lifestyle changes help prevent it.",
        "diabetes": "Manage diabetes with a healthy diet, exercise, and regular sugar level checks.",
        "migraine": "Migraines cause intense headache, nausea, and sensitivity to light.",
        "parkinson": "Parkinson's symptoms include tremors, stiffness, and balance problems. It's a neurological disorder."
    }
    for keyword, response in fallback_responses.items():
        if keyword in question.lower():
            return response

    return "Sorry, I couldn't find reliable medical information. Try rephrasing or asking about another topic."

# ✅ Sidebar & Inputs
st.sidebar.title("Multiple Disease Prediction System")
disease_name = st.sidebar.radio("Choose a Disease:", list(health_tips.keys()))
st.header(f"{disease_name} Prediction using AI")

st.subheader("Enter your symptoms below:")
symptoms_input = st.text_area("List symptoms separated by commas (e.g., fatigue, chest pain, dizziness)")

if st.button("Get Prediction"):
    symptoms_list = [s.strip().lower() for s in symptoms_input.split(",")]
    prediction = predict_disease(symptoms_list, disease_name)

    st.write("### 🩺 Prediction Result:")
    st.success(prediction)

    # ✅ Symptom-Sensitive Risk Meter
    st.subheader("📊 Risk Meter")
    matched = [s for s in symptoms_list if s in disease_symptoms[disease_name]]
    total = len(disease_symptoms[disease_name])
    match_count = len(matched)
    risk_score = int((match_count / total) * 100) if total > 0 else 0

    fig, ax = plt.subplots(figsize=(4, 4))
    colors = ["#ff4d4d", "#d9d9d9"]
    wedges, texts, autotexts = ax.pie(
        [risk_score, 100 - risk_score],
    
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        textprops={'fontsize': 12}
    )
    
    ax.axis("equal")
    st.pyplot(fig)

    if match_count == 0:
        st.info("No known symptoms matched. The risk appears low.")
    elif match_count < total // 2:
        st.warning("Partial symptoms matched. Monitor closely or consult a doctor.")
    else:
        st.error("Several symptoms matched. Consult a healthcare professional.")

    # ✅ Health Tips
    st.subheader("🔹 Health Tips:")
    selected_tips = random.sample(health_tips[disease_name], min(3, len(health_tips[disease_name])))
    for tip in selected_tips:
        st.write(f"✅ {tip}")

    # ✅ YouTube Video
    st.subheader("🎥 Watch this Health Tutorial:")
    st.video(youtube_links[disease_name])
    st.markdown(f"[Open on YouTube 🔗]({youtube_links[disease_name]})", unsafe_allow_html=True)

    # ✅ Appointment Booking
    st.subheader("👨‍⚕️ Book a Doctor Appointment:")
    st.markdown(f"[Click here to book a doctor for {disease_name} 🔗]({appointment_links[disease_name]})", unsafe_allow_html=True)

    # ✅ PDF Download
    pdf_path = generate_pdf(disease_name, prediction, symptoms_list)
    with open(pdf_path, "rb") as file:
        st.download_button(label="📄 Download Report as PDF", data=file, file_name="Disease_Report.pdf", mime="application/pdf")

# ✅ Chatbot
st.subheader("💬 Chat with HealthBot")
user_chat = st.text_input("You:", key="chat_input")
if user_chat:
    response = get_health_answer(user_chat)
    st.markdown(f"**HealthBot 🤖:** {response}")
