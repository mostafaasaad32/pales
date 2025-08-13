import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



df=pd.read_csv(r'C:\My Career\AI _Data Science\My Work\Excel&power pi\pales\fatalities_isr_pse_conflict_2000_to_2023Edited.csv')


st.set_page_config(page_title='Fatalities in the Israeli-Palestinian',page_icon="🇵🇸",
    layout="wide", 
    initial_sidebar_state="expanded")

st.title("Fatalities in the Israeli-Palestinian")
st.header("Fatalities in the Israeli-Palestinian")
st.sidebar.title("Fatalities in the Israeli-Palestinian Dashboard")
event_location=st.sidebar.multiselect("Select event location",options=df['event_location'].unique(),default=sorted(df['event_location'].unique()))
event_location_district=st.sidebar.multiselect("Select event location",options=df['event_location_district'].unique(),default=sorted(df['event_location_district'].unique()))
event_location_region=st.sidebar.multiselect("Select event location",options=df['event_location_region'].unique(),default=sorted(df['event_location_region'].unique()))



df['date_of_death'] = pd.to_datetime(df['date_of_death'], errors='coerce')


min_date = df['date_of_death'].min().date()
max_date = df['date_of_death'].max().date()


start_date, end_date = st.slider(
    "Select Date of Death range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)


filtered_df = df[
    (df['event_location'].isin(event_location)) &
    (df['event_location_district'].isin(event_location_district)) &
    (df['event_location_region'].isin(event_location_region)) &
    (df['date_of_death'].dt.date >= start_date) &
    (df['date_of_death'].dt.date <= end_date)
]
tab1, tab2, tab3 = st.tabs([
    "🔎 Overview",
    "![Palestine Flag](https://flagcdn.com/w20/ps.png) Palestine",
    "![Israel Flag](https://flagcdn.com/w20/il.png) The Zionist entity"
])


gender_counts = filtered_df['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']


z = filtered_df[
    (filtered_df['took_part_in_the_hostilities'] == 'No') |
    (filtered_df['took_part_in_the_hostilities'] == 'Object of targeted killing')
].groupby('citizenship')['took_part_in_the_hostilities'].value_counts().reset_index()


e=filtered_df['killed_by'].value_counts().reset_index()



with tab1 :
    
    col1,col2,col3=st.columns(3)
    with col1:
       
       fig = px.pie(
            data_frame=gender_counts,
            names='gender',
            values='count',
            title="Gender Distribution",
            color_discrete_sequence=px.colors.sequential.RdBu)
       st.plotly_chart(fig, use_container_width=True)

       
    with col2 :
         fig2 = px.bar(
         data_frame=z,
         x='citizenship',
            y='count',
          color='took_part_in_the_hostilities',
          hover_data=['took_part_in_the_hostilities'],
           barmode='group',  
           title='Fatalities by Citizenship and Hostilities Participation'
                                 )
         st.plotly_chart(fig2, use_container_width=True)

    with col3:
         fig3=px.histogram(data_frame=e,x='killed_by',y='count')
         st.plotly_chart(fig3, use_container_width=True) 

with tab2:
    palestine_df = filtered_df[filtered_df['citizenship'] == 'Palestinian']

    st.subheader("![Palestine Flag](https://flagcdn.com/w20/ps.png) Palestine Fatalities Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Deaths", len(palestine_df))
    with col2:
        st.metric("Date Range", f"{palestine_df['date_of_death'].min().date()} → {palestine_df['date_of_death'].max().date()}")

    col1, col2 = st.columns(2)

    with col1:
        fig_age_pal = px.histogram(
            palestine_df,
            x="age",
            nbins=20,
            title="Age Distribution - Palestine",
            color_discrete_sequence=['#d62728']
        )
        st.plotly_chart(fig_age_pal, use_container_width=True)

    with col2:
        ammo_pal = palestine_df['ammunition'].value_counts().reset_index()
        ammo_pal.columns = ['Ammunition', 'Count']
        ammo_pal = ammo_pal.sort_values('Count', ascending=False)
        fig_ammo_pal = px.bar(
            ammo_pal,
            x='Ammunition',
            y='Count',
            title="Ammunition Types Used - Palestine",
            color='Count',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_ammo_pal, use_container_width=True)

    injury_pal = palestine_df['type_of_injury'].value_counts().reset_index()
    injury_pal.columns = ['Type of Injury', 'Count']
    injury_pal = injury_pal.sort_values('Count', ascending=False)
    fig_injury_pal = px.bar(
        injury_pal,
        x='Type of Injury',
        y='Count',
        title="Type of Injury - Palestine",
        color='Count',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_injury_pal, use_container_width=True)



with tab3:
    israel_df = filtered_df[filtered_df['citizenship'] == 'Israeli']

    st.subheader("![The Zionist entity Flag](https://flagcdn.com/w20/il.png) The Zionist entity Fatalities Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Deaths", len(israel_df))
    with col2:
        st.metric("Date Range", f"{israel_df['date_of_death'].min().date()} → {israel_df['date_of_death'].max().date()}")

    col1, col2 = st.columns(2)

    with col1:
        fig_age_isr = px.histogram(
            israel_df,
            x="age",
            nbins=20,
            title="Age Distribution - Israel",
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig_age_isr, use_container_width=True)

    with col2:
        ammo_isr = israel_df['ammunition'].value_counts().reset_index()
        ammo_isr.columns = ['Ammunition', 'Count']
        ammo_isr = ammo_isr.sort_values('Count', ascending=False)
        fig_ammo_isr = px.bar(
            ammo_isr,
            x='Ammunition',
            y='Count',
            title="Ammunition Types Used - Israel",
            color='Count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_ammo_isr, use_container_width=True)

  
    injury_isr = israel_df['type_of_injury'].value_counts().reset_index()
    injury_isr.columns = ['Type of Injury', 'Count']
    injury_isr = injury_isr.sort_values('Count', ascending=False)
    fig_injury_isr = px.bar(
        injury_isr,
        x='Type of Injury',
        y='Count',
        title="Type of Injury - Israel",
        color='Count',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_injury_isr, use_container_width=True)

  
