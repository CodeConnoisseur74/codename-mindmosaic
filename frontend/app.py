import pandas as pd
import requests
import streamlit as st
from decouple import config

BASE_URL = config('BASE_URL', default='http://127.0.0.1')
PORT = config('PORT', default='8000')
STUDY_PLAN_ENDPOINT = '/get_study_plan/'


api_url = f'{BASE_URL}:{PORT}{STUDY_PLAN_ENDPOINT}'


def get_study_plan(plan_id):
    headers = {'Authorization': 'SECRET_KEY'}
    response = requests.get(f'{api_url}{plan_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Error fetching data from API')
        return None


plan_id = st.text_input('Enter Plan ID:', '')

if plan_id:
    # Fetch the study plan
    study_plan = get_study_plan(plan_id)
    if study_plan:
        input_data = study_plan.get('input_data')
        generated_study_plan = study_plan.get('study_plan')

        # Display input data
        st.write('Input Data:')
        st.json(input_data)

        # Parse and display the generated study plan as a table
        if generated_study_plan:
            st.write('Generated Study Plan:')
            # Assuming generated_study_plan is a list of dictionaries
            df = pd.DataFrame(generated_study_plan)
            st.dataframe(df)
