import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.title("Transport Map Demo")

# Example transport stops
data = {
    "Name": ["Bus Stop A", "Bus Stop B", "Train Station"],
    "Latitude": [1.3521, 1.3550, 1.3600],
    "Longitude": [103.8198, 103.8205, 103.8300]
}
df = pd.DataFrame(data)

# Create map
m = folium.Map(location=[1.3521, 103.8198], zoom_start=13)

# Add markers
for i, row in df.iterrows():
    folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Name"]).add_to(m)

# Display map
st_folium(m, width=700, height=500)
