# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 02:20:13 2025

@author: chetna09
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Load saved models
diabetes_model = pickle.load(open('C:/Users/chetn/Desktop/Multiple Disease Prediction System/saved models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:/Users/chetn/Desktop/Multiple Disease Prediction System/saved models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('C:/Users/chetn/Desktop/Multiple Disease Prediction System/saved models/parkinsons_model.sav', 'rb'))

# Sidebar navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    diab_diagnosis = ''
    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]
        user_input = [float(x) for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])
        diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'

    st.success(diab_diagnosis)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age', help="Enter the age in years")
    with col2:
        sex = st.text_input('Sex (0 = Female, 1 = Male)', help="0 for Female, 1 for Male")
    with col3:
        cp = st.text_input('Chest Pain Type (0–3)', help="0: Typical angina, 1: Atypical angina, 2: Non-anginal pain, 3: Asymptomatic")

    with col1:
        trestbps = st.text_input('Resting Blood Pressure (mm Hg)', help="Resting blood pressure in mm Hg")
    with col2:
        chol = st.text_input('Serum Cholesterol (mg/dl)', help="Serum cholesterol in mg/dl")
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = True; 0 = False)', help="1 if fasting blood sugar > 120 mg/dl, else 0")

    with col1:
        restecg = st.text_input('Resting ECG Results (0–2)', help="0: Normal, 1: ST-T abnormality, 2: Left ventricular hypertrophy")
    with col2:
        thalach = st.text_input('Max Heart Rate Achieved', help="Maximum heart rate achieved during test")
    with col3:
        exang = st.text_input('Exercise Induced Angina (1 = Yes; 0 = No)', help="1 if yes, 0 if no")

    with col1:
        oldpeak = st.text_input('ST Depression (Oldpeak)', help="ST depression induced by exercise relative to rest")
    with col2:
        slope = st.text_input('Slope of ST Segment (0–2)', help="0: Upsloping, 1: Flat, 2: Downsloping")
    with col3:
        ca = st.text_input('Number of Major Vessels (0–3) Colored by Fluoroscopy', help="Enter number of major vessels (0–3)")

    with col1:
        thal = st.text_input('Thalassemia (1 = Normal; 2 = Fixed Defect; 3 = Reversible Defect)', help="1: Normal, 2: Fixed defect, 3: Reversible defect")

    heart_diagnosis = ''
    if st.button('Heart Disease Test Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                      exang, oldpeak, slope, ca, thal]
        user_input = [float(x) for x in user_input]
        heart_prediction = heart_disease_model.predict([user_input])
        heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'

    st.success(heart_diagnosis)

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    st.title("Parkinson's Disease Prediction using ML")

    st.markdown("#### Input features with explanations:")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo (Hz)', help="Average vocal fundamental frequency")
    with col2:
        fhi = st.text_input('MDVP:Fhi (Hz)', help="Maximum vocal fundamental frequency")
    with col3:
        flo = st.text_input('MDVP:Flo (Hz)', help="Minimum vocal fundamental frequency")
    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter (%)', help="Variation in fundamental frequency")
    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter (Abs)', help="Absolute variation in fundamental frequency")

    with col1:
        RAP = st.text_input('MDVP:RAP', help="Relative average perturbation")
    with col2:
        PPQ = st.text_input('MDVP:PPQ', help="Five-point period perturbation quotient")
    with col3:
        DDP = st.text_input('Jitter:DDP', help="Average absolute difference of differences between cycles")
    with col4:
        Shimmer = st.text_input('MDVP:Shimmer', help="Variation in amplitude")
    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer (dB)', help="Variation in amplitude in decibels")

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3', help="Three-point amplitude perturbation quotient")
    with col2:
        APQ5 = st.text_input('Shimmer:APQ5', help="Five-point amplitude perturbation quotient")
    with col3:
        APQ = st.text_input('MDVP:APQ', help="Amplitude perturbation quotient")
    with col4:
        DDA = st.text_input('Shimmer:DDA', help="Average absolute difference between consecutive amplitudes")
    with col5:
        NHR = st.text_input('NHR', help="Noise-to-harmonics ratio")

    with col1:
        HNR = st.text_input('HNR', help="Harmonics-to-noise ratio")
    with col2:
        RPDE = st.text_input('RPDE', help="Recurrence period density entropy")
    with col3:
        DFA = st.text_input('DFA', help="Signal fractal scaling exponent")
    with col4:
        spread1 = st.text_input('Spread1', help="Nonlinear measure of fundamental frequency variation")
    with col5:
        spread2 = st.text_input('Spread2', help="Another nonlinear measure of fundamental frequency variation")

    with col1:
        D2 = st.text_input('D2', help="Correlation dimension")
    with col2:
        PPE = st.text_input('PPE', help="Pitch period entropy")

    parkinsons_diagnosis = ''
    if st.button("Parkinson's Test Result"):
        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        user_input = [float(x) for x in user_input]
        parkinsons_prediction = parkinsons_model.predict([user_input])
        parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"

    st.success(parkinsons_diagnosis)
