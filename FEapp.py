import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title('Snowflake Consumption Tracker')

# Sidebar for user input
with st.sidebar:
    st.header('Add Customer Consumption')
    customer_name = st.text_input('Customer Name')
    consumption_amount = st.number_input('Monthly Consumption Amount ($)', min_value=0.0, format='%f')
    consumption_month = st.date_input('Month', datetime.now()).strftime('%Y-%m')
    submit_button = st.button('Submit')

# Initialize the DataFrame if it doesn't exist in the session state
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Customer', 'Month', 'Consumption'])

# Handle the submit action
if submit_button:
    new_data = {'Customer': customer_name, 'Month': consumption_month, 'Consumption': consumption_amount}
    # Append the new data to the DataFrame
    st.session_state['data'] = st.session_state['data'].append(new_data, ignore_index=True)

# Display the data
st.subheader('Monthly Consumption Data')
st.dataframe(st.session_state['data'])

# Calculate and display month-over-month changes if possible
if not st.session_state['data'].empty:
    st.session_state['data']['Month'] = pd.to_datetime(st.session_state['data']['Month'])
    st.session_state['data'].sort_values(['Customer', 'Month'], inplace=True)
    st.session_state['data']['MoM Change'] = st.session_state['data'].groupby('Customer')['Consumption'].diff().fillna(0)
    st.subheader('Month-over-Month Change')
    st.dataframe(st.session_state['data'])
