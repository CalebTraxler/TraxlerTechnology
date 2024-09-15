# C:\Users\caleb


import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Traxler Technology - Mars Colonization",
    layout="wide",
)

# Function to add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )

# Uncomment the line below to add a background image
# add_bg_from_local('assets/background.jpg')

# Load the logo image
logo = Image.open('love.png')

# Sidebar configuration
st.sidebar.image(logo, use_column_width=True)
st.sidebar.title("Navigation")
#page = st.sidebar.radio(
    #"Go to",
    #["Home", "Mars Data Explorer", "Colonization Simulations", "About Us"],
#)

page = st.sidebar.radio(
    "Go to",
    ["Home", "About Us"],
)

# Custom CSS for fonts and headings
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .sub-header {
        text-align: center;
        color: #555;
        padding: 0 0 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

# Mars Data Explorer
elif page == "Mars Data Explorer":
    st.markdown("<h1 class='main-header'>Mars Data Explorer</h1>", unsafe_allow_html=True)

    st.write(
        """
        Dive into detailed visualizations of Mars' terrain, climate, and more.
        Use the tools below to explore the Red Planet like never before.
        """
    )

    # Placeholder for Mars terrain data visualization
    st.subheader("Mars Surface Elevation Map")

    # Sample elevation data (replace with real Mars data later)
    elevation_data = np.random.rand(50, 50)

    fig = go.Figure(data=[go.Surface(z=elevation_data)])
    fig.update_layout(
        title='Mars Surface Elevation',
        autosize=False,
        width=800,
        height=800,
        margin=dict(l=65, r=50, b=65, t=90),
    )

    st.plotly_chart(fig)

# Colonization Simulations
elif page == "Colonization Simulations":
    st.markdown("<h1 class='main-header'>Colonization Simulations</h1>", unsafe_allow_html=True)

    st.write(
        """
        Simulate various aspects of Mars colonization, including habitat design,
        resource management, and population growth.
        """
    )

    st.subheader("Mars Colony Habitat Designer")

    # User inputs for simulation
    module_size = st.selectbox("Select Module Size", ["Small", "Medium", "Large"])
    energy_source = st.radio("Choose Energy Source", ["Solar", "Nuclear", "Wind"])
    include_life_support = st.checkbox("Include Life Support Systems", True)

    # Simulated calculations (you can enhance these later)
    if module_size == "Small":
        base_area = 50
    elif module_size == "Medium":
        base_area = 100
    else:
        base_area = 200

    energy_multiplier = 1.0
    if energy_source == "Solar":
        energy_multiplier = 1.0
    elif energy_source == "Nuclear":
        energy_multiplier = 1.5
    else:
        energy_multiplier = 1.2

    energy_requirements = base_area * energy_multiplier

    st.write(f"Estimated Habitat Base Area: {base_area} square meters")
    st.write(f"Estimated Energy Requirements: {energy_requirements} kWh/day")

    if include_life_support:
        st.write("Life Support Systems: Included")
    else:
        st.write("Life Support Systems: Not Included")

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