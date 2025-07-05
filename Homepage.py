import streamlit as st
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



# Load animations (with fallback to empty dict if loading fails)
try:
    lottie_education = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0yfsb3a1.json") or {}
    lottie_analytics = load_lottie("https://assets1.lottiefiles.com/packages/lf20_uzjci3wz.json") or {}

except:
    pass


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
        background-color: #4CAF50 !important;
        color: white !important;
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
        background-color: #2c3e50;
        color: white;
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
        options=["Home"],
        icons=["house", "calculator", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2c3e50"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color": "white"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

# Homepage content
if selected == "Home":
    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='header'>Welcome to LASUCOM Attendance Predictor</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size: 1.2rem; line-height: 1.6; margin-bottom: 30px;'>
            Optimize your academic performance with our intelligent attendance prediction system. 
            Get personalized recommendations to help you balance your study time effectively.
        </div>
        """, unsafe_allow_html=True)
        
        
            
    with col2:
        if lottie_analytics:
            st_lottie(lottie_analytics, height=300, key="hero_animation")

    # Features Section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>Key Features</h2>", unsafe_allow_html=True)
    
    # Feature cards in three columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📚</div>
            <h3>Course-Specific</h3>
            <p>Get predictions tailored to each course's requirements and credit load.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <h3>Data-Driven</h3>
            <p>Powered by machine learning models trained on historical academic data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <h3>Goal-Oriented</h3>
            <p>Adjust predictions based on your desired grade target.</p>
        </div>
        """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;background-color: var(--block-background-color); color: var(--text-color);'>How It Works</h2>", unsafe_allow_html=True)
    
    steps = [
        {"icon": "1️⃣", "title": "Select Your Course", "desc": "Choose from all Computer Science courses at LASUCOM"},
        {"icon": "2️⃣", "title": "Set Your Specifics", "desc": "Indicate materials availability and learning mode"},
        {"icon": "3️⃣", "title": "Get Your Prediction", "desc": "Receive personalized attendance recommendations"}
    ]
    
    # Display each step
    for step in steps:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin: 20px 0; padding: 15px;background-color: var(--block-background-color); color: var(--text-color); border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1)'>
            <div style='font-size: 2rem; margin-right: 20px;'>{step['icon']}</div>
            <div>
                <h3 style='margin: 0; color: #2c3e50;'>{step['title']}</h3>
                <p style='margin: 5px 0 0;'>{step['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


    # # Call-to-action button
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #2c3e50;'>Ready to Optimize Your Attendance?</h2>", unsafe_allow_html=True)
    
    if st.button("Start Predicting Now →", key="bottom_cta", type="primary"):
        st.switch_page("pages/Prediction Page.py")
        st.rerun()#Refresh the page
    