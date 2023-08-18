import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.markdown('# <span style="color:#0CAD92">It Works (Maybe)</span>', unsafe_allow_html=True)

def drawHisto(data_path):
    data = pd.read_csv(data_path)

    cols_to_plot = data.columns[4:]
    numerical_cols = data[cols_to_plot].select_dtypes(include=['int', 'float']).columns

    # Use st.sidebar to create a slider in the sidebar
    min_price, max_price = st.sidebar.slider(label="Price range (SGD)",
                                             value=(np.min(data['price_sgd']), np.max(data['price_sgd'])),
                                             min_value=np.min(data['price_sgd']),
                                             max_value=np.max(data['price_sgd']))

    data_filtered = data[(data['price_sgd'] >= min_price) & (data['price_sgd'] <= max_price)]

    for selected_attribute in numerical_cols:
        st.write(f"## Histogram for {selected_attribute}")

        # Create Altair histogram
        chart = alt.Chart(data_filtered).mark_bar(color='#33b343').encode(
            alt.X(selected_attribute, bin=True),
            alt.Y('count()'),
        ).properties(
            width=600,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)

# Streamlit UI
data_path = "screen.csv"
drawHisto(data_path)
