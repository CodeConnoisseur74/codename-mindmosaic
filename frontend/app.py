import pandas as pd
import requests
import streamlit as st
from decouple import config

# Load configuration from environment variables
HOST = config('BASE_URL', default='http://127.0.0.1')
PORT = config('PORT', default='8000')
BASE_URL = f'{HOST}:{PORT}'
STUDY_PLAN_ENDPOINT = BASE_URL + '/get_study_plan/'
TOKEN_ENDPOINT = BASE_URL + '/token'


def get_token(username, password):
    """Retrieve a bearer token using username and password."""
    payload = {'username': username, 'password': password}
    response = requests.post(TOKEN_ENDPOINT, data=payload)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        st.error('Error fetching token from API')
        return None


def get_study_plan(plan_id, token):
    """Fetch the study plan using the provided plan ID and bearer token."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{STUDY_PLAN_ENDPOINT}{plan_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Error fetching data from API')
        return None


# User inputs for authentication and plan ID
username = st.text_input('Enter Username:', '')
password = st.text_input('Enter Password:', '', type='password')
plan_id = st.text_input('Enter Plan ID:', '')

if username and password and plan_id:
    # Retrieve the token
    token = get_token(username, password)

    if token:
        # Fetch the study plan
        study_plan = get_study_plan(plan_id, token)
        if study_plan:
            input_data = study_plan.get('input_data')
            generated_study_plan = study_plan.get('study_plan')

            st.write('Input Data:')
            st.json(input_data)

            if generated_study_plan:
                st.write('Generated Study Plan:')
                # Assuming generated_study_plan is a list of dictionaries
                df = pd.DataFrame(generated_study_plan)
                st.dataframe(df)
