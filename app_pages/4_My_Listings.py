import streamlit as st
import pandas as pd
import math
from db.database import get_food_listings_by_provider, update_food_status, delete_food_listing
from utils.helpers import format_quantity
from utils.styles import get_custom_css

st.set_page_config(layout="wide", page_title="My Listings")

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background: #FFFFFF;
    border: 0.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1rem 1.25rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
}
.stat-mini { display: flex; align-items: center; gap: 10px; }
.stat-icon-tile {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.stat-mini-label { font-size: 12px; color: #6B7280; margin-bottom: 2px; }
.stat-mini-value { font-size: 20px; font-weight: 500; color: #111827; }
.stat-mini-sub { font-size: 10.5px; color: #9CA3AF; }

.table-header-row {
    display: flex;
    padding: 8px 4px;
    background: #F1F5F2;
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 500;
    color: #4B5563;
    margin-bottom: 4px;
}
.table-header-row > div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.food-row-thumb {
    width: 36px; height: 36px; border-radius: 8px;
    background: #E9F3EC; display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-right: 8px;
}
.row-food-name { font-weight: 500; color: #111827; font-size: 12.5px; white-space: nowrap; }
.cell-text { padding-top: 6px; font-size: 12.5px; color: #374151; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tag-pill-sm { font-size: 10.5px; padding: 2px 9px; border-radius: 999px; font-weight: 500; white-space: nowrap; }
.status-dot { width:7px; height:7px; border-radius:50%; display:inline-block; margin-right:5px; flex-shrink:0; }

/* Filter button = solid dark green, not red */
button[kind="primary"] {
    background-color: #1B4D3E !important;
    border-color: #1B4D3E !important;
}
button[kind="primary"]:hover {
    background-color: #163F33 !important;
    border-color: #163F33 !important;
}

/* Keep utility buttons on one line */
div[data-testid="stButton"] button {
    white-space: nowrap !important;
}

/* Compact icon-only action buttons */
.action-btn button {
    padding: 4px 10px !important;
    min-width: 34px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div class="animate-fade-in">
    <h1 class="header-title">My Listings</h1>
    <p class="header-subtitle">Manage all the food items you have listed.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ---------------- Data loading ----------------
provider_id = st.session_state.get("current_user_id", 1)

@st.cache_data(ttl=60)
def load_my_listings(pid):
    return get_food_listings_by_provider(pid)

with st.spinner("Loading your listings..."):
    my_listings = load_my_listings(provider_id)

# Normalize status text for reliable comparisons (fixes stat cards showing 0)
if not my_listings.empty:
    my_listings['status_norm'] = my_listings['status'].astype(str).str.strip().str.capitalize()
else:
    my_listings['status_norm'] = pd.Series(dtype=str)

# ---------------- Stat cards ----------------
total_count = len(my_listings)
available_count = int((my_listings['status_norm'] == 'Available').sum())
pending_count = int((my_listings['status_norm'] == 'Pending').sum())
claimed_count = int((my_listings['status_norm'] == 'Claimed').sum())

box_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""
check_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
clock_stat_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#378ADD" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""
archive_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D8973C" stroke-width="2"><rect x="3" y="4" width="18" height="4" rx="1"></rect><path d="M5 8v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8"></path><path d="M10 12h4"></path></svg>"""

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
                <div class="stat-mini-label">Available</div>
                <div class="stat-mini-value">{available_count}</div>
                <div class="stat-mini-sub">Currently available</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
with s3:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#E6F1FB;">{clock_stat_icon}</div>
            <div>
                <div class="stat-mini-label">Pending</div>
                <div class="stat-mini-value">{pending_count}</div>
                <div class="stat-mini-sub">Awaiting claim</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
with s4:
    with st.container(border=True):
        st.markdown(f"""
        <div class="stat-mini">
            <div class="stat-icon-tile" style="background:#FAEEDA;">{archive_icon}</div>
            <div>
                <div class="stat-mini-label">Claimed</div>
                <div class="stat-mini-value">{claimed_count}</div>
                <div class="stat-mini-sub">Successfully claimed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ---------------- Filter row ----------------
COLUMN_RATIOS = [2.4, 1.1, 1, 1.3, 1.4, 1.3, 1, 1.1]  # shared by header + body rows

with st.container(border=True):
    fcol1, fcol2, fcol3, fcol4, fcol5, fcol6 = st.columns([2.2, 1.2, 1.2, 1.2, 1, 1], gap="small")
    with fcol1:
        search_filter = st.text_input("Search", placeholder="Search your listings…", label_visibility="collapsed", key="my_search")
    with fcol2:
        status_filter = st.selectbox("Status", ["All statuses", "Available", "Pending", "Claimed", "Expired"], label_visibility="collapsed", key="my_status")
    with fcol3:
        category_filter = st.selectbox("Category", ["All categories", "Cooked Food", "Fruits", "Vegetables", "Bakery", "Others"], label_visibility="collapsed", key="my_category")
    with fcol4:
        food_type_filter = st.selectbox("Food type", ["All food types", "Veg", "Non-Veg", "Vegan"], label_visibility="collapsed", key="my_food_type")
    with fcol5:
        filter_clicked = st.button("Filter", use_container_width=True, type="primary", key="filter_btn")
    with fcol6:
        refresh_clicked = st.button("Refresh", use_container_width=True, key="refresh_btn")

if refresh_clicked:
    st.cache_data.clear()
    st.rerun()

# ---------------- Apply filters ----------------
filtered = my_listings.copy()

if status_filter != "All statuses":
    filtered = filtered[filtered['status_norm'] == status_filter]
if category_filter != "All categories":
    filtered = filtered[filtered['food_type'] == category_filter]
if food_type_filter != "All food types" and 'diet_type' in filtered.columns:
    filtered = filtered[filtered['diet_type'] == food_type_filter]
if search_filter:
    filtered = filtered[filtered['food_name'].str.contains(search_filter, case=False, na=False)]

filtered = filtered.sort_values('created_at', ascending=False).reset_index(drop=True)

# ---------------- Pagination ----------------
PAGE_SIZE = 5
total_pages = max(1, math.ceil(len(filtered) / PAGE_SIZE))
if "my_listings_page" not in st.session_state:
    st.session_state.my_listings_page = 1
st.session_state.my_listings_page = min(st.session_state.my_listings_page, total_pages)

start_idx = (st.session_state.my_listings_page - 1) * PAGE_SIZE
page_data = filtered.iloc[start_idx:start_idx + PAGE_SIZE]

# ---------------- Table ----------------
status_colors = {
    "Available": "#639922",
    "Pending": "#EF9F27",
    "Claimed": "#378ADD",
    "Expired": "#888780",
}

food_icon = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1B4D3E" stroke-width="1.6"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"></path><path d="M7 2v20"></path><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"></path></svg>"""

with st.container(border=True):
    header_cols = st.columns(COLUMN_RATIOS, gap="small")
    header_labels = ["Food item", "Category", "Quantity", "Location", "Listed on", "Expires on", "Status", "Actions"]
    for hc, label in zip(header_cols, header_labels):
        with hc:
            align = "text-align:right;" if label == "Actions" else ""
            st.markdown(f'<div style="font-size:11.5px; font-weight:500; color:#4B5563; padding:6px 0; {align}">{label}</div>', unsafe_allow_html=True)
    st.markdown("<div style='border-bottom:1px solid #E5E7EB; margin-bottom:4px;'></div>", unsafe_allow_html=True)

    if not page_data.empty:
        for _, row in page_data.iterrows():
            dot_color = status_colors.get(row['status_norm'], "#888780")
            listed_on = str(row.get("created_at", "—")).split(" ")[0]
            expires_on = str(row.get("expiry_time", "—")).split(" ")[0]

            row_cols = st.columns(COLUMN_RATIOS, gap="small")

            with row_cols[0]:
                st.markdown(f"""
                <div style="display:flex; align-items:center; padding-top:4px;">
                    <div class="food-row-thumb">{food_icon}</div>
                    <div class="row-food-name">{row['food_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            with row_cols[1]:
                st.markdown(f'<div style="padding-top:8px;"><span class="tag-pill-sm" style="background:#E9F3EC; color:#1B4D3E;">{row["food_type"]}</span></div>', unsafe_allow_html=True)
            with row_cols[2]:
                st.markdown(f'<div class="cell-text">{format_quantity(row["quantity"], row["unit"])}</div>', unsafe_allow_html=True)
            with row_cols[3]:
                st.markdown(f'<div class="cell-text">{row["location"]}</div>', unsafe_allow_html=True)
            with row_cols[4]:
                st.markdown(f'<div class="cell-text">{listed_on}</div>', unsafe_allow_html=True)
            with row_cols[5]:
                st.markdown(f'<div class="cell-text">{expires_on}</div>', unsafe_allow_html=True)
            with row_cols[6]:
                st.markdown(f"""
                <div class="cell-text" style="display:flex; align-items:center;">
                    <span class="status-dot" style="background:{dot_color};"></span>{row['status_norm']}
                </div>
                """, unsafe_allow_html=True)
            with row_cols[7]:
                act1, act2, act3 = st.columns(3, gap="small")
                with act1:
                    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                    view_clicked = st.button("👁", key=f"view_{row['id']}", help="View details")
                    st.markdown('</div>', unsafe_allow_html=True)
                with act2:
                    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                    edit_clicked = st.button("✎", key=f"edit_{row['id']}", help="Edit listing")
                    st.markdown('</div>', unsafe_allow_html=True)
                with act3:
                    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
                    delete_clicked = st.button("🗑", key=f"delete_{row['id']}", help="Delete listing")
                    st.markdown('</div>', unsafe_allow_html=True)

                if view_clicked:
                    st.session_state.selected_listing_id = row['id']
                    st.switch_page("pages/3_Food_Listing_Detail.py")

                if edit_clicked:
                    st.session_state.editing_listing_id = row['id']
                    st.switch_page("pages/2_Add_Food_Listing.py")

                if delete_clicked:
                    try:
                        delete_food_listing(row['id'])
                        st.cache_data.clear()
                        st.success(f"Deleted \"{row['food_name']}\".")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Couldn't delete listing: {str(e)}")

            st.markdown("<div style='border-bottom:0.5px solid #F0F0EE; margin:2px 0;'></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-text">You haven't posted any food listings yet.</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- Pagination controls ----------------
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
if total_pages > 1:
    page_cols = st.columns([1] + [1] * min(total_pages, 5) + [1], gap="small")
    with page_cols[0]:
        if st.button("Previous", disabled=st.session_state.my_listings_page == 1, use_container_width=True):
            st.session_state.my_listings_page -= 1
            st.rerun()
    visible_pages = range(1, min(total_pages, 5) + 1)
    for i, p in enumerate(visible_pages):
        with page_cols[i + 1]:
            ptype = "primary" if p == st.session_state.my_listings_page else "secondary"
            if st.button(str(p), key=f"my_page_{p}", use_container_width=True, type=ptype):
                st.session_state.my_listings_page = p
                st.rerun()
    with page_cols[-1]:
        if st.button("Next", disabled=st.session_state.my_listings_page == total_pages, use_container_width=True):
            st.session_state.my_listings_page += 1
            st.rerun()