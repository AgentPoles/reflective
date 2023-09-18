"""
Copyright (C) 2023, Matthew Adams

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or 
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the licence is provided with this program. If you are unable
to view it, please see https://www.gnu.org/licenses/
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from scripts import blockchain_connector, fetch_records, jsonproducer, oracle


st.set_page_config(
    page_title="Relay labs",
    page_icon="🦚",
)

# with st.sidebar:
#     st.sidebar.markdown("### <span style='color: #1DB954;'>Setup</span>", unsafe_allow_html=True)     
#     openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password", help="You can find your API key at https://platform.openai.com/account/api-keys")
#     st.session_state["openai_api_key"] = openai_api_key

    # # Add the drop-down selectors for Industry and Company Size
    # industry = st.selectbox(
    # "Select your company's industry:",
    # sorted(['Aerospace / Defense', 'Agriculture / Food Services', 
    #         'Automotive', 'Construction', 'Education', 
    #         'Energy / Utilities', 'Finance / Banking', 
    #         'Government / Public Sector', 'Healthcare', 
    #         'Hospitality / Tourism', 'Insurance', 
    #         'Legal Services', 'Manufacturing', 
    #         'Media / Entertainment', 'Non-profit', 
    #         'Real Estate', 'Retail / E-commerce', 
    #         'Technology / IT', 'Telecommunication', 
    #         'Transportation / Logistics'])
    # , placeholder="Select Industry")
    # st.session_state["industry"] = industry

    # company_size = st.selectbox("Select your company's size:", ['Small (1-50 employees)', 'Medium (51-200 employees)', 'Large (201-1,000 employees)', 'Enterprise (1,001-10,000 employees)', 'Large Enterprise (10,000+ employees)'], placeholder="Select Company Size")
    # st.session_state["company_size"] = company_size

    # st.sidebar.markdown("---")

    # st.sidebar.markdown("### <span style='color: #1DB954;'>About</span>", unsafe_allow_html=True)        
    
    # st.sidebar.markdown("""
    #                     Created by [Matt Adams](https://www.linkedin.com/in/matthewrwadams)
                        
    #                     View the source code on [GitHub](https://github.com/mrwadams/attackgen)
    #                     """)



st.markdown("# <span style='color: #1DB954;'>Relay Labs 🦚</span>", unsafe_allow_html=True)
st.markdown("<span style='color: #1DB954;'> **..an event-driven approach to processing  blockchain relay costs.**</span>", unsafe_allow_html=True)

st.image(
            "./img/props-green-crystal.png", width=200)

st.markdown("---")

col2, col3, col4 = st.columns([1, 2, 3])
        

with col2:
    if st.button("For User"):
        switch_page("user")

with col3:
    st.write("")

with col4:
    if st.button("For Business"):
        switch_page("business")
