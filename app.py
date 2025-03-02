import streamlit as st

# 🔹 Configure the page
st.set_page_config(
    page_title='MindMosaic',
    page_icon='🧠',
    layout='centered',  # Centering the layout for a better user experience
    initial_sidebar_state='expanded',
)

# 🔹 Sidebar branding
st.sidebar.title('🌟 MindMosaic')
st.sidebar.info('Your personalized study planner.')

# 🔹 Centered welcome screen
with st.container():
    st.title('🧠 Welcome to MindMosaic!')
    st.subheader('Your personalized study planner.')
    st.write(
        """
    MindMosaic helps you create structured study plans and track your learning journey.
    Log in to access your study plans or register to get started!
    """
    )

    # 🔹 Create two columns for navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button('🔑 Login', use_container_width=True):
            st.switch_page('pages/1_Login.py')  # Navigate to login page

    with col2:
        if st.button('📝 Register', use_container_width=True):
            st.switch_page('pages/2_Register.py')  # Navigate to register page
