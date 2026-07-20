import streamlit as st
import pandas as pd
import math
from datetime import datetime
from db.database import get_all_food_listings, claim_food_listing
from utils.helpers import format_quantity, get_initials, get_avatar_color
from utils.styles import get_custom_css

st.set_page_config(layout="wide", page_title="Food Listings")

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background: #FFFFFF;
    border: 0.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
}
.stat-mini {
    display: flex; align-items: center; gap: 10px;
}
.stat-icon-tile {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.stat-mini-label { font-size: 12px; color: #6B7280; margin-bottom: 2px; }
.stat-mini-value { font-size: 20px; font-weight: 500; color: #111827; }
.stat-mini-sub { font-size: 10.5px; color: #9CA3AF; }
.food-card-img {
    width: 100%; height: 140px; border-radius: 10px; object-fit: cover;
    background: #F3F4F6;
}
.food-card-img-fallback {
    width: 100%; height: 140px; border-radius: 10px;
    background: #E9F3EC; display: flex; align-items: center; justify-content: center;
}
.food-card-status {
    position: absolute; top: 10px; right: 10px;
    font-size: 10.5px; font-weight: 500; padding: 3px 10px; border-radius: 999px;
}
.food-card-name { font-size: 15px; font-weight: 500; color: #111827; margin: 10px 0 4px; }
.food-card-tags { display: flex; gap: 6px; margin-bottom: 8px; }
.tag-pill { font-size: 10.5px; padding: 2px 9px; border-radius: 999px; font-weight: 500; }
.food-card-detail-row {
    display: flex; align-items: center; justify-content: space-between;
    font-size: 11.5px; color: #6B7280; padding: 3px 0;
}
.food-card-detail-label { display: flex; align-items: center; gap: 5px; color: #9CA3AF; }
.food-card-detail-value { color: #374151; font-weight: 500; }
.page-btn button {
    min-width: 34px !important; padding: 4px 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header row ----------------
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown("""
    <div class="animate-fade-in">
        <h1 class="header-title">Food Listings</h1>
        <p class="header-subtitle">Browse and claim available food donations.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Filters + Refresh ----------------
with st.container(border=True):
    fcol1, fcol2, fcol3, fcol4, fcol5, fcol6 = st.columns([2, 1, 1, 1, 1, 0.8], gap="small")
    with fcol1:
        search_filter = st.text_input("Search", placeholder="Search food, category, provider…", label_visibility="collapsed", key="search_filter")
    with fcol2:
        food_type_filter = st.selectbox("Category", ["All Categories", "Cooked Food", "Fruits", "Vegetables", "Bakery", "Others"], label_visibility="collapsed", key="food_type_filter")
    with fcol3:
        food_kind_filter = st.selectbox("Food Types", ["All Food Types", "Veg", "Non-Veg", "Vegan"], label_visibility="collapsed", key="food_kind_filter")
    with fcol4:
        status_filter = st.selectbox("Availability", ["All Availability", "Available", "Claimed", "Expired"], label_visibility="collapsed", key="status_filter")
    with fcol5:
        location_filter = st.text_input("Location", placeholder="All Locations", label_visibility="collapsed", key="location_filter")
    with fcol6:
        refresh_clicked = st.button("↻ Refresh", use_container_width=True, type="primary", key="refresh_btn")

if refresh_clicked:
    st.cache_data.clear()
    st.rerun()

# ---------------- Load data ----------------
@st.cache_data(ttl=60)
def load_food_listings():
    return get_all_food_listings()

with st.spinner("Loading food listings..."):
    all_listings = load_food_listings()

# ---------------- Stat cards ----------------
total_count = len(all_listings)
available_count = len(all_listings[all_listings['status'] == 'Available']) if not all_listings.empty else 0
claimed_count = len(all_listings[all_listings['status'] == 'Claimed']) if not all_listings.empty else 0
expired_count = len(all_listings[all_listings['status'] == 'Expired']) if not all_listings.empty else 0

box_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""
check_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
badge_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#378ADD" stroke-width="2"><circle cx="12" cy="8" r="6"></circle><path d="M9 14l-3 8 6-3 6 3-3-8"></path></svg>"""
clock_stat_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D8973C" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

s1, s2, s3, s4 = st.columns(4, gap="small")
with s1:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#E9F3EC;">{box_icon}</div>
            <div>
                <div class="stat-mini-label">Total Listings</div>
                <div class="stat-mini-value">{total_count}</div>
                <div class="stat-mini-sub">All time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
with s2:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#E9F3EC;">{check_icon}</div>
            <div>
                <div class="stat-mini-label">Available Food</div>
                <div class="stat-mini-value">{available_count}</div>
                <div class="stat-mini-sub">Currently available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
with s3:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#E6F1FB;">{badge_icon}</div>
            <div>
                <div class="stat-mini-label">Claimed Food</div>
                <div class="stat-mini-value">{claimed_count}</div>
                <div class="stat-mini-sub">Successfully claimed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
with s4:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#FAEEDA;">{clock_stat_icon}</div>
            <div>
                <div class="stat-mini-label">Expired Food</div>
                <div class="stat-mini-value">{expired_count}</div>
                <div class="stat-mini-sub">No longer available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ---------------- Apply filters ----------------
filtered = all_listings.copy()

if food_type_filter != "All Categories":
    filtered = filtered[filtered['food_type'] == food_type_filter]
if food_kind_filter != "All Food Types" and 'diet_type' in filtered.columns:
    filtered = filtered[filtered['diet_type'] == food_kind_filter]
if status_filter != "All Availability":
    filtered = filtered[filtered['status'] == status_filter]
if location_filter:
    filtered = filtered[filtered['location'].str.contains(location_filter, case=False, na=False)]
if search_filter:
    mask = (
        filtered['food_name'].str.contains(search_filter, case=False, na=False)
        | filtered['food_type'].str.contains(search_filter, case=False, na=False)
        | filtered['provider_name'].str.contains(search_filter, case=False, na=False)
    )
    filtered = filtered[mask]

filtered = filtered.sort_values('created_at', ascending=False).reset_index(drop=True)

# ---------------- Pagination ----------------
PAGE_SIZE = 8
total_pages = max(1, math.ceil(len(filtered) / PAGE_SIZE))
if "listings_page" not in st.session_state:
    st.session_state.listings_page = 1
st.session_state.listings_page = min(st.session_state.listings_page, total_pages)

start_idx = (st.session_state.listings_page - 1) * PAGE_SIZE
page_data = filtered.iloc[start_idx:start_idx + PAGE_SIZE]

# ---------------- Food card grid (4 columns) ----------------
food_icon = """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="1.5"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"></path><path d="M7 2v20"></path><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"></path></svg>"""
pin_icon = """<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>"""
person_icon = """<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
qty_icon = """<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>"""
time_icon = """<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

status_colors = {
    "Available": ("#E9F3EC", "#1B4D3E"),
    "Claimed": ("#E6F1FB", "#0C447C"),
    "Pending": ("#FAEEDA", "#854F0B"),
    "Expired": ("#F1EFE8", "#5F5E5A"),
}

if not page_data.empty:
    rows = [page_data.iloc[i:i + 4] for i in range(0, len(page_data), 4)]
    for row_chunk in rows:
        cols = st.columns(4, gap="small")
        for col, (_, item) in zip(cols, row_chunk.iterrows()):
            with col:
                with st.container(border=True):
                    status = item['status']
                    bg, fg = status_colors.get(status, ("#F1EFE8", "#5F5E5A"))

                    if item.get('image_url'):
                        st.markdown(f'<div style="position:relative;"><img src="{item["image_url"]}" class="food-card-img"><div class="food-card-status" style="background:{bg}; color:{fg};">{status}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="position:relative;"><div class="food-card-img-fallback">{food_icon}</div><div class="food-card-status" style="background:{bg}; color:{fg};">{status}</div></div>', unsafe_allow_html=True)

                    diet = item.get('diet_type', 'Veg') or 'Veg'
                    st.markdown(f"""
                    <div class="food-card-name">{item['food_name']}</div>
                    <div class="food-card-tags">
                        <span class="tag-pill" style="background:#E9F3EC; color:#1B4D3E;">{item['food_type']}</span>
                        <span class="tag-pill" style="background:#F1EFE8; color:#5F5E5A;">{diet}</span>
                    </div>
                    <div class="food-card-detail-row">
                        <span class="food-card-detail-label">{qty_icon} Quantity</span>
                        <span class="food-card-detail-value">{format_quantity(item['quantity'], item['unit'])}</span>
                    </div>
                    <div class="food-card-detail-row">
                        <span class="food-card-detail-label">{person_icon} Provider</span>
                        <span class="food-card-detail-value">{item['provider_name']}</span>
                    </div>
                    <div class="food-card-detail-row">
                        <span class="food-card-detail-label">{pin_icon} Location</span>
                        <span class="food-card-detail-value">{item['location']}</span>
                    </div>
                    <div class="food-card-detail-row">
                        <span class="food-card-detail-label">{time_icon} Expires on</span>
                        <span class="food-card-detail-value">{item['expiry_time']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    bcol1, bcol2 = st.columns(2, gap="small")
                    with bcol1:
                        claim_disabled = status != "Available"
                        claim_clicked = st.button(
                            "Claim Food" if not claim_disabled else "Claimed",
                            key=f"claim_{item['id']}",
                            use_container_width=True,
                            type="primary",
                            disabled=claim_disabled,
                        )

                    with bcol2:
                        st.markdown('<div style="display:flex; align-items:center; justify-content:center; height:38px; background:#F3F4F6; border-radius:6px; font-size:12px; color:#6B7280;">' + f"ID: {item['id']}" + '</div>', unsafe_allow_html=True)

                    if claim_clicked and not claim_disabled:
                        try:
                            claim_food_listing(food_id=item['id'], receiver_id=st.session_state.get("current_user_id", 1), quantity_claimed=item['quantity'])
                            st.cache_data.clear()
                            st.success(f"Claim request sent for {item['food_name']}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Couldn't submit claim: {str(e)}")
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-text">No food listings found matching your filters.</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Pagination controls ----------------
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
if total_pages > 1:
    page_cols = st.columns([1] + [1] * min(total_pages, 5) + [1], gap="small")
    with page_cols[0]:
        if st.button("‹ Previous", disabled=st.session_state.listings_page == 1, use_container_width=True):
            st.session_state.listings_page -= 1
            st.rerun()
    visible_pages = range(1, min(total_pages, 5) + 1)
    for i, p in enumerate(visible_pages):
        with page_cols[i + 1]:
            ptype = "primary" if p == st.session_state.listings_page else "secondary"
            if st.button(str(p), key=f"page_{p}", use_container_width=True, type=ptype):
                st.session_state.listings_page = p
                st.rerun()
    with page_cols[-1]:
        if st.button("Next ›", disabled=st.session_state.listings_page == total_pages, use_container_width=True):
            st.session_state.listings_page += 1
            st.rerun()