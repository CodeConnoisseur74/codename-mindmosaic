import time

import requests
import streamlit as st
from config import HOST, PORT  # ✅ Import centralized settings

# ✅ API endpoints
USER_STUDY_PLANS_ENDPOINT = f'{HOST}:{PORT}/get_study_plans'
DELETE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/delete_study_plan'

# ✅ Ensure user is logged in
if 'token' not in st.session_state or not st.session_state['token']:
    st.warning('You must log in to view your study plans.')
    st.switch_page('pages/1_Login.py')  # ✅ Redirect to login


# ✅ Function to fetch study plans (no caching to ensure updated list)
def get_user_study_plans(token):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(USER_STUDY_PLANS_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to retrieve study plans: {e}')
        return []


# ✅ Function to delete a study plan
def delete_study_plan(plan_id):
    headers = {'Authorization': f'Bearer {st.session_state["token"]}'}
    try:
        response = requests.delete(
            f'{DELETE_STUDY_PLAN_ENDPOINT}/{plan_id}', headers=headers
        )
        response.raise_for_status()
        st.success('✅ Study plan deleted successfully!')
        st.session_state['study_plans'] = None  # ✅ Reset session cache
        st.rerun()  # ✅ Refresh dashboard
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to delete study plan: {e}')


# ✅ Force fresh data each time the page loads
st.session_state['study_plans'] = get_user_study_plans(st.session_state['token'])

st.title('📊 Dashboard')
st.subheader('Your Study Plans')

# ✅ Check if study plans exist
study_plans = st.session_state['study_plans']
if not study_plans:
    st.info('📚 You have no study plans yet. Click below to create one!')

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('➕ Create New Study Plan', use_container_width=True):
            st.switch_page('pages/4_Create_Study_Plan.py')

for plan in study_plans:
    study_plan_title = plan['input_data'].get('goals', f'Study Plan {plan["plan_id"]}')

    with st.expander(f'📄 {study_plan_title}'):
        st.write(f'**🕒 Created On:** {plan["created_at"]}')
        st.write(f'**🎯 Goals:** {plan["input_data"]["goals"]}')
        st.write(f'**📅 Days:** {plan["input_data"]["days"]}')
        st.write(f'**⏳ Time Per Day:** {plan["input_data"]["time_per_day"]} min')

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button('📖 View', key=f'view-{plan["plan_id"]}'):
                st.session_state['study_plan'] = plan
                st.switch_page('pages/6_View_Study_Plan.py')

        with col2:
            if st.button('📝 Edit', key=f'edit-{plan["plan_id"]}'):
                st.session_state['edit_plan'] = plan
                st.switch_page('pages/5_Edit_Study_Plan.py')

        with col3:
            if st.button('🗑️ Delete', key=f'delete-{plan["plan_id"]}'):
                delete_study_plan(plan['plan_id'])


st.sidebar.write(f'👤 Logged in as: **{st.session_state.get("username", "User")}**')

if st.sidebar.button('🚪 Logout', use_container_width=True):
    st.toast('✅ Logged out successfully!')  # ✅ Show confirmation message
    time.sleep(1)  # ✅ Small delay before refresh (1 second)
    st.session_state.clear()  # ✅ Clears all session data
    st.rerun()  # ✅ Refresh the app to show login page
