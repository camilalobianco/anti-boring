import streamlit as st
import pandas as pd
import json
import numpy as np
from sqlite3 import connect

conn = connect('bored_database.db')


st.title('Bored? Let luck help you!')

def load_data():
    query = """
    SELECT activity, type, participants, price, accessibility 
    FROM activities
    """
    df = pd.read_sql_query(query, conn)
    df['price'] = pd.to_numeric(df['price']).apply(lambda x: '{:.2f}'.format(x))
    df['accessibility'] = pd.to_numeric(df['accessibility']).apply(lambda x: '{:.2f}'.format(x))
    df.columns = ['Activity', 'Type', 'Participants', 'Price', 'Accessibility']
    return df

df = load_data()

activities_types = ['Surprise me'] + [type.capitalize() for type in df['Type'].unique()]

option = st.selectbox(
    "Type of activity",
    activities_types,
)


participants = st.select_slider(
    "Select a range of participants",
    options=range(int(df['Participants'].min()), int(df['Participants'].max()) + 1),
    value=(int(df['Participants'].min()), int(df['Participants'].max())),
)

st.write('Being 0 absolutely no money is required and 1 can be quite expensive')
price_range = np.arange(0, 1.05, 0.05)
pricing = st.select_slider(
    "Select a range of price",
    options=price_range,
    value=(0.0, 1.0),
    format_func=lambda x: f'{x:.2f}'
)

st.write('Being 0 realy easy and acessible and 1 can be quite hard and need more resources or time')
accessibility_range = np.arange(0, 1.05, 0.05)
accessibility = st.select_slider(
    "Select a range of accessibility",
    options=accessibility_range,
    value=(0.0, 1.0),
    format_func=lambda x: f'{x:.2f}'
)

if st.button("Submit", use_container_width=True):
    filtered_df = df.copy()
    
    if option != 'Surprise me':
        filtered_df = filtered_df[filtered_df['Type'].str.capitalize() == option]
    
    filtered_df = filtered_df[filtered_df['Participants'].astype(int) <= participants[1]]
    filtered_df = filtered_df[filtered_df['Participants'].astype(int) >= participants[0]]
    
    filtered_df = filtered_df[filtered_df['Price'].astype(float) <= pricing[1]]
    filtered_df = filtered_df[filtered_df['Price'].astype(float) >= pricing[0]]
    
    filtered_df = filtered_df[filtered_df['Accessibility'].astype(float) <= accessibility[1]]
    filtered_df = filtered_df[filtered_df['Accessibility'].astype(float) >= accessibility[0]]
    
    if len(filtered_df) > 0:
        random_activity = filtered_df.sample(n=1)
        
        st.success("Here's your activity suggestion:")
        st.write("Activity:", random_activity['Activity'].iloc[0])
        st.write("Type:", random_activity['Type'].iloc[0])
        st.write("Participants:", random_activity['Participants'].iloc[0])
        st.write("Price:", random_activity['Price'].iloc[0])
        st.write("Accessibility:", random_activity['Accessibility'].iloc[0])
    else:
        st.error("Sorry, no activities found matching your criteria. Try adjusting your filters!")
    
    
