import streamlit as st

# 🔹 Ensure we have a study plan selected
if 'study_plan' not in st.session_state:
    st.warning('No study plan selected for viewing.')
    st.switch_page('pages/dashboard.py')

plan = st.session_state['study_plan']

st.title('View Study Plan')

# ✅ Show success message for updated plans
st.success('Study plan updated successfully!')

st.write(f'**🎯 Goals:** {plan["input_data"]["goals"]}')
st.write(f'**📅 Days:** {plan["input_data"]["days"]}')
st.write(f'**⏳ Time Per Day:** {plan["input_data"]["time_per_day"]} min')
st.write(
    f'**📖 Preferred Topics:** {", ".join(plan["input_data"]["preferred_topics"])}'
)

# 🔹 Display study plan activities
for day in plan['study_plan']['study_plan']:
    st.subheader(f'Day {day["day"]}')
    for activity in day['activities']:
        st.write(f'🔹 {activity["activity"]} ({activity["time_minutes"]} min)')

# 🔹 Button to go back to dashboard
if st.button('⬅️ Back to Dashboard'):
    st.switch_page('pages/dashboard.py')
