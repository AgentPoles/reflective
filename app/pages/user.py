
import streamlit as st
from home import blockchain_connector

st.markdown("# <span style='color: #1DB954;'>User 🧑‍🎤</span>", unsafe_allow_html=True)

col1, col2 =  st.columns([1, 3])
col3, col4 =  st.columns([1, 3])
balance =  blockchain_connector.get_balance()
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
            `latest Hash`
                """)
    
with col4:
    transaction_hash = st.empty()
    transaction_hash.text("0x011853adc9f44a8a22a66875bdb50835f03485de40d02b56c69f8c5c52ab1250")


reward_amount_to_spend = st.text_input('Reward Amount', 10)
if st.button("spend"):
    new_hash = blockchain_connector.send_transaction(reward_amount_to_spend)
    transaction_hash.text(new_hash)
    balancee = blockchain_connector.get_balance()
    balance_display.text(f"{balancee} points")