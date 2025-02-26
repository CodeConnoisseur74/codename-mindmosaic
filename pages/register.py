import requests
import streamlit as st
from decouple import config

# Load configuration
HOST = config('HOST', default='http://127.0.0.1')
PORT = config('PORT', default='8080')
REGISTER_ENDPOINT = f'{HOST}:{PORT}/register'


def register_page():
    """Render the registration page."""
    st.title('Register')

    # Registration form inputs
    name = st.text_input('Enter Full Name:')
    email = st.text_input('Enter Email:')
    username = st.text_input('Choose a Username:')
    password = st.text_input('Choose a Password:', type='password')
    confirm_password = st.text_input('Confirm Password:', type='password')

    if st.button('Register'):
        if password != confirm_password:
            st.error('Passwords do not match. Please try again.')
        else:
            response = register_user(name, email, username, password)
            if response:
                st.success('Registration successful! You can now log in.')
            else:
                st.error(
                    'Registration failed. Please check your details and try again.'
                )


def register_user(name, email, username, password):
    """Send registration data to the backend."""
    payload = {'name': name, 'email': email, 'username': username, 'password': password}
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    return response.status_code == 201
