import logging

import pandas as pd
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
STUDY_PLAN_ENDPOINT = BASE_URL + '/get_study_plan'


def get_study_plan(plan_id, token):
    """Fetch the study plan using the provided plan ID and bearer token."""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{STUDY_PLAN_ENDPOINT}{plan_id}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching study plan: {e}')
        st.error(f'Error fetching data from API: {e}')
        return None


# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ('Login', 'Register', 'Dashboard'))

if page == 'Login':
    login_page()
elif page == 'Register':
    register_page()
elif page == 'Dashboard':
    st.title('Dashboard')

    # Check if user is logged in
    if 'token' not in st.session_state:
        st.warning('Please log in to access the dashboard.')
    else:
        plan_id = st.sidebar.text_input('Enter Plan ID:')
        submit = st.sidebar.button('Fetch Study Plan')

        if submit and plan_id:
            with st.spinner('Retrieving Study Plan...'):
                study_plan = get_study_plan(plan_id, st.session_state['token'])

            if study_plan:
                input_data = study_plan.get('input_data')
                generated_study_plan = study_plan.get('study_plan')

                st.write('Input Data:')
                st.json(input_data)

                if generated_study_plan:
                    st.write('Generated Study Plan:')
                    df = pd.DataFrame(generated_study_plan)
                    st.dataframe(df)
