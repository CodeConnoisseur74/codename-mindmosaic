import streamlit as st

# Sidebar Navigation using st.switch_page
st.sidebar.title('Navigation')

# Get user selection
page = st.sidebar.radio(
    'Go to', ['Login', 'Register', 'Dashboard', 'Create Study Plan']
)

# Use switch_page to navigate dynamically
if page == 'Login':
    st.switch_page('pages/login.py')
elif page == 'Register':
    st.switch_page('pages/register.py')
elif page == 'Dashboard':
    st.switch_page('pages/dashboard.py')
elif page == 'Create Study Plan':
    if 'token' in st.session_state:
        st.switch_page('pages/create_study_plan.py')
    else:
        st.warning('Please log in to create a study plan.')
