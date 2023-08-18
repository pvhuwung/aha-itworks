import streamlit as st
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import altair as alt
import drawFunc


def show_tv_page():
    # Add a slider to the sidebar
    data = pd.read_csv("screen.csv")

    cols_to_plot = data.columns[4:]
    numerical_cols = data[cols_to_plot].select_dtypes(include=['int', 'float']).columns
    non_numerical_cols = data[cols_to_plot].select_dtypes(exclude=['int', 'float']).columns

    histo_tab, bubble_tab, chatbot_tab, histo_tab_2 = st.tabs(["Histogram", "Bubble", "Chatbot", "Histogram 2"])

    with histo_tab:
        drawFunc.drawHisto("screen.csv")

    with bubble_tab:
        import plotly.graph_objects as go
        # import plotly.express as px
        import math

        hover_text = []
        bubble_size = []

        for index, row in data.iterrows():
            hover_text.append(('Brand: {brand}<br>' +
                               'Price (SGD): {price}<br>' +
                               'Screen Size (inches): {screen_size}<br>' +
                               'Resolution: {resolution}').format(brand=row['brand'],
                                                                  price=row['price_sgd'],
                                                                  screen_size=row['screen_size_inches'],
                                                                  resolution=row['resolution']))
            bubble_size.append(math.sqrt(row['price_sgd']))

        data['text'] = hover_text
        data['size'] = bubble_size
        sizeref = 2. * max(data['size']) / (100 ** 2)

        # Dictionary with dataframes for each category (e.g., brand, resolution, etc.)
        category_names = data['brand'].unique()  # Replace with your own attribute
        category_data = {category: data.query("brand == '%s'" % category)
                         for category in category_names}

        # Create figure
        fig = go.Figure()

        for category_name, category in category_data.items():
            fig.add_trace(go.Scatter(
                x=category['screen_size_inches'], y=category['price_sgd'],
                name=category_name, text=category['text'],
                marker_size=category['size'],
            ))

        # Tune marker appearance and layout
        fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                      sizeref=sizeref, line_width=2))

        fig.update_layout(
            title='   Price vs. Screen Size for Different Brands',
            xaxis=dict(
                title='Screen Size (inches)',
                gridcolor='white',
                gridwidth=2,
            ),
            yaxis=dict(
                title='Price (SGD)',
                gridcolor='white',
                gridwidth=2,
            ),
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
        )
        # fig.show()
        st.plotly_chart(fig, use_container_width=True)

    with chatbot_tab:
        pass

    with histo_tab_2:
        import plotly.figure_factory as ff

        selected_attribute = st.radio(label="Select an Attribute", options=numerical_cols, horizontal=True)
        brands_list = data['brand'].unique()
        brands_dict = {brand: data[data['brand'] == brand] for brand in brands_list}

        hist_data = [brands_dict[brand][selected_attribute].dropna(axis=0) for brand in brands_list]
        group_labels = brands_list

        histo_fig_2 = ff.create_distplot(hist_data, group_labels)
        st.plotly_chart(histo_fig_2, use_container_width=True)
