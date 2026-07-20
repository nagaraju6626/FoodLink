import streamlit as st
import plotly.graph_objects as go
from db.database import get_kpi_counts, get_kpi_trends, get_listings_trend, get_category_distribution, get_recent_claims, get_recent_listings
from utils.helpers import time_ago, render_kpi_card, render_listing_row, render_claim_row, render_cta_banner, format_quantity, get_initials
from utils.styles import get_custom_css

st.set_page_config(layout="wide", page_title="Dashboard")

st.markdown(get_custom_css(), unsafe_allow_html=True)

# Handle "View all" navigation via session state
if 'view_all_page' in st.session_state and st.session_state.view_all_page:
    st.session_state['nav_clicked'] = st.session_state.view_all_page
    st.session_state.view_all_page = None
    st.rerun()

# Restyle Streamlit's native bordered container to act as our "card"
# (fixes the empty-white-box bug caused by splitting HTML across calls)
st.markdown("""
<style>
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background: #FFFFFF;
    border: 0.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Top Navbar ----------------
st.markdown("""
<div class="top-navbar">
    <div class="top-navbar-left">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <div class="search-bar">
            <svg class="search-bar-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" placeholder="Search anything…">
            <span class="search-bar-badge">Ctrl K</span>
        </div>
    </div>
    <div class="top-navbar-right">
        <div class="notification-bell">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <div class="notification-badge">3</div>
        </div>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
        <div class="user-profile">
            <div class="user-avatar">N</div>
            <div class="user-info">
                <div class="user-name">Nagaraju</div>
                <div class="user-role">Provider</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- Data loading ----------------
@st.cache_data(ttl=60)
def load_kpi_data():
    return get_kpi_counts()

@st.cache_data(ttl=60)
def load_kpi_trends():
    return get_kpi_trends()

@st.cache_data(ttl=60)
def load_trend_data():
    return get_listings_trend('month')

@st.cache_data(ttl=60)
def load_category_data():
    return get_category_distribution()

@st.cache_data(ttl=60)
def load_recent_listings():
    return get_recent_listings(3)

@st.cache_data(ttl=60)
def load_recent_claims():
    return get_recent_claims(3)

with st.spinner("Loading dashboard data..."):
    kpi_data = load_kpi_data()
    kpi_trends = load_kpi_trends()
    trend_data = load_trend_data()
    category_data = load_category_data()
    recent_listings = load_recent_listings()
    recent_claims = load_recent_claims()

# ---------------- Welcome + Banner Row ----------------
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin: 1.25rem 0;">
    <div style="flex: 1;">
        <div class="header-title">Welcome back, Nagaraju</div>
        <div class="header-subtitle">Together, let's reduce food waste and feed more people in need.</div>
    </div>
    <div class="welcome-banner">
        <div class="welcome-banner-text">
            <div class="welcome-banner-title">Don't waste food,<br>make a difference!</div>
            <button class="btn-light-pill">Donate food →</button>
        </div>
        <div class="welcome-banner-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- KPI Card Row ----------------
package_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
    <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
    <line x1="12" y1="22.08" x2="12" y2="12"></line>
</svg>"""

store_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 21h18"></path>
    <path d="M5 21V7l8-4 8 4v14"></path>
    <path d="M17 21v-8.5a2.5 2.5 0 0 0-5 0V21"></path>
</svg>"""

users_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
    <circle cx="9" cy="7" r="4"></circle>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
</svg>"""

clipboard_icon = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
    <path d="M9 14h6"></path>
    <path d="M9 10h6"></path>
    <path d="M9 18h6"></path>
</svg>"""

col1, col2, col3, col4 = st.columns(4, gap="small")
with col1:
    st.markdown(render_kpi_card("Total food listings", kpi_data['total_listings'], kpi_trends['listings_trend'], 'green', package_icon), unsafe_allow_html=True)
with col2:
    st.markdown(render_kpi_card("Total providers", kpi_data['total_providers'], kpi_trends['providers_trend'], 'blue', store_icon), unsafe_allow_html=True)
with col3:
    st.markdown(render_kpi_card("Total receivers", kpi_data['total_receivers'], kpi_trends['receivers_trend'], 'purple', users_icon), unsafe_allow_html=True)
with col4:
    st.markdown(render_kpi_card("Total claims", kpi_data['total_claims'], kpi_trends['claims_trend'], 'amber', clipboard_icon), unsafe_allow_html=True)

st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# ---------------- Charts row ----------------
chart_col1, chart_col2 = st.columns([1.6, 1], gap="small")

with chart_col1:
    with st.container(border=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="section-title" style="margin:0;">Food listings overview</div>', unsafe_allow_html=True)
        with c2:
            period = st.selectbox("period", ["This month", "This week", "Last 3 months"], label_visibility="collapsed", key="trend_period")

        if not trend_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend_data['date'], y=trend_data['count'],
                fill='tozeroy', mode='lines',
                line=dict(color='#1B4D3E', width=2.5, shape='spline'),
                fillcolor='rgba(27, 77, 62, 0.12)',
                hovertemplate='<b>%{x}</b><br>Listings: %{y}<extra></extra>'
            ))
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0), height=250,
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter, sans-serif', size=11, color='#6B7280'),
                showlegend=False, hovermode='x unified',
            )
            fig.update_xaxes(showgrid=False, tickfont=dict(size=10), title=None)
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.06)', tickfont=dict(size=10), title=None)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No listing trend data available yet.")

with chart_col2:
    with st.container(border=True):
        st.markdown('<div class="section-title" style="margin-bottom: 0.5rem;">Food categories</div>', unsafe_allow_html=True)

        if not category_data.empty:
            total = int(category_data['count'].sum())
            colors = ['#1B4D3E', '#D8973C', '#378ADD', '#7F77DD', '#D4537E']

            fig = go.Figure(data=[go.Pie(
                labels=category_data['food_type'], values=category_data['count'],
                hole=0.68, marker=dict(colors=colors[:len(category_data)], line=dict(color='#FFFFFF', width=2)),
                textinfo='none', sort=False,
                hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
            )])
            fig.update_layout(
                annotations=[
                    dict(text=str(total), x=0.5, y=0.54, showarrow=False, font=dict(size=22, color='#111827', family='Inter, sans-serif')),
                    dict(text='total', x=0.5, y=0.42, showarrow=False, font=dict(size=11, color='#6B7280', family='Inter, sans-serif'))
                ],
                margin=dict(l=0, r=0, t=0, b=0), height=190, showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            legend_html = '<div>'
            for idx, row in category_data.iterrows():
                color = colors[idx % len(colors)]
                pct = round((row['count'] / total) * 100, 1) if total else 0
                legend_html += (
                    '<div class="legend-item">'
                    f'<div class="legend-color" style="background:{color};"></div>'
                    f'<div class="legend-label">{row["food_type"]}</div>'
                    f'<div class="legend-value">{row["count"]} ({pct}%)</div>'
                    '</div>'
                )
            legend_html += '</div>'
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.info("No category data available yet.")

# ---------------- Activity row ----------------
activity_col1, activity_col2 = st.columns([1.6, 1], gap="small")

with activity_col1:
    with st.container(border=True):
        h1, h2 = st.columns([3, 1])
        with h1:
            st.markdown('<div class="section-title" style="margin:0;">Recent food listings</div>', unsafe_allow_html=True)
        with h2:
            if st.button("View all", key="view_all_listings"):
                st.session_state.view_all_page = "Food Listings"
                st.rerun()

        if not recent_listings.empty:
            rows_html = ""
            for _, row in recent_listings.iterrows():
                quantity_str = format_quantity(row['quantity'], row['unit'])
                rows_html += render_listing_row(
                    row['food_name'], row['provider_name'], row['location'],
                    quantity_str, 'Available', row['food_type']
                )
            st.markdown(rows_html, unsafe_allow_html=True)
        else:
            st.info("No recent listings available.")

with activity_col2:
    with st.container(border=True):
        h1, h2 = st.columns([2, 1])
        with h1:
            st.markdown('<div class="section-title" style="margin:0;">Recent claims</div>', unsafe_allow_html=True)
        with h2:
            if st.button("View all", key="view_all_claims"):
                st.session_state.view_all_page = "Claims"
                st.rerun()

        if not recent_claims.empty:
            rows_html = ""
            for _, row in recent_claims.iterrows():
                initial = get_initials(row['receiver_name'])
                quantity_str = format_quantity(row['quantity_claimed'], '')
                time_str = time_ago(row['claimed_at'])
                rows_html += render_claim_row(
                    row['receiver_name'], quantity_str, row['food_name'], time_str, initial
                )
            st.markdown(rows_html, unsafe_allow_html=True)
        else:
            st.info("No recent claims available.")

# ---------------- Bottom CTA Banner ----------------
st.markdown(render_cta_banner(), unsafe_allow_html=True)