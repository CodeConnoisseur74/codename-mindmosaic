import logging

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
CREATE_STUDY_PLAN_ENDPOINT = BASE_URL + '/create_study_plan'


def create_study_plan_page():
    """Render the create study plan page."""
    st.title('Create Study Plan')

    # Input fields for creating a study plan
    goals = st.text_area('Goals:', '')
    days = st.number_input('Days:', min_value=1, step=1, value=1)
    time_per_day = st.number_input(
        'Time per Day (minutes):', min_value=1, step=1, value=60
    )
    preferred_topics = st.text_input('Preferred Topics (comma-separated):', '')
    submit = st.button('Create Study Plan')

    if submit:
        if goals and preferred_topics and days > 0 and time_per_day > 0:
            preferred_topics_list = [
                topic.strip() for topic in preferred_topics.split(',')
            ]
            response = create_study_plan(
                goals,
                days,
                time_per_day,
                preferred_topics_list,
                st.session_state['token'],
            )
            if response:
                st.success('Study plan created successfully!')
            else:
                st.error('Failed to create study plan. Please try again.')
        else:
            st.error('Please fill in all fields with valid data.')


def create_study_plan(goals, days, time_per_day, preferred_topics, token):
    """Send study plan data to the backend for creation."""
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'goals': goals,
        'days': days,
        'time_per_day': time_per_day,
        'preferred_topics': preferred_topics,
    }
    try:
        response = requests.post(
            CREATE_STUDY_PLAN_ENDPOINT, json=payload, headers=headers
        )
        response.raise_for_status()
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to create study plan: {e}')
        return False


# Sidebar Navigation
st.sidebar.title('Navigation')

# Map pages to their respective functions
page_functions = {
    'Login': login_page,
    'Register': register_page,
    'Dashboard': lambda: None,  # Placeholder for Dashboard code
    'Create Study Plan': create_study_plan_page
    if 'token' in st.session_state
    else lambda: st.warning('Please log in to create a study plan.'),
}

# Display the radio buttons and execute the corresponding function
page = st.sidebar.radio('Go to', list(page_functions.keys()))
page_functions[page]()
