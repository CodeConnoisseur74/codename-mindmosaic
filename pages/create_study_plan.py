import json

import requests
import streamlit as st

# Backend configuration
HOST = 'http://localhost'
PORT = '8080'
CREATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/create_study_plan'


def create_study_plan(goals, days, time_per_day, preferred_topics, token):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'goals': goals,
        'days': days,
        'time_per_day': time_per_day,
        'preferred_topics': preferred_topics,
    }

    # Log payload for debugging
    st.write(f'Payload being sent: {json.dumps(payload, indent=2)}')

    try:
        response = requests.post(
            CREATE_STUDY_PLAN_ENDPOINT, json=payload, headers=headers
        )

        # Log the response for debugging
        st.write(f'Response status code: {response.status_code}')
        st.write(f'Response content: {response.content}')

        response.raise_for_status()

        # Return the study plan data to be displayed
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f'Request failed: {e}')
        return None


# Streamlit page to create and display a study plan
def create_study_plan_page():
    st.title('Create Study Plan')

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
                st.session_state.get('token'),
            )
            if study_plan:
                st.success('Study plan created successfully!')
                st.subheader('Your Study Plan:')
                st.write(study_plan)  # Display the study plan details
            else:
                st.error('Failed to create study plan. Please try again.')
        else:
            st.error('Please fill in all fields with valid data.')


# Run the page
if __name__ == '__main__':
    create_study_plan_page()
