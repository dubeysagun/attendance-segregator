# app.py
import streamlit as st
import joblib
import pandas as pd
from utils import preprocess_image
from PIL import Image

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load('roll_number_recognizer.pkl')

st.title("Handwritten Roll Number Recognition")
model = load_model()

uploaded_files = st.file_uploader("Upload Handwritten Roll Number Image(s)", type=['png', 'jpg'], accept_multiple_files=True)
last_roll_number = st.number_input("Enter the last roll number:", min_value=1, step=1)

if st.button("Identify Present and Absent Students"):
    present_roll_numbers = []
    for file in uploaded_files:
        processed_image = preprocess_image(file)
        prediction = model.predict([processed_image])[0]
        present_roll_numbers.append(prediction)
    
    present_roll_numbers = set(sorted(present_roll_numbers))
    all_roll_numbers = set(range(1, int(last_roll_number) + 1))
    absent_roll_numbers = sorted(all_roll_numbers - present_roll_numbers)

    st.write("### Present Students")
    st.write(list(present_roll_numbers))
    st.write("### Absent Students")
    st.write(absent_roll_numbers)

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame({
        'Present': list(present_roll_numbers) + [''] * (len(absent_roll_numbers) - len(present_roll_numbers)),
        'Absent': absent_roll_numbers + [''] * (len(present_roll_numbers) - len(absent_roll_numbers))
    })
    df.to_excel('attendance_report.xlsx', index=False)
    st.success("Attendance report saved as 'attendance_report.xlsx'")
