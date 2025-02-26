import streamlit as st

# 🔹 Ensure session state is properly set up
if 'token' not in st.session_state:
    st.session_state['token'] = None  # Set default to None if missing

# 🔹 Redirect to login if user is not authenticated
if not st.session_state['token']:
    st.warning('You need to log in first.')
    st.switch_page('pages/login.py')  # Redirect immediately

# 🔹 If logged in, show the dashboard
st.title('Dashboard')
st.write('Welcome to your dashboard!')

# Example dashboard content
st.write('Here is your study plan or dashboard data...')
