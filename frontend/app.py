import requests
import streamlit as st

api_url = 'http://127.0.0.1:8000/get_study_plan/'


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
    study_plan = get_study_plan(plan_id)
    if study_plan:
        st.write('Input Data:', study_plan.get('input_data'))
        st.write('Generated Study Plan:', study_plan.get('study_plan'))
