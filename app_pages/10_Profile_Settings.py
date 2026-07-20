import streamlit as st
from utils.styles import get_custom_css

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="animate-fade-in"><h1 class="header-title">Profile & Settings</h1><p class="header-subtitle">Manage your profile and application preferences.</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Tabs for Profile and Settings
tab1, tab2 = st.tabs(["Profile", "Settings"])

with tab1:
    st.markdown('<div class="section-title">Profile Information</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Profile form
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value="Nagaraju")
            email = st.text_input("Email", value="nagaraju@example.com")
            phone = st.text_input("Phone", value="+91 98765 43210")
        
        with col2:
            role = st.selectbox("Role", ["Provider", "Receiver", "Admin"], index=0)
            city = st.text_input("City", value="Hyderabad")
            organization = st.text_input("Organization (Optional)", value="")
        
        bio = st.text_area("Bio", value="Passionate about reducing food waste and helping communities.", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            save_profile = st.form_submit_button("Save Profile", use_container_width=True)
        with col2:
            cancel_profile = st.form_submit_button("Cancel", use_container_width=True)
    
    if save_profile:
        st.success("✓ Profile updated successfully!")
        st.session_state['user']['name'] = name

with tab2:
    st.markdown('<div class="section-title">Application Settings</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Notification settings
    st.markdown("### Notification Preferences")
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    email_notifications = st.checkbox("Email Notifications", value=True)
    push_notifications = st.checkbox("Push Notifications", value=True)
    sms_notifications = st.checkbox("SMS Notifications", value=False)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Theme settings
    st.markdown("### Theme Preferences")
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    theme = st.selectbox("Theme", ["Light", "Dark", "System Default"], index=0)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Privacy settings
    st.markdown("### Privacy Settings")
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    profile_visibility = st.selectbox("Profile Visibility", ["Public", "Private", "Registered Users Only"], index=0)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Save settings button
    save_settings = st.button("Save Settings", use_container_width=True)
    
    if save_settings:
        st.success("✓ Settings saved successfully!")

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Danger zone
st.markdown('<div class="card animate-slide-up" style="border-color: #FEE2E4;"><div class="section-title" style="color: #991B1B;">Danger Zone</div>', unsafe_allow_html=True)
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    delete_account = st.button("Delete Account", type="secondary", use_container_width=True)
with col2:
    logout = st.button("Logout", type="secondary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if logout:
    st.session_state.clear()
    st.rerun()
