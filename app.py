# C:\Users\caleb

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ['plotly', 'folium']

print("Starting installation of packages...")
for package in packages:
    try:
        print(f"Installing {package}...")
        install(package)
        print(f"{package} installed successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please check your internet connection and try again.")


import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
#import folium



# Set page configuration with theme settings
st.set_page_config(
    page_title="Traxler Technology - Mars Colonization",
    layout="wide",
    initial_sidebar_state="auto"
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

page = st.sidebar.radio(
    "Go to",
    ["Home", "About Us"],
)

# Custom CSS for base theme (light) and text colors
st.markdown(
    """
    <style>
    body, html, .css-1v3fvcr, .stApp {
        background-color: #ffffff;  /* Secondary background color */
        color: #000000;  /* Text color */
    }

    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
        color: #000000;  /* Custom text color */
    }

    .sub-header {
        text-align: center;
        color: #555;
        padding: 0 0 20px 0;
    }

    .sidebar .sidebar-content {
        background-color: #ffffff;
        color: #000000;
    }

    .fullwidth {
        width: 100%;
        height: 600px;  /* Adjust this value to change the height of the map */
        margin: 0 auto;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to create Mars map
def create_mars_map():
    mars_map = folium.Map(
        location=[0, 0],
        zoom_start=3,
        tiles=None,
        attr='OpenPlanetaryMap'
    )
    folium.TileLayer(
        tiles='https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-mars-basemap-v0-1/all/{z}/{x}/{y}.png',
        attr='OpenPlanetaryMap',
        name='Mars',
        overlay=False,
        control=True
    ).add_to(mars_map)
    folium.Marker(
        [0, 0],
        popup="Center of Mars",
        tooltip="Click me!"
    ).add_to(mars_map)
    return mars_map

# Home Page
if page == "Home":
    st.markdown("<h1 class='main-header'>Welcome to Traxler Technology</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Pioneering the Future of Mars Colonization in 2024</h2>", unsafe_allow_html=True)
    
    # Use columns to center the logo
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo, use_column_width=True)
    
    st.write(
        """
        Traxler Technology is at the forefront of space exploration and Mars colonization.
        Join us as we embark on a journey to make humanity a multi-planetary species.
        Explore our interactive tools and simulations to learn more about the Red Planet and
        how we plan to establish a sustainable human presence on Mars.
        """
    )

    # Add Mars Map
    st.markdown("<h2 class='sub-header'>Explore Mars</h2>", unsafe_allow_html=True)
    st.write("                                             Interact with our Mars map to explore the Red Planet's surface.")
    
    mars_map = create_mars_map()
    mars_map.save("mars_map.html")
    
    # Use the full width of the page for the map
    st.components.v1.html(open("mars_map.html", 'r').read(), height=400, width=None)
    
    st.markdown("Map data: © OpenPlanetaryMap contributors")

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

# Mars Data Explorer and Colonization Simulations pages can be added here

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
