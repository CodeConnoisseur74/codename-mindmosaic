import requests
import streamlit as st
from config import HOST, PORT

# ✅ Construct API endpoints dynamically
UPDATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/update_study_plan'


# ✅ Function for updating study plan
def update_study_plan(plan_id, updated_data, token):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    try:
        response = requests.put(
            f'{UPDATE_STUDY_PLAN_ENDPOINT}/{plan_id}',
            json=updated_data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to update study plan: {e}')
    return None


# ✅ Ensure a study plan is selected for editing
if 'edit_plan' not in st.session_state:
    st.warning('⚠️ No study plan selected for editing.')
    st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard

plan = st.session_state['edit_plan']

st.title('✏️ Edit Study Plan')

# ✅ Pre-fill form with existing data
goals = st.text_area('🎯 Goals:', plan['input_data']['goals'])
days = st.number_input(
    '📅 Days:', min_value=1, step=1, value=plan['input_data']['days']
)
time_per_day = st.number_input(
    '⏳ Time per Day (minutes):',
    min_value=1,
    step=1,
    value=plan['input_data']['time_per_day'],
)
preferred_topics = st.text_input(
    '📚 Preferred Topics (comma-separated):',
    ', '.join(plan['input_data']['preferred_topics']),
)

if st.button('💾 Save Changes'):
    updated_data = {
        'goals': goals,
        'days': days,
        'time_per_day': time_per_day,
        'preferred_topics': [topic.strip() for topic in preferred_topics.split(',')],
    }

    response = update_study_plan(
        plan['plan_id'], updated_data, st.session_state['token']
    )

    if response:
        st.success('✅ Study plan updated successfully!')
        st.session_state.pop('edit_plan', None)  # ✅ Clear session state
        st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard
