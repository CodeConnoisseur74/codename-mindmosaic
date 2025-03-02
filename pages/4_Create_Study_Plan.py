import requests
import streamlit as st
from config import HOST, PORT  # ✅ Import centralized settings

# ✅ Construct API endpoints dynamically
CREATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/create_study_plan'

# 🔹 Ensure user is logged in
if 'token' not in st.session_state or not st.session_state['token']:
    st.warning('You must log in to create a study plan.')
    st.switch_page('pages/1_Login.py')  # ✅ Redirect to login page

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
        return response.json()  # ✅ Return study plan details
    except requests.exceptions.HTTPError as http_err:
        st.error(f'Server error: {http_err}')
    except requests.exceptions.ConnectionError:
        st.error('Network error: Could not connect to the server.')
    except requests.exceptions.Timeout:
        st.error('Request timed out. Try again later.')
    except requests.exceptions.RequestException as e:
        st.error(f'Failed to create study plan: {e}')
    return None  # ✅ Return None if API request fails


# 🔹 UI: Create Study Plan Form
st.title('📖 Create Study Plan')

if st.session_state['study_plan'] is None:
    goals = st.text_area('🎯 Goals:', '')
    days = st.number_input('📅 Days:', min_value=1, step=1, value=1)
    time_per_day = st.number_input(
        '⏳ Time per Day (minutes):', min_value=1, step=1, value=60
    )
    preferred_topics = st.text_input('📚 Preferred Topics (comma-separated):', '')

    submit = st.button('➕ Create Study Plan')

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
                    study_plan  # ✅ Save study plan in session state
                )
                st.success('✅ Study plan created successfully!')
                st.rerun()  # Refresh page to show only the study plan
            else:
                st.error('❌ Failed to create study plan. Please try again.')
        else:
            st.error('❌ Please fill in all fields with valid data.')

# 🔹 Display Study Plan if Created
if st.session_state['study_plan']:
    plan = st.session_state['study_plan']

    st.success('✅ Study plan created successfully!')
    st.subheader('📖 Your Study Plan')

    # Extract plan details
    input_data = plan.get('input_data', {})
    study_plan_details = plan.get('study_plan', {}).get('study_plan', [])

    st.write(f'**🎯 Goals:** {input_data.get("goals", "Not specified")}')
    st.write(f'**📅 Days:** {input_data.get("days", "N/A")}')
    st.write(f'**⏳ Time per Day:** {input_data.get("time_per_day", "N/A")} minutes')
    st.write(
        f'**📚 Preferred Topics:** {", ".join(input_data.get("preferred_topics", []))}'
    )

    # Display each day’s activities
    for day in study_plan_details:
        st.subheader(f'📅 Day {day["day"]}')
        for activity in day['activities']:
            st.write(f'- {activity["activity"]} ({activity["time_minutes"]} min)')

    # 🔹 Navigation Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button('📊 Back to Dashboard'):
            st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard

    with col2:
        if st.button('➕ Create Another Study Plan'):
            st.session_state['study_plan'] = None  # Reset state
            st.rerun()  # Refresh the page
