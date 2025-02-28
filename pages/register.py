import requests
import streamlit as st
from config import HOST, PORT

REGISTER_ENDPOINT = f'{HOST}:{PORT}/register'


# 🔹 Function to Register User
def register_user(name, email, username, password):
    """Send registration data to the backend."""
    payload = {'name': name, 'email': email, 'username': username, 'password': password}
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    return response.status_code == 200


# 🔹 Page Title
st.title('Register')

# 🔹 Registration Form
name = st.text_input('Enter Full Name:')
email = st.text_input('Enter Email:')
username = st.text_input('Choose a Username:')
password = st.text_input('Choose a Password:', type='password')
confirm_password = st.text_input('Confirm Password:', type='password')

# 🔹 Registration Button
if st.button('Register'):
    if not name or not email or not username or not password or not confirm_password:
        st.error('All fields are required.')
    elif password != confirm_password:
        st.error('Passwords do not match. Please try again.')
    else:
        response = register_user(name, email, username, password)
        if response:
            st.success('Registration successful! Redirecting to login...')
            st.query_params['registered'] = 'true'  # ✅ Set query param
            st.switch_page('pages/login.py')  # Redirect to login page
        else:
            st.error('Registration failed. Please check your details and try again.')
