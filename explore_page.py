
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
import plotly.express as px
import seaborn as sns
import statsmodels
import plotly.graph_objects as go


df = pd.read_csv("df_good_for_models.csv")

@st.cache_data
def show_explore_page():
    
    st.markdown(
    """
    <style>
    .title {
        font-size: 2.6em;       
        font-weight: bold; 
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Title
    st.markdown('<div class="title"> Explore Tesla Pre-Owned EV Trends</div>', unsafe_allow_html=True)

    st.divider()

    st.write("""
             #### Based on Tesla Model Listings on the Markets in Canada
    """)

    st.write("Last update: Nov , 2024")
    
    # DataFrame Filtering
    model3_df = df[df['model']=='Model 3']
    models_df = df[df['model']=='Model S']
    modelx_df = df[df['model']=='Model X']
    modely_df = df[df['model']=='Model Y']

    # Price Distribution 
    st.write(
        """ 
    #### Tesla Models: Price Distributions
    """
    )
    fig = go.Figure()
    fig.add_trace(go.Box(y = model3_df['price'], name='Model 3',
                    marker_color = 'blue'))
    fig.add_trace(go.Box(y = modelx_df['price'], name = 'Model X',
                    marker_color = 'indianred'))
    fig.add_trace(go.Box(y = models_df['price'], name = 'Model S',
                    marker_color = 'lightseagreen'))
    fig.add_trace(go.Box(y = modely_df['price'], name = 'Model Y',
                    marker_color = 'purple'))
    fig.update_layout(
    yaxis_title='price', 
    )   
    st.plotly_chart(fig)


    # Plot - Year Vs. Price
    st.write(
        """ 
    #### Tesla Models: Year Vs. Price
    """
    )
    fig10 = px.scatter(df, 
                 y="price", 
                 x="year",
                 color="model",
                 opacity=0.65,
                 trendline_color_override='darkblue',
                 color_discrete_sequence=px.colors.qualitative.Plotly)   
    fig10.update_xaxes(title_text='Year', title_font=dict(size=14))
    fig10.update_yaxes(title_text='Price', title_font=dict(size=14))

    st.plotly_chart(fig10)

    # Plot - Mileage vs. Price
    st.write(
        """ 
    #### Tesla Models: Mileage vs. Price
    """
    )
    fig1 = px.scatter(df, 
                 y="price", 
                 x="mileage(km)", 
                 color="model",
                 opacity=0.75,
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_xaxes(title_text='Mileage (km)', title_font=dict(size=14))
    fig1.update_yaxes(title_text='Price', title_font=dict(size=14))

    st.plotly_chart(fig1)


    # Plot- Battery Range vs. Price
    st.write(
        """ 
    #### Tesla Models: Battery Range vs. Price
    """
    )

    fig2 = px.scatter(df, 
                 y="price", 
                 x="battery_range(km)",
                 trendline='ols',
                 opacity=0.65,
                 trendline_color_override='darkblue',
                 color_discrete_sequence=px.colors.qualitative.Plotly)   
    fig2.update_xaxes(title_text='Battery Range (km)', title_font=dict(size=14))
    fig2.update_yaxes(title_text='Price', title_font=dict(size=14))

    st.plotly_chart(fig2)


    # Plot- Battery Charge Time vs. Price
    st.write(
        """ 
    #### Tesla Models: Battery Charge Time vs. Price
    """
    )

    fig2 = px.scatter(df, 
                 y="price", 
                 x="battery_charge_time(hr)",
                 trendline='ols',
                 opacity=0.65,
                 trendline_color_override='darkblue',
                 color_discrete_sequence=px.colors.qualitative.Plotly)   
    fig2.update_xaxes(title_text='Battery Charge Time(hr)', title_font=dict(size=14))
    fig2.update_yaxes(title_text='Price', title_font=dict(size=14))

    st.plotly_chart(fig2)



    # Implot - Year vs Price
    st.write(
        """ 
    #### Tesla Models: Year vs. Price
    """
    )
    year_df = df[df['year']>=2012]
    fig3 = px.scatter(year_df, 
                 y="price", 
                 x="year",
                 trendline='ols',
                 opacity=0.65,
                 trendline_color_override='darkblue',
                 color_discrete_sequence=px.colors.qualitative.Plotly)   
    fig3.update_xaxes(title_text='Year', title_font=dict(size=14))
    fig3.update_yaxes(title_text='Price', title_font=dict(size=14))

    st.plotly_chart(fig3)

    st.write(
        """ 
    #### Tesla Models: Year (2021-2014) vs. Price
    """
    )

    fig = go.Figure()

    recent_df = df[df['year']>=2021]

    model3_recent_df= recent_df[recent_df['model']=='Model 3']
    models_recent_df= recent_df[recent_df['model']=='Model S']
    modelx_recent_df= recent_df[recent_df['model']=='Model X']
    modely_recent_df= recent_df[recent_df['model']=='Model Y']

    fig.add_trace(go.Box(
        y=model3_recent_df['price'],
        x=recent_df['year'],
        name='Model 3',
        marker_color='blue',
        opacity=0.65
    ))
    fig.add_trace(go.Box(
        y=models_recent_df['price'],
        x=recent_df['year'],
        name='Model S',
        marker_color='indianred',
        opacity=0.65
    ))
    fig.add_trace(go.Box(
        y=modelx_recent_df['price'],
        x=recent_df['year'],
        name='Model X',
        marker_color='lightseagreen',
        opacity=0.65
    ))
    fig.add_trace(go.Box(
        y=modely_recent_df['price'],
        x=recent_df['year'],
        name='Model Y',
        marker_color='purple',
        opacity=0.65
    ))

    fig.update_layout(
    yaxis=dict(
        title=dict(
            text='Price')
    ),
    boxmode='group' # group together boxes of the different traces for each value of x
    )
    st.plotly_chart(fig)


    