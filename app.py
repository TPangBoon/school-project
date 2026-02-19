import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")  # Make full-width layout
st.title("Transport Map Demo")

# --- Example transport stops data ---
st.subheader("Map of Transport Stops")
data = {
    "Name": ["Bus Stop A", "Bus Stop B", "Train Station"],
    "Latitude": [1.3521, 1.3550, 1.3600],
    "Longitude": [103.8198, 103.8205, 103.8300]
}
df = pd.DataFrame(data)

# --- Example chart data (placeholder) ---
chart_df = pd.DataFrame({
    "Stop": ["Bus Stop A", "Bus Stop B", "Train Station"],
    "Passengers": [120, 80, 200],
    "Transport_Type": ["Bus", "Bus", "Train"]
})

traffic_df = pd.DataFrame({
    "Hour": list(range(6, 23)),
    "Traffic": [50, 70, 120, 180, 250, 300, 320, 280, 230, 180, 140, 100, 70, 50, 30, 20, 10]
})

# --- Layout: Map + Charts ---
col1, col2 = st.columns([2, 1])

# Left column: Map
with col1:
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=13)
    for i, row in df.iterrows():
        folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Name"]).add_to(m)
    st_folium(m, width=700, height=500)

# Right column: Charts
with col2:
    st.subheader("Passengers per Stop")
    st.bar_chart(chart_df.set_index("Stop")["Passengers"])

    st.subheader("Transport Type Proportion")
    transport_counts = chart_df["Transport_Type"].value_counts()
    fig = px.pie(
        names=transport_counts.index,
        values=transport_counts.values,
        title="Transport Type Proportion"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Traffic Flow Over Time")
    st.line_chart(traffic_df.set_index("Hour")["Traffic"])
