import streamlit as st
from mariska_pages.compare_9500 import compare_9500
from mariska_pages.import_deposits import import_deposits



if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()