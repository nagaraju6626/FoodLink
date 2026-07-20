import streamlit as st
from streamlit_option_menu import option_menu
from utils.styles import get_custom_css
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize database
from db.database import init_database

# Page config (must be first st command)
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state['user'] = {
        'name': 'Nagaraju',
        'role': 'Provider',
        'avatar': 'https://via.placeholder.com/40?text=N',
        'notifications': 3
    }

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Dashboard'

if 'navigation' not in st.session_state:
    st.session_state['navigation'] = 'main'

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Define page files before using them
PAGE_FILES = {
    'Dashboard': 'app_pages/1_Dashboard.py',
    'Add Food Listing': 'app_pages/2_Add_Food_Listing.py',
    'Food Listings': 'app_pages/3_Food_Listings.py',
    'My Listings': 'app_pages/4_My_Listings.py',
    'Claims': 'app_pages/5_Claims.py',
    'Providers': 'app_pages/6_Providers.py',
    'Receivers': 'app_pages/7_Receivers.py',
    'Analytics': 'app_pages/8_Analytics.py',
    'Reports': 'app_pages/9_Reports.py',
    'Profile Settings': 'app_pages/10_Profile_Settings.py',
}

# Store navigation in session state
if 'nav_clicked' not in st.session_state:
    st.session_state['nav_clicked'] = None

# Handle navigation from session state
if st.session_state['nav_clicked'] in PAGE_FILES:
    st.session_state['current_page'] = st.session_state['nav_clicked']
    st.session_state['nav_clicked'] = None
    st.rerun()

# Sidebar navigation
NAV_ITEMS = [
    (
        'Dashboard',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<rect x="3" y="3" width="7" height="7"></rect>'
        '<rect x="14" y="3" width="7" height="7"></rect>'
        '<rect x="14" y="14" width="7" height="7"></rect>'
        '<rect x="3" y="14" width="7" height="7"></rect>'
        '</svg>'
    ),
    (
        'Add Food Listing',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<line x1="12" y1="8" x2="12" y2="16"></line>'
        '<line x1="8" y1="12" x2="16" y2="12"></line>'
        '</svg>'
    ),
    (
        'Food Listings',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<line x1="8" y1="6" x2="21" y2="6"></line>'
        '<line x1="8" y1="12" x2="21" y2="12"></line>'
        '<line x1="8" y1="18" x2="21" y2="18"></line>'
        '<line x1="3" y1="6" x2="3.01" y2="6"></line>'
        '<line x1="3" y1="12" x2="3.01" y2="12"></line>'
        '<line x1="3" y1="18" x2="3.01" y2="18"></line>'
        '</svg>'
    ),
    (
        'My Listings',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>'
        '<circle cx="12" cy="7" r="4"></circle>'
        '</svg>'
    ),
    (
        'Claims',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<line x1="16" y1="13" x2="8" y2="13"></line>'
        '<line x1="16" y1="17" x2="8" y2="17"></line>'
        '<polyline points="10 9 9 9 8 9"></polyline>'
        '</svg>'
    ),
    (
        'Providers',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>'
        '<circle cx="9" cy="7" r="4"></circle>'
        '<path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"></path>'
        '</svg>'
    ),
    (
        'Receivers',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>'
        '</svg>'
    ),
    (
        'Analytics',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<line x1="18" y1="20" x2="18" y2="10"></line>'
        '<line x1="12" y1="20" x2="12" y2="4"></line>'
        '<line x1="6" y1="20" x2="6" y2="14"></line>'
        '</svg>'
    ),
    (
        'Reports',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<line x1="16" y1="13" x2="8" y2="13"></line>'
        '<line x1="16" y1="17" x2="8" y2="17"></line>'
        '<polyline points="10 9 9 9 8 9"></polyline>'
        '</svg>'
    ),
    (
        'Profile Settings',
        '<svg class="sidebar-nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4z"></path>'
        '<path d="M6 20c0-2.21 3.58-4 8-4s8 1.79 8 4"></path>'
        '</svg>'
    ),
]

with st.sidebar:
    # Logo and title
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
            </svg>
        </div>
        <div>
            <div class="sidebar-logo-title">Local Food Wastage</div>
            <div class="sidebar-logo-subtitle">Management System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">MANAGEMENT</div>', unsafe_allow_html=True)

    # Create a form for navigation (uses session state, no URL changes)
    with st.form(key='nav_form', clear_on_submit=True):
        for label, icon_html in NAV_ITEMS:
            active_cls = 'active' if label == st.session_state['current_page'] else ''
            # Use custom-styled button that looks like div
            if st.form_submit_button(
                label=f"  {label}",
                help=label,
                use_container_width=True
            ):
                st.session_state['nav_clicked'] = label
                st.rerun()
    
    # Add hidden inputs to track current page for styling
    st.session_state['current_page'] = st.session_state.get('current_page', 'Dashboard')

    st.markdown("""
    <div class="sidebar-bottom-card">
        <div class="sidebar-bottom-icon">
            <span style="font-size: 18px; line-height: 1;">🌍</span>
        </div>
        <div class="sidebar-bottom-text-container">
            <div class="sidebar-bottom-title">Local Food Wastage</div>
            <div class="sidebar-bottom-subtitle">Management System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page routing
selected_page = st.session_state.get('current_page', 'Dashboard')
page_path = PAGE_FILES.get(selected_page, 'pages/1_Dashboard.py')
try:
    with open(page_path, 'r', encoding='utf-8') as f:
        page_code = f.read()
    exec(page_code, {"__name__": "__main__"})
except FileNotFoundError:
    st.error(f"Page not found: {selected_page}")
except Exception as e:
    st.error(f"Error loading page: {str(e)}")

# Initialize database on first run
if 'db_initialized' not in st.session_state:
    init_database()
    st.session_state['db_initialized'] = True
