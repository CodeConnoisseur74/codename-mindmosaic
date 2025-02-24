import logging

import requests
import streamlit as st
from decouple import config

# Load configuration from environment variables
HOST = config('HOST', default='http://127.0.0.1')
PORT = config('PORT', default='8080')
CREATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/create_study_plan/'

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)


def create_study_plan_page():
    """Render the create study plan page."""
    st.title('Create Study Plan')

    # Input fields for creating a study plan
    goals = st.text_area('Goals:', '')
    days = st.number_input('Days:', min_value=1, value=1)
    time_per_day = st.number_input('Time per Day (minutes):', min_value=1, value=60)
    preferred_topics = st.text_input('Preferred Topics (comma-separated):', '')
    submit = st.button('Create Study Plan')

    if submit:
        if goals and preferred_topics:
            preferred_topics_list = [
                topic.strip() for topic in preferred_topics.split(',')
            ]
            response = create_study_plan(
                goals,
                days,
                time_per_day,
                preferred_topics_list,
                st.session_state.get('token'),
            )
            if response:
                st.success('Study plan created successfully!')
            else:
                st.error('Failed to create study plan. Please try again.')
        else:
            st.error('Please fill in all fields.')


def create_study_plan(goals, days, time_per_day, preferred_topics, token):
    """Send study plan data to the backend for creation."""
    headers = {'Authorization': f'Bearer {token}'} if token else {}
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
