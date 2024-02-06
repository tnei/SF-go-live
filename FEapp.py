import streamlit as st
import pandas as pd

# Initialize session state to store data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "SI", "Customer", "Implementation colour code:Red/Yellow/Green", "Go Live Date",
        "Last Month Consumption", "Projected Consumption Value", "Update / Client Feedback / Use Case",
        "Snowflake Growth Plan", "Region"  # Add "Region" to the columns
    ])

# Function to add a new customer record
def add_customer(si, customer, status, go_live_date, last_month_consumption, projected_consumption_value, feedback, growth_plan, region):
    new_entry = {
        "SI": si,
        "Customer": customer,
        "Implementation colour code:Red/Yellow/Green": status,
        "Go Live Date": go_live_date,
        "Last Month Consumption": last_month_consumption,
        "Projected Consumption Value": projected_consumption_value,
        "Update / Client Feedback / Use Case": feedback,
        "Snowflake Growth Plan": growth_plan,
        "Region": region  # Add the "Region" value
    }
    st.session_state.data = st.session_state.data.append(new_entry, ignore_index=True)

# Sidebar for data entry
with st.sidebar:
    st.header("Enter Customer Data")
    si = st.text_input("SI")
    customer = st.text_input("Customer")
    status = st.selectbox("Implementation Status", ["On Track", "Paused", "On Hold By Client", "Red", "Yellow", "Green"])
    go_live_date = st.date_input("Go Live Date")
    last_month_consumption = st.text_area("Last Month Consumption")
    projected_consumption_value = st.text_input("Projected Consumption Value")
    feedback = st.text_area("Update / Client Feedback / Use Case")
    growth_plan = st.text_input("Snowflake Growth Plan")
    # Dropdown for selecting the region
    region = st.selectbox("Region", ["Canada East", "Canada Central", "Canada West", "US East", "US Central", "US West"])
    add_data = st.button("Add Customer", on_click=add_customer, args=(si, customer, status, go_live_date, last_month_consumption, projected_consumption_value, feedback, growth_plan, region))

# Display the data
st.header("Customer Data")
st.dataframe(st.session_state.data)
