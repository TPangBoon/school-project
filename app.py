import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("Interactive Transport Map Demo")

# --- Example transport stops data ---
data = {
    "Name": ["Bus Stop A", "Bus Stop B", "Train Station"],
    "Latitude": [1.3521, 1.3550, 1.3600],
    "Longitude": [103.8198, 103.8205, 103.8300]
}
df = pd.DataFrame(data)

# --- Example chart data ---
chart_df = pd.DataFrame({
    "Stop": ["Bus Stop A", "Bus Stop B", "Train Station"],
    "Passengers": [120, 80, 200],
    "Transport_Type": ["Bus", "Bus", "Train"]
})

traffic_df = pd.DataFrame({
    "Stop": ["Bus Stop A"]*17 + ["Bus Stop B"]*17 + ["Train Station"]*17,
    "Hour": list(range(6,23))*3,
    "Traffic": [50,70,120,180,250,300,320,280,230,180,140,100,70,50,30,20,10,
                40,60,100,150,200,220,250,230,200,150,120,90,60,40,20,15,10,
                80,90,150,200,300,320,350,300,250,200,180,150,120,100,70,50,30]
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
    # --- Interactive widget to select stop ---
    selected_stop = st.selectbox("Select a Station:", df["Name"].tolist() + ["All Stops"])

    # Filter data based on selection
    if selected_stop != "All Stops":
        filtered_chart_df = chart_df[chart_df["Stop"] == selected_stop]
        filtered_traffic_df = traffic_df[traffic_df["Stop"] == selected_stop]
    else:
        filtered_chart_df = chart_df
        filtered_traffic_df = traffic_df.groupby("Hour").sum().reset_index()

    st.subheader("Passengers per Stop")
    st.bar_chart(filtered_chart_df.set_index("Stop")["Passengers"])

    st.subheader("Transport Type Proportion")
    transport_counts = filtered_chart_df["Transport_Type"].value_counts()
    fig = px.pie(
        names=transport_counts.index,
        values=transport_counts.values,
        title="Transport Type Proportion"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Traffic Flow Over Time")
    st.line_chart(filtered_traffic_df.set_index("Hour")["Traffic"])
