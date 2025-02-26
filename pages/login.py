import logging  # Import logging module

import requests
import streamlit as st
from decouple import config

# Load configuration from environment variables
HOST = config('HOST', default='http://127.0.0.1')
PORT = config('PORT', default='8080')
TOKEN_ENDPOINT = f'{HOST}:{PORT}/token'


def login_page():
    """Render the login page with user authentication."""
    st.title('Login')

    # User inputs for authentication
    username = st.text_input('Enter Username:', '')
    password = st.text_input('Enter Password:', '', type='password')
    submit = st.button('Login')

    if submit:
        token = get_token(username, password)
        if token:
            st.session_state['token'] = token
            st.success('Login successful! Proceed to the dashboard.')
        else:
            st.error('Invalid credentials. Please try again.')


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
