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

# Add a background image (uncomment and provide the correct path)
# add_bg_from_local('assets/mars_background.jpg')

# Custom CSS for improved design
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        color: #333;
        background-color: #f5f5f5;
    }

    .main-header {
        font-size: 2.5em;
        font-weight: 700;
        color: #dd4b39;
        text-align: center;
        padding: 20px 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .sub-header {
        font-size: 1.5em;
        font-weight: 400;
        color: #666;
        text-align: center;
        padding-bottom: 20px;
    }

    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #dd4b39;
        padding: 15px 0;
        border-bottom: 2px solid #dd4b39;
        margin-bottom: 20px;
    }

    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }

    .stButton>button {
        background-color: #dd4b39;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #c53727;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    .fullwidth {
        width: 100%;
        height: 600px;
        margin: 0 auto;
        display: block;
    }

    .card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }

    .idea-card {
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }

    .idea-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Load the logo image
logo = Image.open('love.png')

# Sidebar configuration
st.sidebar.image(logo, use_column_width=True)
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Mars Minerals", "Mars Innovators Hub", "Mars Data Explorer", "About Us"],
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

    # Add markers for important Mars locations
    locations = [
        {"name": "Olympus Mons", "coords": [18.65, -133.8], "info": "Largest known volcano in the Solar System"},
        {"name": "Valles Marineris", "coords": [-14, -59], "info": "Largest canyon in the Solar System"},
        {"name": "Gale Crater", "coords": [-5.4, 137.8], "info": "Landing site of the Curiosity rover"},
        {"name": "Jezero Crater", "coords": [18.38, 77.58], "info": "Landing site of the Perseverance rover"}
    ]

    for loc in locations:
        folium.Marker(
            loc["coords"],
            popup=f"<b>{loc['name']}</b><br>{loc['info']}",
            tooltip=loc["name"]
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
    fig.update_layout(
        title_font_size=24,
        legend_title_font_size=14,
        legend_font_size=12
    )
    return fig

# Home Page
if page == "Home":
    st.markdown("<h1 class='main-header'>Welcome to Traxler Technology</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Pioneering Mars Mineral Exploration and Utilization</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class='card'>
            <h3>Our Mission</h3>
            <p>Traxler Technology is at the forefront of Mars mineral exploration and utilization. 
            Our mission is to unlock the resource potential of the Red Planet, paving the way for future Mars colonization efforts.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class='card'>
            <h3>Latest News</h3>
            <ul>
                <li>Traxler Tech secures major funding for Mars mineral mapping project</li>
                <li>New breakthrough in Martian soil analysis techniques</li>
                <li>Collaboration announced with NASA for future Mars missions</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("<h3 class='section-header'>Explore Mars</h3>", unsafe_allow_html=True)
        st.write("Interact with our Mars map to explore potential mineral-rich areas and key geological features of the Red Planet.")
        mars_map = create_mars_map()
        mars_map.save("mars_map.html")
        st.components.v1.html(open("mars_map.html", 'r').read(), height=400)
        st.caption("Map data: © OpenPlanetaryMap contributors")

    st.markdown("<h3 class='section-header'>Join the Mars Mineral Exploration Initiative</h3>", unsafe_allow_html=True)
    st.write("Be part of humanity's quest to understand and utilize Martian resources. Sign up for updates on our progress and opportunities to get involved.")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("Enter your email address")
        if st.button("Sign Up for Updates"):
            if email:
                st.success(f"Thank you for signing up! We'll keep {email} updated on our Mars exploration progress.")
            else:
                st.error("Please enter a valid email address.")

# Mars Minerals Page
elif page == "Mars Minerals":
    st.markdown("<h1 class='main-header'>Mars Minerals Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Unlocking the Resource Potential of the Red Planet</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class='card'>
            <h3>Why Mars Minerals Matter</h3>
            <p>Understanding the mineral composition of Mars is crucial for future exploration and potential colonization efforts. 
            These minerals are key to:</p>
            <ul>
                <li>Identifying resources for future in-situ resource utilization (ISRU)</li>
                <li>Studying the geological history of Mars</li>
                <li>Developing mining and extraction technologies for future missions</li>
                <li>Supporting scientific research on the formation and evolution of Mars</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("<h3 class='section-header'>Overall Mineral Composition</h3>", unsafe_allow_html=True)
        mineral_chart = create_mineral_chart()
        st.plotly_chart(mineral_chart, use_container_width=True)

    st.markdown("<h3 class='section-header'>Explore Mars Minerals</h3>", unsafe_allow_html=True)
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
    
    st.markdown(
        f"""
        <div class='card'>
        <h4>{selected_mineral}</h4>
        <p><strong>Color:</strong> {mineral_info[selected_mineral]['color']}</p>
        <p><strong>Potential Uses:</strong> {mineral_info[selected_mineral]['uses']}</p>
        <p><strong>Fun Fact:</strong> {mineral_info[selected_mineral]['fun_fact']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h3 class='section-header'>Join Our Mars Mineral Research Team</h3>", unsafe_allow_html=True)
    st.write("Are you passionate about Martian geology and resource utilization? Join our team!")
    if st.button("Apply Now"):
        st.success("Thank you for your interest! We'll be in touch soon with more information about joining our Mars mineral research team.")


# Mars Innovators Hub page
elif page == "Mars Innovators Hub":
    st.markdown("<h1 class='main-header'>Mars Innovators Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Share Your Ideas for Mars Exploration and Colonization</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class='section-header'>Submit Your Idea</h3>", unsafe_allow_html=True)
        idea_title = st.text_input("Idea Title")
        idea_description = st.text_area("Describe your idea")
        if st.button("Submit Idea"):
            if idea_title and idea_description:
                add_idea(idea_title, idea_description)
                st.success("Your idea has been submitted successfully!")
            else:
                st.error("Please provide both a title and description for your idea.")

    with col2:
        st.markdown("<h3 class='section-header'>Need Inspiration?</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='card'>
            <p>Here are some areas to consider for your Mars exploration and colonization ideas:</p>
            <ul>
                <li>Sustainable habitat designs</li>
                <li>Mars agriculture and food production</li>
                <li>Energy solutions for Mars colonies</li>
                <li>Mars transportation systems</li>
                <li>Scientific research projects on Mars</li>
                <li>Mars resource utilization</li>
                <li>Health and medical care on Mars</li>
                <li>Mars communication systems</li>
                <li>Martian recreation and entertainment</li>
                <li>Ethical considerations for Mars colonization</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<h3 class='section-header'>Explore Ideas</h3>", unsafe_allow_html=True)
    if not st.session_state.mars_ideas.empty:
        # Sort ideas by votes (descending) and then by timestamp (descending)
        sorted_ideas = st.session_state.mars_ideas.sort_values(['votes', 'timestamp'], ascending=[False, False])
        
        for index, idea in sorted_ideas.iterrows():
            st.markdown(
                f"""
                <div class='idea-card'>
                <h4>{idea['title']}</h4>
                <p>{idea['description']}</p>
                <p><small>Submitted on: {idea['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"👍 Upvote ({idea['votes']})", key=f"vote_{index}"):
                    vote_idea(index)
                    st.experimental_rerun()
    else:
        st.info("No ideas submitted yet. Be the first to share your innovative Mars exploration idea!")

# Mars Data Explorer page
elif page == "Mars Data Explorer":
    st.markdown("<h1 class='main-header'>Mars Data Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Analyze and Visualize Mars Data</h2>", unsafe_allow_html=True)

    # Simulated Mars data
    @st.cache_data
    def load_mars_data():
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        temperature = np.random.normal(-63, 15, size=len(dates))  # Average temperature on Mars is about -63°C
        pressure = np.random.normal(600, 50, size=len(dates))  # Average pressure on Mars is about 600 Pascals
        wind_speed = np.random.normal(10, 5, size=len(dates))  # Wind speeds on Mars can vary
        
        df = pd.DataFrame({
            'Date': dates,
            'Temperature (°C)': temperature,
            'Pressure (Pa)': pressure,
            'Wind Speed (m/s)': wind_speed
        })
        return df

    mars_data = load_mars_data()

    st.markdown("<h3 class='section-header'>Mars Weather Data</h3>", unsafe_allow_html=True)
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min(mars_data['Date']), min_value=min(mars_data['Date']), max_value=max(mars_data['Date']))
    with col2:
        end_date = st.date_input("End Date", max(mars_data['Date']), min_value=min(mars_data['Date']), max_value=max(mars_data['Date']))

    filtered_data = mars_data[(mars_data['Date'] >= pd.Timestamp(start_date)) & (mars_data['Date'] <= pd.Timestamp(end_date))]

    # Data visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Temperature (°C)'], name='Temperature'))
    fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Pressure (Pa)'], name='Pressure', yaxis='y2'))
    fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Wind Speed (m/s)'], name='Wind Speed', yaxis='y3'))

    fig.update_layout(
        title='Mars Weather Data',
        yaxis=dict(title='Temperature (°C)'),
        yaxis2=dict(title='Pressure (Pa)', overlaying='y', side='right'),
        yaxis3=dict(title='Wind Speed (m/s)', overlaying='y', side='right'),
        legend=dict(x=1.1, y=1),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Data statistics
    st.markdown("<h3 class='section-header'>Data Statistics</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_data.describe())

    # Download data option
    st.markdown("<h3 class='section-header'>Download Data</h3>", unsafe_allow_html=True)
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download Mars Data as CSV",
        data=csv,
        file_name="mars_weather_data.csv",
        mime="text/csv",
    )

# About Us
elif page == "About Us":
    st.markdown("<h1 class='main-header'>About Traxler Technology</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("new.png", width=200, caption="Caleb Traxler - Founder & CEO")

    with col2:
        st.markdown(
            """
            <div class='card'>
            <h3>Our Mission</h3>
            <p>At Traxler Technology, our mission is to advance humanity's reach into the cosmos by pioneering
            innovative solutions for Mars exploration and colonization. We believe in a future where humans
            live and thrive on multiple planets.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='card'>
            <h3>Our Founder</h3>
            <p>Caleb Traxler, Founder & CEO of Traxler Technology, is a visionary entrepreneur with a passion for space exploration and technology. 
            With a comprehensive academic background in Machine Learning and Artificial Intelligence, Caleb founded Traxler Technology to bring the dream of 
            Mars colonization closer to reality.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='card'>
            <h3>Our Team</h3>
            <p>We are a team of passionate engineers, scientists, and visionaries dedicated to making Mars
            colonization a reality. Our diverse backgrounds and expertise enable us to tackle the complex
            challenges of interplanetary travel and settlement.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<h3 class='section-header'>Contact Us</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class='card'>
            <p><strong>Email:</strong> <a href="mailto:traxlertechnology@gmail.com">traxlertechnology@gmail.com</a></p>
            <p><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/company/traxlertech" target="_blank">Traxler Technology</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class='card'>
            <h4>Send us a message</h4>
            <form>
                <input type="text" placeholder="Your Name" style="width: 100%; margin-bottom: 10px; padding: 5px;">
                <input type="email" placeholder="Your Email" style="width: 100%; margin-bottom: 10px; padding: 5px;">
                <textarea placeholder="Your Message" style="width: 100%; height: 100px; margin-bottom: 10px; padding: 5px;"></textarea>
                <button style="background-color: #dd4b39; color: white; border: none; padding: 10px 20px; cursor: pointer;">Send Message</button>
            </form>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center; padding: 20px;'>
        <p>&copy; 2024 Traxler Technology. All rights reserved.</p>
        <p>
            <a href="#" style="color: #dd4b39; text-decoration: none; margin: 0 10px;">Privacy Policy</a> |
            <a href="#" style="color: #dd4b39; text-decoration: none; margin: 0 10px;">Terms of Service</a> |
            <a href="#" style="color: #dd4b39; text-decoration: none; margin: 0 10px;">Careers</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
