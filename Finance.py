import streamlit as st

st.set_page_config(page_title="Finance Automation", page_icon="📈", layout="wide")

st.sidebar.success("Welcome!")

st.title("📊 Finance Dashboard")

st.markdown("""
Welcome to the Finance Automation tool.

Use the menu on the left to access different sections:
- 📈 **Dashboard**  
- 📊 **Reports**  
- 🧾 **Statements**  
- 🛠️ **Utilities**
""")
