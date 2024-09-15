# C:\Users\caleb
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64

# Set page configuration with theme settings
st.set_page_config(
    page_title="Traxler Technology - Mars Colonization",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load the logo image
logo = Image.open('love.png')

# Custom CSS for white background and black text, including sidebar and top bar
st.markdown(
    """
    <style>
    body, html, .css-1v3fvcr, .stApp, .sidebar .sidebar-content, .css-18e3th9,
    .css-1d391kg, .css-1e5imcs, .css-1vbkxwb {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .sidebar .sidebar-content, [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }

    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
        color: #000000;
    }

    .sub-header {
        text-align: center;
        color: #333333;
        padding: 0 0 20px 0;
    }

    .stButton>button {
        color: #000000;
        border-color: #000000;
    }

    .stTextInput>div>div>input {
        color: #000000;
    }

    .stSelectbox>div>div>select {
        color: #000000;
    }

    .stCheckbox>label>div {
        color: #000000;
    }

    .css-145kmo2 {
        color: #000000;
    }

    /* Ensure sidebar text is black */
    .sidebar .sidebar-content {
        color: #000000 !important;
    }

    /* Style the radio buttons in the sidebar */
    .stRadio > label {
        color: #000000 !important;
    }

    /* Ensure the top bar hamburger menu is black */
    .css-1rs6os {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar configuration
st.sidebar.image(logo, use_column_width=True)
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "About Us"],
)

# Home Page
if page == "Home":
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("")
    with col2:
        st.write("")
        st.image(logo, use_column_width=True)
    with col3:
        st.write("")

    st.markdown("<h1 class='main-header'>Welcome to Traxler Technology</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Pioneering the Future of Mars Colonization in 2024</h2>", unsafe_allow_html=True)
    st.write(
        """
        Traxler Technology is at the forefront of space exploration and Mars colonization.
        Join us as we embark on a journey to make humanity a multi-planetary species.
        Explore our interactive tools and simulations to learn more about the Red Planet and
        how we plan to establish a sustainable human presence on Mars.
        """
    )

# About Us
elif page == "About Us":
    st.markdown("<h1 class='main-header'>About Traxler Technology</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("new.png", width=200, caption="Founder & CEO")

    with col2:
        st.write(
            """
            **Our Mission**

            At Traxler Technology, our mission is to advance humanity's reach into the cosmos by pioneering
            innovative solutions for Mars exploration and colonization. We believe in a future where humans
            live and thrive on multiple planets.

            **Our Founder**

            Caleb Traxler, Founder & CEO of Traxler Technology is a visionary entrepreneur with a passion for space exploration and technology. 
            Caleb has an comprehensive academic background in Machine Learning and Artificial Intelligence, he founded Traxler Technology to bring the dream of 
            Mars colonization closer to reality. Caleb and his team will help bring the notion humanity being 
            a space-faring civilization to reality. At Traxler Technology, we will determine what Mars has to offer to humanity by analyzing the martian landscape, mineral compositions, elevation levels and much more. 

            **Our Team**

            We are a team of passionate engineers, scientists, and visionaries dedicated to making Mars
            colonization a reality. Our diverse backgrounds and expertise enable us to tackle the complex
            challenges of interplanetary travel and settlement.

            **Contact Us**

            - **Email**: [traxlertechnology@gmail.com](mailto:traxlertechnology@gmail.com)

            **Follow Us**

            - [LinkedIn](https://www.linkedin.com/company/traxlertech)
            """
        )

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        &copy; 2024 Traxler Technology. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
