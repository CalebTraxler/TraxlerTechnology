# C:\Users\caleb
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
import plotly.graph_objects as go
import folium
import plotly.express as px
from datetime import datetime
import os

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
    ["Home", "Mars Minerals", "Mars Innovators Hub","About Us"],
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

# File to store ideas
IDEAS_FILE = 'mars_ideas.csv'

# Function to load ideas from CSV
def load_ideas():
    if os.path.exists(IDEAS_FILE):
        return pd.read_csv(IDEAS_FILE, parse_dates=['timestamp'])
    return pd.DataFrame(columns=['title', 'description', 'votes', 'timestamp'])

# Function to save ideas to CSV
def save_ideas(ideas_df):
    ideas_df.to_csv(IDEAS_FILE, index=False)

# Initialize session state to store ideas if it doesn't exist
if 'mars_ideas' not in st.session_state:
    st.session_state.mars_ideas = load_ideas()

def add_idea(title, description):
    new_idea = pd.DataFrame({
        'title': [title],
        'description': [description],
        'votes': [0],
        'timestamp': [datetime.now()]
    })
    st.session_state.mars_ideas = pd.concat([st.session_state.mars_ideas, new_idea], ignore_index=True)
    save_ideas(st.session_state.mars_ideas)

def vote_idea(index):
    st.session_state.mars_ideas.loc[index, 'votes'] += 1
    save_ideas(st.session_state.mars_ideas)

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

# Function for mineral composition chart
def create_mineral_chart():
    minerals = ['Iron Oxide', 'Silicon Dioxide', 'Aluminum Oxide', 'Calcium Oxide', 'Magnesium Oxide', 'Other']
    percentages = [18, 46, 10, 9, 8, 9]
    colors = ['#FF5733', '#C70039', '#900C3F', '#581845', '#FFC300', '#DAF7A6']
    
    fig = px.pie(values=percentages, names=minerals, title='Mars Surface Mineral Composition',
                 color_discrete_sequence=colors)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Home Page
if page == "Home":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo, use_column_width=True)
    
    st.markdown("<h1 class='main-header'>Welcome to Traxler Technology</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Pioneering Mars Mineral Exploration and Utilization</h2>", unsafe_allow_html=True)
    
    # Mission Statement
    st.write(
        """
        Traxler Technology is at the forefront of Mars mineral exploration and utilization.
        Our mission is to unlock the resource potential of the Red Planet, paving the way for future Mars colonization efforts.
        """
    )
    
    # Interactive Mars Map
    st.markdown("<h2 class='sub-header'>Explore Mars</h2>", unsafe_allow_html=True)
    st.write("Interact with our Mars map to explore potential mineral-rich areas and key geological features of the Red Planet.")
    
    mars_map = create_mars_map()
    mars_map.save("mars_map.html")
    st.components.v1.html(open("mars_map.html", 'r').read(), height=400, width=None)
    
    st.markdown("Map data: © OpenPlanetaryMap contributors")

    # Call to Action
    st.header("Join the Mars Mineral Exploration Initiative")
    st.write("Be part of humanity's quest to understand and utilize Martian resources. Sign up for updates on our progress and opportunities to get involved.")
    
    if st.button("Sign Up for Mars Mineral Updates", key="signup"):
        st.success("Thank you for your interest in Mars mineral exploration! We'll keep you updated on our progress.")

# Mars Minerals Page
elif page == "Mars Minerals":
    st.markdown("<h1 class='main-header'>Mars Minerals Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Unlocking the Resource Potential of the Red Planet</h2>", unsafe_allow_html=True)

    st.write("""
    Understanding the mineral composition of Mars is crucial for future exploration and potential colonization efforts. 
    These minerals are key to:
    - Identifying resources for future in-situ resource utilization (ISRU)
    - Studying the geological history of Mars
    - Developing mining and extraction technologies for future missions
    - Supporting scientific research on the formation and evolution of Mars
    """)

    # Overall mineral composition
    st.subheader("Overall Mineral Composition")
    mineral_chart = create_mineral_chart()
    st.plotly_chart(mineral_chart, use_container_width=True)

    # Interactive mineral explorer
    st.subheader("Explore Mars Minerals")
    selected_mineral = st.selectbox(
        "Select a mineral to learn more:",
        ["Iron Oxide", "Silicon Dioxide", "Aluminum Oxide", "Calcium Oxide", "Magnesium Oxide"]
    )
    
    mineral_info = {
        "Iron Oxide": {
            "color": "Red",
            "uses": "Potential source of iron and oxygen",
            "fun_fact": "Gives Mars its distinctive red color"
        },
        "Silicon Dioxide": {
            "color": "Transparent to white",
            "uses": "Can be used to make glass and electronics",
            "fun_fact": "Forms the basis of Martian quartz and sand"
        },
        "Aluminum Oxide": {
            "color": "White",
            "uses": "Used in making ceramics and abrasives",
            "fun_fact": "Can be used to produce aluminum metal"
        },
        "Calcium Oxide": {
            "color": "White",
            "uses": "Important for potential cement production on Mars",
            "fun_fact": "Could be used to regulate soil pH for potential Martian greenhouses"
        },
        "Magnesium Oxide": {
            "color": "White",
            "uses": "Potential use in construction materials",
            "fun_fact": "Could be used in radiation shielding for future Mars structures"
        }
    }
    
    st.write(f"**Color:** {mineral_info[selected_mineral]['color']}")
    st.write(f"**Potential Uses:** {mineral_info[selected_mineral]['uses']}")
    st.write(f"**Fun Fact:** {mineral_info[selected_mineral]['fun_fact']}")

    
    # Call to action
    st.subheader("Join Our Mars Mineral Research Team")
    st.write("Are you passionate about Martian geology and resource utilization? Join our team!")
    if st.button("Apply Now"):
        st.success("Thank you for your interest! We'll be in touch soon with more information about joining our Mars mineral research team.")


# Mars Innovators Hub page
if page == "Mars Innovators Hub":
    st.markdown("<h1 class='main-header'>Mars Innovators Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Share Your Ideas for Mars Exploration and Colonization</h2>", unsafe_allow_html=True)

    # Form for submitting new ideas
    st.subheader("Submit Your Idea")
    idea_title = st.text_input("Idea Title")
    idea_description = st.text_area("Describe your idea")
    if st.button("Submit Idea"):
        if idea_title and idea_description:
            add_idea(idea_title, idea_description)
            st.success("Your idea has been submitted successfully!")
        else:
            st.error("Please provide both a title and description for your idea.")

    # Display existing ideas
    st.subheader("Explore Ideas")
    if not st.session_state.mars_ideas.empty:
        # Sort ideas by votes (descending) and then by timestamp (descending)
        sorted_ideas = st.session_state.mars_ideas.sort_values(['votes', 'timestamp'], ascending=[False, False])
        
        for index, idea in sorted_ideas.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {idea['title']}")
                st.write(idea['description'])
                st.caption(f"Submitted on: {idea['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            with col2:
                st.button(f"👍 {idea['votes']}", key=f"vote_{index}", on_click=vote_idea, args=(index,))
            st.markdown("---")
    else:
        st.write("No ideas submitted yet. Be the first to share your innovative Mars exploration idea!")

    # Add some inspiration
    st.subheader("Need Inspiration?")
    st.write("""
    Here are some areas to consider for your Mars exploration and colonization ideas:
    - Sustainable habitat designs
    - Mars agriculture and food production
    - Energy solutions for Mars colonies
    - Mars transportation systems
    - Scientific research projects on Mars
    - Mars resource utilization
    - Health and medical care on Mars
    - Mars communication systems
    - Martian recreation and entertainment
    - Ethical considerations for Mars colonization
    """)

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
