import logging

import requests
import streamlit as st
from config import HOST, PORT

TOKEN_ENDPOINT = f'{HOST}:{PORT}/token'

# 🔹 Initialize session state
if 'token' not in st.session_state:
    st.session_state['token'] = None


# 🔹 Function to get token
def get_token(username, password):
    """Retrieve a bearer token using username and password."""
    payload = {'username': username, 'password': password}
    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload, timeout=10)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to retrieve token: {e}')
        return None


# 🔹 Redirect logged-in users to the Dashboard
if st.session_state['token']:
    st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard

# 🔹 Login Form
st.title('🔑 Login')

st.markdown('Enter your credentials to access your study plans.')

username = st.text_input('👤 Username', '')
password = st.text_input('🔒 Password', '', type='password')

# 🔹 Login Button
if st.button('🚀 Login'):
    if username and password:
        token = get_token(username, password)
        if token:
            st.session_state['token'] = token
            st.success('✅ Login successful! Redirecting...')
            st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard
        else:
            st.error('❌ Invalid credentials. Please try again.')
    else:
        st.warning('⚠️ Please fill in both fields.')
