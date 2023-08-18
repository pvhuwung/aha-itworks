import numpy as np
import pandas as pd
import os
import json
import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st

# # Custom CSS styles for the menu/taskbar
# st.markdown(
#     """
#     <style>
#     .menu {
#         display: flex;
#         justify-content: space-between;
#         background-color: #3498db;
#         color: white;
#         padding: 10px 20px;
#         border-bottom: 2px solid #2980b9;
#     }
#
#     .menu-item {
#         margin-right: 20px;
#         font-size: 18px;
#         font-weight: bold;
#         cursor: pointer;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # Menu/taskbar content
# st.markdown('<div class="menu">'
#             '<div class="menu-item">Home</div>'
#             '<div class="menu-item">About</div>'
#             '<div class="menu-item">Services</div>'
#             '<div class="menu-item">Contact</div>'
#             '</div>', unsafe_allow_html=True)


st.markdown('# <span style="color:#0CAD92">It Works (Maybe)</span>', unsafe_allow_html=True)
data = pd.read_csv("screen.csv")

cols_to_plot = data.columns[4:]
numerical_cols = data[cols_to_plot].select_dtypes(include=['int', 'float']).columns
non_numerical_cols = data[cols_to_plot].select_dtypes(exclude=['int', 'float']).columns

histo_tab, bubble_tab, chatbot_tab, histo_tab_2 = st.tabs(["Histogram", "Bubble", "Chatbot", "Histogram 2"])
with histo_tab:
    selected_attribute = st.radio(label="Select Attribute", options=numerical_cols, horizontal=True)

    fig, ax = plt.subplots(figsize=(10, 4.5))

    # for column in numerical_cols[0:1]:
    column = selected_attribute
    min_price, max_price = st.slider(label="Range", value=(np.min(data[column]), np.max(data[column])),
                                     min_value=np.min(data[column]), max_value=np.max(data[column]))
    value_counts = data[column].value_counts()
    data_ = data[(data[column] >= min_price) & (data[column] <= max_price)]
    data_[column].plot(kind='hist', bins=20, edgecolor='black')
    st.pyplot(fig, use_container_width=True)

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
