import streamlit as st



st.set_page_config(page_title="Finance Automation", page_icon="📈", layout="wide")

# --- HIDE SIDEBAR QUICKLY BEFORE LOGIN ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                visibility: hidden;
            }
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

users = {
    "admin": "admin123",
    "user1": "test123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Incorrect username or password")

# --- MAIN APP ---
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📊 Finance Dashboard")
    st.markdown("""
    Welcome to the Finance Automation tool.

    Use the menu on the left to access different sections:
    - 📈 **Dashboard**  
    - 📊 **Reports**  
    - 🧾 **Statements**  
    - 🛠️ **Utilities**
    """)
else:
    # hide sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
