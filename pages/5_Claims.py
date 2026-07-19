import streamlit as st
import pandas as pd
from db.database import get_all_claims, update_claim_status
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

# Display count
st.markdown(f"<div style='color: #6B7280; font-size: 0.9375rem; margin-bottom: 1.5rem; font-weight: 500;'>Showing {len(all_claims)} claims</div>", unsafe_allow_html=True)

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
            <div style="margin-top: 1.25rem; padding-top: 1.25rem; border-top: 1px solid #E5E7EB; display: flex; gap: 0.75rem;">
                <button class="btn-primary" style="padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 600; border-radius: 12px;">Approve</button>
                <button class="btn-danger" style="padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 600; border-radius: 12px;">Reject</button>
                <button class="btn-secondary" style="padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 600; border-radius: 12px; margin-left: auto;">View Details</button>
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
