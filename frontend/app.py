import logging

# import pandas as pd
import requests
import streamlit as st
from decouple import config
from login import login_page
from register import register_page

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Load configuration from environment variables
HOST = config('HOST', default='http://127.0.0.1')
PORT = config('PORT', default='8080')
BASE_URL = f'{HOST}:{PORT}'
CREATE_STUDY_PLAN_ENDPOINT = BASE_URL + '/create_study_plan/'


def create_study_plan_page():
    """Render the create study plan page."""
    st.title('Create Study Plan')

    # Input fields for creating a study plan
    title = st.text_input('Plan Title:')
    description = st.text_area('Description:')
    goals = st.text_input('Goals:')
    submit = st.button('Create Study Plan')

    if submit:
        if title and description and goals:
            response = create_study_plan(
                title, description, goals, st.session_state['token']
            )
            if response:
                st.success('Study plan created successfully!')
            else:
                st.error('Failed to create study plan. Please try again.')
        else:
            st.error('Please fill in all fields.')


def create_study_plan(title, description, goals, token):
    """Send study plan data to the backend for creation."""
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'title': title, 'description': description, 'goals': goals}
    try:
        response = requests.post(
            CREATE_STUDY_PLAN_ENDPOINT, json=payload, headers=headers
        )
        response.raise_for_status()
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to create study plan: {e}')
        return False


# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio(
    'Go to', ('Login', 'Register', 'Dashboard', 'Create Study Plan')
)

if page == 'Login':
    login_page()
elif page == 'Register':
    register_page()
elif page == 'Dashboard':
    # Dashboard code here
    pass
elif page == 'Create Study Plan':
    if 'token' not in st.session_state:
        st.warning('Please log in to create a study plan.')
    else:
        create_study_plan_page()
