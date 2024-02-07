import streamlit as st
import pandas as pd
from datetime import datetime

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

# Assuming 'data' DataFrame is available and not empty
if not st.session_state['data'].empty:
    # Generate a unique identifier for each row to help users select entries to delete
    st.session_state['data']['ID'] = st.session_state['data'].apply(lambda x: f"{x['Customer']} - {x['Month']}", axis=1)
    
    # Let users select entries to delete based on this ID
    delete_selection = st.multiselect('Select entries to delete', options=st.session_state['data']['ID'].unique())
    
    # Button to delete selected entries
    if st.button('Delete Selected Entries'):
        # Keep rows that are not in delete_selection
        st.session_state['data'] = st.session_state['data'][~st.session_state['data']['ID'].isin(delete_selection)]
        st.success('Selected entries deleted.')

    # Remove the 'ID' column before displaying or using the DataFrame further
    st.session_state['data'] = st.session_state['data'].drop(columns=['ID'])

# Filtering options
st.sidebar.header("Filter Data")
filter_customer = st.sidebar.selectbox('Filter by Customer', options=['All'] + list(st.session_state['data']['Customer'].unique()))
filter_region = st.sidebar.selectbox('Filter by Region', ['All'] + ['Canada East', 'Canada Central', 'Canada West', 'US East', 'US Central', 'US West'])
filter_project_status = st.sidebar.selectbox('Filter by Project Status', ['All', 'On Track', 'At Risk', 'Paused'])

# Apply filters to DataFrame
filtered_data = st.session_state['data']
if filter_customer != 'All':
    filtered_data = filtered_data[filtered_data['Customer'] == filter_customer]
if filter_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == filter_region]
if filter_project_status != 'All':
    filtered_data = filtered_data[filtered_data['Project Status'] == filter_project_status]

# Display the data with applied filters
st.subheader('Filtered Monthly Consumption Data')
st.dataframe(filtered_data)

# Calculate and display month-over-month changes if possible
if not filtered_data.empty:
    filtered_data['Month'] = pd.to_datetime(filtered_data['Month'])
    filtered_data.sort_values(['Customer', 'Month'], inplace=True)
    # Calculate MoM Change as a percentage
    filtered_data['MoM Change'] = filtered_data.groupby('Customer')['Consumption'].pct_change().fillna(0) * 100
    # Format the 'MoM Change' column to show percentages with 2 decimal places
    filtered_data['MoM Change'] = filtered_data['MoM Change'].map('{:,.2f}%'.format)
    st.subheader('Month-over-Month Change (%)')
    st.dataframe(filtered_data)

# Function to display the main tracker page
def main_tracker_page():
    st.title('Snowflake Consumption Tracker - Active Projects')
    
    # Sidebar for user input in Active Projects page
    with st.sidebar:
        st.header('Add Customer Consumption')
        # Your existing sidebar code for adding customer consumption...

    # Your existing code for handling submit action, filtering, and displaying data...
    
    # Button to move selected customers to completed
    completed_customers = st.multiselect('Select customers to mark as Completed', options=st.session_state['data']['Customer'].unique())
    if st.button('Mark as Completed'):
        if 'completed_data' not in st.session_state:
            st.session_state['completed_data'] = pd.DataFrame(columns=st.session_state['data'].columns)
        for customer in completed_customers:
            # Move selected customers to completed_data
            completed_entries = st.session_state['data'][st.session_state['data']['Customer'] == customer]
            st.session_state['completed_data'] = pd.concat([st.session_state['completed_data'], completed_entries])
            st.session_state['data'] = st.session_state['data'][st.session_state['data']['Customer'] != customer]
        st.success('Selected customers marked as Completed')

# Function to display the completed projects page
def completed_projects_page():
    st.title('Completed Projects')
    if 'completed_data' in st.session_state and not st.session_state['completed_data'].empty:
        st.dataframe(st.session_state['completed_data'])
    else:
        st.write("No completed projects.")

# Add a navigation bar
page = st.sidebar.selectbox("Navigate", ["Active Projects", "Completed Projects"])

if page == "Active Projects":
    main_tracker_page()
elif page == "Completed Projects":
    completed_projects_page()
