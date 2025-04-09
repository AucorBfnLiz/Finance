import streamlit as st
from mariska_pages.compare_9500 import compare_9500
from mariska_pages.import_deposits import import_deposits




if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔐 You must log in to view this page.")
    st.stop()


st.set_page_config(page_title="9500 Page", page_icon="📑")

st.sidebar.title("📂  Menu")
selection = st.sidebar.radio("Select a section:", 
                            ["🏠 Overview", "📊 Compare Excel 9500", "🏦 Deposit Import"])

# Simple menu-based routing
if selection == "🏠 Overview":
    st.title("🏠 Overview")
    st.write("Welcome to 9500's main page.")
    st.write("Use the sidebar to navigate to the different sections.")

    st.markdown("---")
    st.markdown("### ℹ️ What each section does:")
    st.markdown("""
    - 📊 **Compare Excel 9500**  
      Upload two Excel files – one from Evolution, one from the 9500 recon – and compare them to see what’s missing or different.

    - 🏦 **Deposit Import**  
      Convert a list of deposit transactions from Excel into a CSV file ready for import into the Evolution cashbook system.
    """)


if selection == "📊 Compare Excel 9500":
    compare_9500()

if selection == "🏦 Deposit Import":
    import_deposits()