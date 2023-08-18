import streamlit as st
import tv_page
import speaker_page
import vaccum_page
import time
import numpy as np
import altair as alt

logo_image = st.sidebar.image("group_logo.png", width=200, use_column_width=True)
input_style = """
    <style>
        .stTextInput input {
            font-size: 20px;       /* Adjust the font size as needed */
            padding: 10px;         /* Adjust padding as needed */
            width: 100%;           /* Ensure the input spans the full width */
            word-wrap: break-word; /* Allow text to wrap to the next line */
        }
    </style>
"""

# Display the CSS style
st.sidebar.markdown(input_style, unsafe_allow_html=True)

# Display the text input with the defined style
user_input = st.sidebar.text_input("Enter your product:", key="user_input",)
send_button = st.sidebar.button("Send", key="send_button")

st.sidebar.markdown(
    """
    <script>
        document.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                document.querySelector("#send_button button").click();
            }
        });
    </script>
    """,
    unsafe_allow_html=True,
)


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
        chart = alt.Chart(data_filtered).mark_bar().encode(
            alt.X(selected_attribute, bin=True),
            alt.Y('count()'),
        ).properties(
            width=600,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)


# Add page selection to the sidebar
page_options = ["TV", "Speaker", "Vacuum"]
selected_page = st.sidebar.selectbox("Select a page", page_options)

if send_button and user_input:
    # classification = classify_product(user_input)
    time.sleep(2)
    classification = np.random.choice(['TV', 'Speaker', 'Vacuum'])

    if classification == "TV":
        selected_page = "TV"
    elif classification == "Speaker":
        selected_page = "Speaker"
    elif classification == "Vacuum":
        selected_page = "Vacuum"

# Main content based on the selected page
if selected_page == "TV":
    tv_page.show_tv_page()
elif selected_page == "Speaker":
    speaker_page.show_speaker_page()
elif selected_page == "Vacuum":
    vaccum_page.show_vacuum_page()
