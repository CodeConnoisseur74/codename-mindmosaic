import logging

import requests
import streamlit as st
from decouple import config

# Load configuration from environment variables
HOST = config('HOST', default='http://127.0.0.1')
PORT = config('PORT', default='8080')
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


# 🔹 Check for registration success message
if 'registered' in st.query_params:
    st.success('Registration successful! You can now log in.')
    del st.query_params[
        'registered'
    ]  # ✅ Remove query param to prevent persistent message

# 🔹 If already logged in, redirect to dashboard
if st.session_state['token']:
    st.switch_page('pages/dashboard.py')

# 🔹 Show login form only if user is not logged in
st.title('Login')

username = st.text_input('Enter Username:', '')
password = st.text_input('Enter Password:', '', type='password')
submit = st.button('Login')

if submit:
    token = get_token(username, password)
    if token:
        st.session_state['token'] = token
        st.success('Login successful! Redirecting...')
        st.switch_page('pages/dashboard.py')
    else:
        st.error('Invalid credentials. Please try again.')
