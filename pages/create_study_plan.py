import requests
import streamlit as st

# Backend configuration
HOST = 'http://localhost'
PORT = '8080'
CREATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/create_study_plan'

# 🔹 Ensure user is logged in
if 'token' not in st.session_state or not st.session_state['token']:
    st.warning('You must log in to create a study plan.')
    st.switch_page('pages/login.py')

# 🔹 Check session state for study plan
if 'study_plan' not in st.session_state:
    st.session_state['study_plan'] = None


# 🔹 Function to create a study plan
def create_study_plan(goals, days, time_per_day, preferred_topics, token):
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
        return response.json()  # Return study plan details
    except requests.exceptions.RequestException as e:
        st.error(f'Failed to create study plan: {e}')
        return None


st.title('Create Study Plan')

# 🔹 Show the form only if no study plan exists
if st.session_state['study_plan'] is None:
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

            study_plan = create_study_plan(
                goals,
                days,
                time_per_day,
                preferred_topics_list,
                st.session_state['token'],
            )

            if study_plan:
                st.session_state['study_plan'] = (
                    study_plan  # ✅ Save the study plan in session state
                )
                st.rerun()  # Refresh the page to show only the study plan
            else:
                st.error('Failed to create study plan. Please try again.')
        else:
            st.error('Please fill in all fields with valid data.')

# 🔹 Display Study Plan if Created
if st.session_state['study_plan']:
    st.success('Study plan created successfully!')
    st.subheader('Your Study Plan:')
    st.write(st.session_state['study_plan'])

    if st.button('Create Another Study Plan'):
        st.session_state['study_plan'] = None  # Reset state
        st.rerun()  # Refresh the page
