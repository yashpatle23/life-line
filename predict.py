import plotly.graph_objs as go
from sklearn.cluster import KMeans
import pandas as pd
import streamlit as st

def create_Scatterplot_map(df):
    # Define the center and zoom level for the map
    center_lat = 15.05  # Center latitude
    center_lon = 76.8  # Center longitude
    zoom = 6  # Zoom level

    # Perform KMeans clustering on the DataFrame
    kmeans = KMeans(n_clusters=25, random_state=42)
    kmeans.fit(df[['Latitude', 'Longitude']])
    centers = kmeans.cluster_centers_

    # Define the cluster centers and their marker properties
    centers_df = pd.DataFrame(centers, columns=['Latitude', 'Longitude'])
    center_marker_size = 15
    center_marker_color = 'gold'

    # Create Scattermapbox traces for each cluster center with only circle outline
    traces_centers = go.Scattermapbox(
        lon=centers_df['Longitude'],
        lat=centers_df['Latitude'],
        mode='markers',
        marker=dict(
            size=center_marker_size,
            color=center_marker_color,
            opacity=1
        ),
        hoverinfo='text',
        hovertext='Latitude: ' + centers_df['Latitude'].astype(str) + '<br>Longitude: ' + centers_df['Longitude'].astype(str)+'<br> <a href="https://www.gps-coordinates.net/street-view/@' + centers_df['Latitude'].astype(str) + ',' + centers_df['Longitude'].astype(str) + ',h237,p9,z1">Open Street View</a>'
        
    )

    # Create the layout for the map
    layout = go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        width=1000,
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
            center=dict(lat=center_lat, lon=center_lon),
            style='dark',
            zoom=zoom
        ),
        autosize=True
    )

    # Create the figure including both original data and cluster centers
    fig = go.Figure(data=[traces_centers], layout=layout)

    # Add a custom data URL to each marker
    for idx, row in centers_df.iterrows():
        lon = row['Longitude']
        lat = row['Latitude']
        url = f"https://www.gps-coordinates.net/street-view/@{lon},{lat},h237,p9,z1"
        fig.add_annotation(
            x=row['Longitude'],
            y=row['Latitude'],
            text=f'<a href="{url}" target="_blank">Open Street View</a>',
            showarrow=False,
            font=dict(color='white', size=10),
        )

    return fig

