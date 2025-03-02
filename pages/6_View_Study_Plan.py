import streamlit as st

# ✅ Ensure a study plan is selected for viewing
if 'study_plan' not in st.session_state or st.session_state['study_plan'] is None:
    st.warning('⚠️ No study plan selected for viewing.')
    st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard

plan = st.session_state['study_plan']

st.title('📖 View Study Plan')

# ✅ Show success message if coming from an update
if 'study_plan_updated' in st.session_state:
    st.success('✅ Study plan updated successfully!')
    del st.session_state['study_plan_updated']  # ✅ Remove flag after showing message

# ✅ Ensure `plan["input_data"]` exists before accessing it
input_data = plan.get('input_data', {})
study_plan_details = plan.get('study_plan', {}).get('study_plan', [])

st.write(f'**🎯 Goals:** {input_data.get("goals", "Not specified")}')
st.write(f'**📅 Days:** {input_data.get("days", "N/A")}')
st.write(f'**⏳ Time Per Day:** {input_data.get("time_per_day", "N/A")} minutes')
st.write(
    f'**📚 Preferred Topics:** {", ".join(input_data.get("preferred_topics", []))}'
)

# 🔹 Display Study Plan Activities
if study_plan_details:
    for day in study_plan_details:
        st.subheader(f'📅 Day {day["day"]}')
        for activity in day['activities']:
            st.write(f'- {activity["activity"]} ({activity["time_minutes"]} min)')
else:
    st.info('📌 No activities found in this study plan.')

# 🔹 Button to go back to dashboard
if st.button('⬅️ Back to Dashboard'):
    st.switch_page('pages/3_Dashboard.py')  # ✅ Redirect to Dashboard
