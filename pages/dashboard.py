import requests
import streamlit as st
from config import HOST, PORT  # ✅ Import centralized settings

# ✅ Construct API endpoints dynamically
USER_STUDY_PLANS_ENDPOINT = f'{HOST}:{PORT}/get_study_plans'
DELETE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/delete_study_plan'
UPDATE_STUDY_PLAN_ENDPOINT = f'{HOST}:{PORT}/update_study_plan'


# 🔹 Ensure user is logged in
if 'token' not in st.session_state or not st.session_state['token']:
    st.warning('You must log in to view your study plans.')
    st.switch_page('pages/login.py')


# 🔹 Function to fetch user study plans
def get_user_study_plans(token):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(USER_STUDY_PLANS_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to retrieve study plans: {e}')
        return []


# 🔹 Function to delete a study plan
def delete_study_plan(plan_id):
    headers = {'Authorization': f'Bearer {st.session_state["token"]}'}
    try:
        response = requests.delete(
            f'{DELETE_STUDY_PLAN_ENDPOINT}/{plan_id}', headers=headers
        )
        response.raise_for_status()
        st.success('✅ Study plan deleted successfully!')
        st.rerun()  # Reload the page to update the study plan list
    except requests.exceptions.RequestException as e:
        st.error(f'❌ Failed to delete study plan: {e}')


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


# 🔹 Dashboard UI
st.title('Dashboard')
st.subheader('Your Study Plans')

# ✅ Add a loading spinner while fetching study plans
with st.spinner('Loading your study plans...'):
    study_plans = get_user_study_plans(st.session_state['token'])

# 🔹 If no study plans exist, show a message and button
if not study_plans:
    st.info('📚 You have no study plans yet. Click below to create one!')

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('➕ Create New Study Plan', use_container_width=True):
            st.switch_page('pages/view_study_plan.py')


# 🔹 Add an Edit button for each study plan
for plan in study_plans:
    with st.expander(f'📄 Study Plan {plan["plan_id"]}'):
        st.write(f'**🕒 Created On:** {plan["created_at"]}')
        st.write(f'**🎯 Goals:** {plan["input_data"]["goals"]}')
        st.write(f'**📅 Days:** {plan["input_data"]["days"]}')
        st.write(f'**⏳ Time Per Day:** {plan["input_data"]["time_per_day"]} min')

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button('📖 View', key=f'view-{plan["plan_id"]}'):
                st.session_state['study_plan'] = plan
                st.switch_page('pages/create_study_plan.py')

        with col2:
            if st.button('📝 Edit', key=f'edit-{plan["plan_id"]}'):
                st.session_state['edit_plan'] = plan
                st.switch_page('pages/edit_study_plan.py')

        with col3:
            if st.button('🗑️ Delete', key=f'delete-{plan["plan_id"]}'):
                delete_study_plan(plan['plan_id'])
