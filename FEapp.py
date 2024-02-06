import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title('Snowflake Consumption Tracker')

# Initialize the DataFrame in session state if it doesn't exist
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Customer', 'Month', 'Consumption', 'Project Status', 'Notes', 'Region'])

# Sidebar for user input
with st.sidebar:
    st.header('Add Customer Consumption')
    # Input for the customer name
    customer_name = st.selectbox('Customer Name', options=[''] + list(st.session_state['data']['Customer'].unique()))
    new_customer = st.text_input('Or add new customer')
    consumption_amount = st.number_input('Monthly Consumption Amount ($)', min_value=0.0, format='%f')
    consumption_month = st.date_input('Month', datetime.now()).strftime('%Y-%m')
    project_status = st.selectbox('Project Status', ['On Track', 'At Risk', 'Paused'])
    notes = st.text_area('Notes')
    region = st.selectbox('Region', ['Canada East', 'Canada Central', 'Canada West', 'US East', 'US Central', 'US West'])
    submit_button = st.button('Submit')

# Handle the submit action
if submit_button:
    if new_customer:  # If a new customer name is provided, use it
        customer_name = new_customer
    if customer_name:  # Ensure a customer name is provided
        new_data = {
            'Customer': customer_name, 
            'Month': consumption_month, 
            'Consumption': consumption_amount, 
            'Project Status': project_status, 
            'Notes': notes,
            'Region': region  # Add the selected region to the new data entry
        }
        st.session_state['data'] = st.session_state['data'].append(new_data, ignore_index=True)
    else:
        st.error('Please provide a customer name.')

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
