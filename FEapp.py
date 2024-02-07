import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid

# UI Customization and Theming
st.set_page_config(
   page_title="Snowflake Consumption Tracker",
   page_icon=":snowflake:",
   layout="wide",
   initial_sidebar_state="expanded",
   menu_items={
       'Get Help': 'https://www.example.com',
       'Report a bug': "https://www.example.com",
       'About': "# This is a Snowflake Consumption Tracker. Built with Streamlit."
   }
)

# Title of the app
st.title('Snowflake Consumption Tracker')

# Initialize the DataFrame in session state if it doesn't exist
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Customer', 'Month', 'Consumption', 'Project Status', 'Notes', 'Region'])

# Sidebar for user input
with st.sidebar:
    st.header('Add Customer Consumption')
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
            'Region': region
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_data])], ignore_index=True)
    else:
        st.error('Please provide a customer name.')

# Filtering options and Data Preparation
filter_customer = st.sidebar.selectbox('Filter by Customer', options=['All'] + list(st.session_state['data']['Customer'].unique()))
filter_region = st.sidebar.selectbox('Filter by Region', ['All'] + ['Canada East', 'Canada Central', 'Canada West', 'US East', 'US Central', 'US West'])
filter_project_status = st.sidebar.selectbox('Filter by Project Status', ['All', 'On Track', 'At Risk', 'Paused'])

filtered_data = st.session_state['data']
if filter_customer != 'All':
    filtered_data = filtered_data[filtered_data['Customer'] == filter_customer]
if filter_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == filter_region]
if filter_project_status != 'All':
    filtered_data = filtered_data[filtered_data['Project Status'] == filter_project_status]

# Collapsible section for displaying filtered data
with st.expander("Filtered Monthly Consumption Data", expanded=True):
    st.dataframe(filtered_data)

# Collapsible section for displaying month-over-month changes
if not filtered_data.empty:
    filtered_data['Month'] = pd.to_datetime(filtered_data['Month'])
    filtered_data.sort_values(['Customer', 'Month'], inplace=True)
    filtered_data['MoM Change'] = filtered_data.groupby('Customer')['Consumption'].pct_change().fillna(0) * 100
    filtered_data['MoM Change'] = filtered_data['MoM Change'].map('{:,.2f}%'.format)
    
    with st.expander("Month-over-Month Change (%)"):
        st.dataframe(filtered_data[['Customer', 'Month', 'MoM Change']])
       
# Function to display the main tracker page
def main_tracker_page():
    st.title('Snowflake Consumption Tracker - Active Projects')
    # Assuming 'filtered_data' is prepared before this function is called
    AgGrid(filtered_data)

def completed_projects_page():
    st.title('Completed Projects')
    # Ensure 'completed_data' is available and not empty
    if 'completed_data' in st.session_state and not st.session_state['completed_data'].empty:
        AgGrid(st.session_state['completed_data'])
    else:
        st.write("No completed projects.")

# Navigation and page logic, including sidebar configurations...
page = st.sidebar.selectbox("Navigate", ["Active Projects", "Completed Projects"])

if page == "Active Projects":
    main_tracker_page()
elif page == "Completed Projects":
    completed_projects_page()
