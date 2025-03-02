import requests
import streamlit as st
from config import HOST, PORT

REGISTER_ENDPOINT = f'{HOST}:{PORT}/register'


# 🔹 Function to Register User
def register_user(name, email, username, password):
    """Send registration data to the backend."""
    payload = {'name': name, 'email': email, 'username': username, 'password': password}
    try:
        response = requests.post(REGISTER_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Registration failed: {e}')
        return False


# 🔹 Redirect logged-in users to Dashboard
if 'token' in st.session_state and st.session_state['token']:
    st.switch_page(
        'pages/3_Dashboard.py'
    )  # ✅ Redirect to Dashboard if already logged in

# 🔹 Page Title
st.title('📝 Register')

st.markdown('Create a new account to start managing your study plans!')

# 🔹 Registration Form
name = st.text_input('👤 Full Name')
email = st.text_input('📧 Email')
username = st.text_input('🔑 Choose a Username')
password = st.text_input('🔒 Choose a Password', type='password')
confirm_password = st.text_input('🔑 Confirm Password', type='password')

# 🔹 Registration Button
if st.button('🚀 Register'):
    if not name or not email or not username or not password or not confirm_password:
        st.warning('⚠️ All fields are required.')
    elif password != confirm_password:
        st.error('❌ Passwords do not match. Please try again.')
    else:
        response = register_user(name, email, username, password)
        if response:
            st.success('✅ Registration successful! Redirecting to login...')
            st.switch_page('pages/1_Login.py')  # ✅ Redirect to Login
        else:
            st.error('❌ Registration failed. Please check your details and try again.')
