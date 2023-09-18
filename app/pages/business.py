
import streamlit as st
from home import blockchain_connector, fetch_records
import pandas as pd
import altair as alt
import math


st.markdown("# <span style='color: #1DB954;'>Business 🏪</span>", unsafe_allow_html=True)

col1, col2 =  st.columns([1, 3])
col3, col4 =  st.columns([1, 3])
balance =  blockchain_connector.get_brand_balance()
st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: -2rem;
    }
    </style>
    """,unsafe_allow_html=True)
# Add components to the first column
with col1:
    st.markdown("""          
            `Reward Balance`
                """)
    
with col2:
    balance_display = st.empty()
    balance_display.text(f"{balance} points")


st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)
# Add components to the first column
with col3:
    st.markdown("""          
            `Account Balance`
                """)
    
with col4:
    account_balance = st.empty()
    account_balance.text(f"${0:.2f}")

st.subheader("Transaction Records")

# Fetch data from the CockroachDB table and get column names
current_balance, transaction_data, column_names = fetch_records.cockroachRead("0X12aed")

if current_balance:
    account_balance.text(f"${current_balance:.2f}")

if transaction_data:
    # Display the data in a Pandas DataFrame
    df = pd.DataFrame(transaction_data, columns=column_names)

    # Display the data as a table in Streamlit
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    timestamps = df['timestamp']
        # Set "timestamp" as the index of the DataFrame
    df.set_index('timestamp', inplace=True)

   
    # Sort the DataFrame by the timestamp (if not already sorted)
    df.sort_index(inplace=True)

        # Calculate previous balance values
    previous_balance = []
    balance = current_balance  # Initialize with the current account balance
    for cost_in_dollar in df['costindollar']:
        balance += cost_in_dollar
        previous_balance.append(balance)

   
    previous_balance = previous_balance[::-1] 
    
        # Create a dictionary with 'timestamp' and 'previous_balance'
    data_dict = {'timestamp': timestamps, 'account_balance': previous_balance}

    # Create a DataFrame from the dictionary
    data = pd.DataFrame(data_dict)

        # Calculate the minimum and maximum values for the y-axis
    min_previous_balance = min(previous_balance)
    max_previous_balance = max(previous_balance)

        # Create an Altair chart
    chart = alt.Chart(data).mark_line(color='#1DB954').encode(
        x='timestamp:T',
        y=alt.Y('account_balance:Q', scale=alt.Scale(domain=[math.ceil(min_previous_balance/1.1), max_previous_balance]))
    ).properties(
        width=600,
        height=300
    )


    st.altair_chart(chart, use_container_width=True)

    st.write("Transaction Data:")
    st.table(df)
# reward_amount_to_spend = st.text_input('Reward Amount', 10)
# if st.button("spend"):
#     new_hash = blockchain_connector.send_transaction(reward_amount_to_spend)
#     transaction_hash.text(new_hash)
#     balancee = blockchain_connector.get_balance()
#     balance_display.text(f"{balancee} points")