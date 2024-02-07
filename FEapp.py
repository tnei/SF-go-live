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
    
    # NEW CODE: Combine existing customers with a text input for new customers
    existing_customers = list(st.session_state['data']['Customer'].unique())
    customer_name = st.sidebar.text_input('Customer Name')
    if customer_name:
        existing_customers.append(customer_name)
    customer_selection = st.sidebar.selectbox('Select or Add New Customer', options=existing_customers)
    
    # Continue with other inputs but adjust to use `customer_selection` instead of `customer_name`
    consumption_amount = st.number_input('Monthly Consumption Amount ($)', min_value=0.0, format='%f')
    consumption_month = st.date_input('Month', datetime.now()).strftime('%Y-%m')
    project_status = st.selectbox('Project Status', ['On Track', 'At Risk', 'Paused'])
    notes = st.text_area('Notes')
    region = st.selectbox('Region', ['Canada East', 'Canada Central', 'Canada West', 'US East', 'US Central', 'US West'])
    submit_button = st.button('Submit')

# Modify the 'Handle the submit action' section to use `customer_selection` instead of `customer_name`
if submit_button:
    new_data = {
        'Customer': customer_selection,  # Use `customer_selection` here
        'Month': consumption_month,
        'Consumption': consumption_amount,
        'Project Status': project_status,
        'Notes': notes,
        'Region': region
    }
    st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_data])], ignore_index=True)

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
