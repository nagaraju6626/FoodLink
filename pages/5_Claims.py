import streamlit as st
import pandas as pd
from db.database import get_all_claims, update_claim_status, approve_claim, reject_claim, complete_claim
from utils.helpers import time_ago, get_status_badge_class, format_quantity, get_initials, get_avatar_color
from utils.styles import get_custom_css

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="animate-fade-in"><h1 class="header-title">Claims</h1><p class="header-subtitle">Manage food claims and track their status.</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Status filter
status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Completed", "Rejected"])

# Get claims data
@st.cache_data(ttl=60)
def load_claims():
    return get_all_claims()

with st.spinner("Loading claims..."):
    all_claims = load_claims()

# Apply filter
if status_filter != "All":
    all_claims = all_claims[all_claims['status'] == status_filter]

# Handle claim actions
action_performed = None
action_claim_id = None

# Check for button clicks using session state
for idx, row in all_claims.iterrows():
    claim_id = row['id']
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if row['status'] == 'Pending':
            if st.button("Approve", key=f"approve_{claim_id}", use_container_width=True):
                try:
                    approve_claim(claim_id)
                    st.cache_data.clear()
                    st.success(f"Claim approved for {row['receiver_name']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        elif row['status'] == 'Approved':
            st.button("✓ Approved", key=f"approved_{claim_id}", use_container_width=True, disabled=True)
    
    with col2:
        if row['status'] in ['Pending', 'Approved']:
            if st.button("Reject", key=f"reject_{claim_id}", use_container_width=True):
                try:
                    reject_claim(claim_id)
                    st.cache_data.clear()
                    st.warning(f"Claim rejected for {row['receiver_name']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        elif row['status'] == 'Rejected':
            st.button("✗ Rejected", key=f"rejected_{claim_id}", use_container_width=True, disabled=True)
    
    with col3:
        if row['status'] == 'Approved':
            if st.button("Mark Complete", key=f"complete_{claim_id}", use_container_width=True, type="primary"):
                try:
                    complete_claim(claim_id)
                    st.cache_data.clear()
                    st.success(f"Claim marked as complete for {row['receiver_name']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Display count
st.markdown(f"<div style='color: #6B7280; font-size: 0.9375rem; margin-bottom: 1.5rem; font-weight: 500; margin-top: 1rem;'>Showing {len(all_claims)} claims</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

if not all_claims.empty:
    for idx, row in all_claims.iterrows():
        status_class = get_status_badge_class(row['status'])
        initials = get_initials(row['receiver_name'])
        avatar_color = get_avatar_color(row['receiver_name'])
        
        st.markdown(f"""
        <div class="card animate-fade-in" style="margin-bottom: 1.25rem; animation-delay: {0.05 * idx}s;">
            <div style="display: flex; align-items: center; gap: 1.25rem;">
                <div class="avatar {avatar_color}" style="width: 52px; height: 52px; font-size: 1.0625rem;">{initials}</div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
                        <div style="font-weight: 700; color: #111827; font-size: 1.0625rem;">{row['receiver_name']}</div>
                        <div class="status-badge {status_class}">{row['status']}</div>
                    </div>
                    <div style="font-size: 0.875rem; color: #6B7280; margin-bottom: 0.25rem;">
                        Claimed {format_quantity(row['quantity_claimed'], '')} of <span style="font-weight: 600; color: #374151;">{row['food_name']}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #9CA3AF;">{time_ago(row['claimed_at'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📋</div>
        <div class="empty-state-text">No claims found matching your filters.</div>
    </div>
    """, unsafe_allow_html=True)
