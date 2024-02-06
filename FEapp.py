import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib as plt
import seaborn as sns

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

# Visualizations
st.subheader("Visualizations")

# Time Series Plot
st.markdown("### Time Series Plot of Consumption")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='Month', y='Consumption', hue='Customer', ax=ax)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Bar Chart of Consumption by Region
st.markdown("### Total Consumption by Region")
consumption_by_region = filtered_data.groupby('Region')['Consumption'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=consumption_by_region, x='Region', y='Consumption', ax=ax)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Project Status Breakdown
st.markdown("### Project Status Distribution")
status_counts = filtered_data['Project Status'].value_counts()
fig, ax = plt.subplots()
status_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, counterclock=False, wedgeprops={'edgecolor': 'black'})
ax.set_ylabel('')  # Remove the y-label as it's not necessary for a pie chart
plt.tight_layout()
st.pyplot(fig)

# Histogram of Consumption Amounts
st.markdown("### Distribution of Consumption Amounts")
fig, ax = plt.subplots()
sns.histplot(data=filtered_data, x='Consumption', kde=True, bins=20, ax=ax)
plt.tight_layout()
st.pyplot(fig)
