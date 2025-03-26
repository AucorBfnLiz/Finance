import streamlit as st
from pages.compare_9500 import compare_9500
from pages.import_deposits import import_deposits


st.set_page_config(page_title="Mariska se Bladsy", page_icon="📑")

st.sidebar.title("📂 Mariska Submenu")
selection = st.sidebar.radio("Kies 'n afdeling:", 
                            ["🏠 Oorsig", "📊 Vergelyk Excel 9500", "🏦 Deposito-invoer"])

# Simple menu-based routing
if selection == "🏠 Oorsig":
    st.title("🏠 Oorsig")
    st.write("Welkom by Mariska se hoofbladsy.")
if selection == "📊 Vergelyk Excel 9500":
    compare_9500()
if selection == "🏦 Deposito-invoer":
    import_deposits()