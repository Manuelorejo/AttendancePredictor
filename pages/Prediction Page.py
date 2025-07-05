# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 21:07:38 2025

@author: Oreoluwa
"""
# Import required libraries
import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import json


# Set page configuration FIRST
st.set_page_config(
    page_title="LASUCOM Attendance Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe Lottie animation loader with error handling
def load_lottie(url_or_path):
    try:
        if url_or_path.startswith('http'):
            r = requests.get(url_or_path)
            if r.status_code == 200:
                return r.json()
        else:
            with open(url_or_path) as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Animation loading failed: {str(e)}")
        return None

# Load animations safely
lottie_education = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0yfsb3a1.json") or {}
lottie_success = load_lottie("https://assets4.lottiefiles.com/packages/lf20_auwi6jpu.json") or {}

# Load or train model
@st.cache_resource
def load_model():
    # Try to load existing model
    model = joblib.load('ensembleModel.joblib')
    df = pd.read_csv('Attendance_Dataset2.csv')
    return model, df
    

model, df = load_model()



# Custom CSS for styling
st.markdown("""
    <style>
    
    :root {
        --background-color: white;
        --text-color: black;
        --block-background-color: #ffffff;
    }

    [data-theme="dark"] {
        --background-color: #0e1117;
        --text-color: #ffffff;
        --block-background-color: #262730;
    }

    /* Theme-adaptive colors */
    html, body, .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Feature and result cards */
    .feature-card, .result-box, .testimonial-card {
        background-color: var(--block-background-color);
        color: var(--text-color);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #4CAF50;
    }

    /* Headers */
    .header {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 20px;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--block-background-color);
        color: var(--text-color);
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #45a049 !important;
        transform: scale(1.05);
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--block-background-color);
        color: var(--text-color);
    }

    /* Responsive tweaks */
    @media screen and (max-width: 768px) {
        .header {
            font-size: 1.5rem;
        }
        .feature-icon {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar with navigation
with st.sidebar:
    if lottie_education:
        st_lottie(lottie_education, height=150, key="sidebar_animation")
    st.markdown("<h2 style='text-align: center; color: white;'>LASUCOM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Computer Science Department</p>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Predict Attendance", "About"],
        icons=["calculator", "gear", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2c3e50"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color": "white"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

# Main content
if selected == "Predict Attendance":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 class='header'>Course Attendance Predictor</h1>", unsafe_allow_html=True)
    with col2:
        if lottie_education:
            st_lottie(lottie_education, height=100, key="header_animation")
    
    st.markdown("""
    <div style='background-color: var(--block-background-color); color: var(--text-color); padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    This tool helps you predict the required attendance percentage based on your course selection and preferences. 
    Select your year and course from the dropdowns, then provide additional information to get your personalized prediction.
    </div>
    """, unsafe_allow_html=True)
    
    
    # Initialize session state for form if not exists
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'selected_year': 1,
            'selected_course': None,
            'materials_available': "Yes",
            'desired_grade': 70,
            'mode': "Physical"
        }
    
    # Year selection - updates immediately when changed
    selected_year = st.selectbox(
        "Select Your Year of Study",
        options=sorted(df['Year'].unique()),
        index=0,
        help="Choose your current academic year",
        key='year_select'
    )
    
    # Update courses when year changes
    if st.session_state.form_data['selected_year'] != selected_year:
        st.session_state.form_data['selected_year'] = selected_year
        st.session_state.form_data['selected_course'] = None  # Reset course selection
    
    # Get courses for selected year
    year_courses = df[df['Year'] == selected_year][[ 'Course Title','Course Code','Credits', 'Status']].drop_duplicates()
    course_options = [f"{row['Course Code']} - {row['Course Title']}" for _, row in year_courses.iterrows()]
    
    # Course selection
    selected_course = st.selectbox(
        "Select Your Course",
        options=course_options,
        index=0 if st.session_state.form_data['selected_course'] is None else course_options.index(st.session_state.form_data['selected_course']),
        help="Choose the course you want to predict attendance for",
        key='course_select'
    )
    
    # Update session state when course changes
    if st.session_state.form_data['selected_course'] != selected_course:
        st.session_state.form_data['selected_course'] = selected_course
    
    # Get course details
    selected_code = selected_course.split(" - ")[0]
    course_details = year_courses[year_courses['Course Code'] == selected_code].iloc[0]
    
    with st.expander("Selected Course Details", expanded=True):
        cols = st.columns(4)
        cols[0].metric("Course Code", course_details['Course Code'])
        cols[1].metric("Credits", course_details['Credits'])
        cols[2].metric("Year", selected_year)
        cols[3].metric("Requirement", course_details['Status'])
        st.caption(f"Course Title: {course_details['Course Title']}")
    
    st.subheader("Additional Information")
    col1, col2 = st.columns(2)
    
    with col1:
        materials_available = st.radio(
            "Are Course Materials Available?",
            options=["Yes", "No"],
            index=0 if st.session_state.form_data['materials_available'] == "Yes" else 1,
            horizontal=True,
            key='materials_radio'
        )
        
        desired_grade = st.slider(
            "Desired Grade (%)",
            min_value=40,
            max_value=100,
            value=st.session_state.form_data['desired_grade'],
            step=1,
            help="The grade you aim to achieve in this course",
            key='grade_slider'
        )
    
    with col2:
        mode = st.radio(
            "Mode of Class Delivery",
            options=["Physical", "Hybrid", "Online"],
            index=0 if st.session_state.form_data['mode'] == "Physical" else (1 if st.session_state.form_data['mode'] == "Hybrid" else 2),
            horizontal=True,
            key='mode_radio'
        )
    
    # Update session state with current values
    st.session_state.form_data.update({
        'materials_available': materials_available,
        'desired_grade': desired_grade,
        'mode': mode
    })
    
    submit_button = st.button("Predict Attendance", type="primary", key='predict_button')
    
    if submit_button:
        input_data = {
            'Credits': [course_details['Credits']],
            'Status': [course_details['Status']],
            'Materials': [materials_available],
            'Year': [selected_year],
            'Grade': [desired_grade],
            'Mode': [mode]
        }
        
        input_df = pd.DataFrame(input_data)
        input_df['Materials'] = input_df['Materials'].map({'Yes': 1, 'No': 0})
        mode_mapping = {"Physical": 2, "Hybrid": 1, "Online": 0}
        input_df['Mode'] = input_df['Mode'].map(mode_mapping)
        status_mapping = {"C": 2, "E": 1, "R": 0}
        input_df['Status'] = input_df['Status'].map(status_mapping)
        
        predicted_attendance = model.predict(input_df)[0]
        predicted_attendance = max(10, min(100, round(predicted_attendance, 1)))
        
        with st.container():
            if lottie_success:
                st_lottie(lottie_success, height=150, key="success_animation")
            
            st.markdown(f"""
            <div class="result-box">
                <h2 style='color: #2c3e50;'>Prediction Result</h2>
                <p style='font-size: 18px;'>For <strong>{selected_course}</strong>:</p>
                <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <p style='font-size: 16px; margin: 5px 0;'>📚 Materials Available: <strong>{materials_available}</strong></p>
                    <p style='font-size: 16px; margin: 5px 0;'>🏫 Mode: <strong>{mode}</strong></p>
                    <p style='font-size: 16px; margin: 5px 0;'>🎯 Desired Grade: <strong>{desired_grade}%</strong></p>
                </div>
                <h3 style='color: #4CAF50;'>Recommended Attendance: <strong>{predicted_attendance}%</strong></h3>
            </div>
            """, unsafe_allow_html=True)
            
            if predicted_attendance >= 80:
                st.success("This course requires high attendance. Make sure to attend regularly and participate actively!")
            elif predicted_attendance >= 60:
                st.info("Moderate attendance is recommended. Balance your time between classes and self-study.")
            else:
                st.warning("Lower attendance is predicted, but make sure to compensate with thorough self-study.")


    
elif selected == "About":
    st.markdown("<h1 class='header'>About the Attendance Predictor</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    
        <h3 style='color: #2c3e50;'>📊 How It Works</h3>
        <p>This application uses machine learning to predict the required attendance percentage for Computer Science courses at Lagos State University.</p>
        
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
       
        <h3 style='color: #2c3e50; margin-top: 20px;'>🔍 Model Details</h3>
        <p>The prediction model was trained on historical course data and considers:</p>
        <ul>
            <li>Course characteristics (credits, year, requirement status)</li>
            <li>Learning mode (physical, hybrid, online)</li>
            <li>Availability of course materials</li>
            <li>Student's desired grade</li>
        </ul>""", unsafe_allow_html=True)
        
    
    st.markdown("""
        <h3 style='color: #2c3e50; margin-top: 20px;'>🎯 Purpose</h3>
        <p>This tool helps students plan their study time effectively by understanding the attendance requirements needed to achieve their academic goals.</p>
    """, unsafe_allow_html=True)
        
    st.markdown("""
        <h3 style='color: #2c3e50; margin-top: 20px;'>📝 Note</h3>
        <p>Predictions are based on statistical patterns and should be used as guidance rather than absolute requirements.</p>
    </div>
    """, unsafe_allow_html=True)