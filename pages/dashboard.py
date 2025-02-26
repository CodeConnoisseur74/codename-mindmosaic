import requests
import streamlit as st

# Backend configuration
HOST = 'http://localhost'
PORT = '8080'
USER_STUDY_PLANS_ENDPOINT = (
    f'{HOST}:{PORT}/get_study_plans'  # ✅ Ensure correct endpoint
)

# 🔹 Ensure user is logged in
if 'token' not in st.session_state or not st.session_state['token']:
    st.warning('You must log in to view your study plans.')
    st.switch_page('pages/login.py')


# 🔹 Fetch User's Study Plans
def get_user_study_plans(token):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(USER_STUDY_PLANS_ENDPOINT, headers=headers)
        response.raise_for_status()  # ✅ Raise error for 4xx/5xx responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f'❌ API HTTP Error: {e}')
        st.write(f'Response content: {response.text}')  # Debugging exact error
        return []
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to connect to API: {e}')
        return []


# 🔹 Dashboard UI
st.title('Dashboard')
st.subheader('Your Study Plans')

study_plans = get_user_study_plans(st.session_state['token'])  # ✅ Token is passed

if study_plans:
    for plan in study_plans:
        with st.expander(f'Study Plan {plan["plan_id"]}'):
            st.write(f'**Created On:** {plan["created_at"]}')
            st.write(f'**Goals:** {plan["input_data"]["goals"]}')
            st.write(f'**Days:** {plan["input_data"]["days"]}')
            st.write(f'**Time Per Day:** {plan["input_data"]["time_per_day"]} min')

            if st.button(f'View Study Plan {plan["plan_id"]}', key=plan['plan_id']):
                st.session_state['study_plan'] = plan
                st.switch_page('pages/create_study_plan.py')
else:
    st.info('No study plans found.')
