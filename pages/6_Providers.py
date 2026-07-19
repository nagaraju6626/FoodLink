import streamlit as st
import pandas as pd
from db.database import get_all_providers
from utils.styles import get_custom_css

st.set_page_config(layout="wide", page_title="Providers", initial_sidebar_state="expanded")


def render_html(html: str) -> None:
    """Render a raw HTML block via st.markdown.

    ROOT-CAUSE FIX: Streamlit's markdown renderer follows CommonMark, which
    treats any line indented 4+ spaces as a literal "indented code block"
    and prints it as plain text instead of parsing it as HTML. Any HTML
    string built inside a `with` block (sidebar, columns, etc.) naturally
    picks up that indentation from Python's own code formatting, which is
    exactly why tags like <tr>, <td>, <div> were showing up as raw text on
    this page. Left-stripping each line before handing it to st.markdown
    removes that indentation (harmless for HTML, which doesn't care about
    whitespace between tags) while leaving every class, attribute, and tag
    untouched.
    """
    cleaned = "\n".join(line.lstrip() for line in html.strip("\n").split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)


st.markdown(get_custom_css(), unsafe_allow_html=True)

# =========================================================
#  GLOBAL THEME / SHELL CSS  (sidebar, header, cards, table)
# =========================================================
st.markdown("""
<style>
:root{
    --brand-dark: #1B4D3E;
    --brand-mid: #245A48;
    --brand-light: #EAF3EC;
    --brand-text-soft: #3F6C57;
    --border-soft: #E5E7EB;
    --bg-soft: #FAFAF9;
}

#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* ---------------- Sidebar ---------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--brand-dark) 0%, #163f33 100%);
    padding-top: 0;
}
section[data-testid="stSidebar"] > div { padding-top: 1rem; }
.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 0.5rem 0.5rem 1.25rem 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 0.75rem;
}
.sidebar-logo-icon {
    background: rgba(255,255,255,0.12); border-radius: 10px;
    width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.sidebar-logo-title { color: #FFFFFF; font-weight: 700; font-size: 15px; line-height: 1.1; }
.sidebar-logo-sub { color: rgba(255,255,255,0.55); font-size: 10.5px; }

.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; margin: 2px 0.5rem; border-radius: 8px;
    color: rgba(255,255,255,0.75); font-size: 13.5px; font-weight: 500;
    text-decoration: none; cursor: pointer;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #FFFFFF; }
.nav-item.active { background: #FFFFFF; color: var(--brand-dark); }
.nav-icon { width: 16px; text-align: center; }

.sidebar-footer-card {
    margin: 1.25rem 0.5rem 0.5rem 0.5rem;
    background: rgba(255,255,255,0.08); border-radius: 12px;
    padding: 1rem 0.9rem; text-align: center;
}
.sidebar-footer-card .emoji { font-size: 26px; margin-bottom: 6px; }
.sidebar-footer-card p { color: #FFFFFF; font-size: 12px; font-weight: 500; line-height: 1.4; margin: 0; }

/* ---------------- Top header ---------------- */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 0 1rem 0; border-bottom: 1px solid var(--border-soft); margin-bottom: 1.25rem;
}
.topbar-search {
    background: var(--bg-soft); border: 1px solid var(--border-soft); border-radius: 8px;
    padding: 8px 14px; font-size: 13px; color: #9CA3AF; width: 320px;
}
.topbar-right { display: flex; align-items: center; gap: 18px; }
.topbar-bell {
    width: 34px; height: 34px; border-radius: 50%; background: var(--bg-soft);
    display: flex; align-items: center; justify-content: center; position: relative;
}
.topbar-bell .dot {
    position: absolute; top: 6px; right: 7px; width: 7px; height: 7px; border-radius: 50%;
    background: #EF4444; border: 1.5px solid #fff;
}
.topbar-user { display: flex; align-items: center; gap: 8px; }
.topbar-avatar {
    width: 34px; height: 34px; border-radius: 50%; background: var(--brand-light); color: var(--brand-dark);
    display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px;
}
.topbar-user-name { font-size: 13px; font-weight: 600; color: #111827; line-height: 1.1; }
.topbar-user-role { font-size: 11px; color: var(--brand-dark); font-weight: 500; }

/* ---------------- Page header ---------------- */
.page-header-row {
    display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1.25rem;
}
.page-title { font-size: 24px; font-weight: 700; color: #14312A; margin: 0; }
.page-subtitle { font-size: 13px; color: #6B7280; margin-top: 2px; }
.add-provider-btn {
    background: var(--brand-dark); color: #FFFFFF !important; border: none; border-radius: 8px;
    padding: 10px 18px; font-size: 13.5px; font-weight: 600; cursor: pointer;
    display: flex; align-items: center; gap: 6px; text-decoration: none;
}

/* ---------------- Stat cards ---------------- */
.stat-card {
    background: #FFFFFF; border: 0.5px solid var(--border-soft); border-radius: 12px;
    padding: 1.1rem 1.25rem; display: flex; align-items: center; gap: 12px;
    height: 96px; box-sizing: border-box; width: 100%;
}
.stat-icon {
    width: 42px; height: 42px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 19px; flex-shrink: 0;
}
.stat-icon.blue { background: #E7EEFB; }
.stat-icon.green { background: #E4F5E9; }
.stat-icon.orange { background: #FDEFDF; }
.stat-icon.purple { background: #ECE7FB; }
.stat-content { min-width: 0; flex: 1; }
.stat-label {
    font-size: 12.5px; color: #6B7280; font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.stat-value {
    font-size: 21px; font-weight: 700; color: #14312A; line-height: 1.15; margin: 1px 0;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.stat-hint { font-size: 11px; color: #9CA3AF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ---------------- Filter bar ---------------- */
.filter-bar {
    background: #FFFFFF; border: 0.5px solid var(--border-soft); border-radius: 12px;
    padding: 0.85rem 1rem; display: flex; align-items: center; gap: 10px; margin: 1.25rem 0;
}
div[data-testid="stTextInput"] input {
    border-radius: 8px !important; border: 1px solid var(--border-soft) !important; font-size: 13px !important;
}
div[data-testid="stSelectbox"] > div { border-radius: 8px !important; font-size: 13px !important; }

/* ---------------- Table ---------------- */
.table-scroll-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
.provider-table {
    width: 100%;
    min-width: 980px;      /* ensures every column has room before scrolling kicks in */
    border-collapse: collapse;
    background: #FFFFFF;
    table-layout: fixed;
}
.provider-table thead th {
    text-align: left; font-size: 11.5px; font-weight: 600; color: #6B7280;
    text-transform: uppercase; letter-spacing: 0.03em;
    padding: 12px 14px; border-bottom: 1px solid var(--border-soft); background: #FAFAF9;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.provider-table tbody td {
    padding: 14px; border-bottom: 1px solid #F1F2F4; font-size: 13px; color: #374151;
    vertical-align: middle; overflow: hidden;
}
.provider-table tbody tr:last-child td { border-bottom: none; }

/* Explicit column widths so every column has enough room and nothing
   gets clipped -- Actions especially, which needs space for 3 buttons */
.provider-table th:nth-child(1), .provider-table td:nth-child(1) { width: 18%; }
.provider-table th:nth-child(2), .provider-table td:nth-child(2) { width: 15%; }
.provider-table th:nth-child(3), .provider-table td:nth-child(3) { width: 13%; }
.provider-table th:nth-child(4), .provider-table td:nth-child(4) { width: 10%; }
.provider-table th:nth-child(5), .provider-table td:nth-child(5) { width: 9%; text-align: center; }
.provider-table th:nth-child(6), .provider-table td:nth-child(6) { width: 10%; text-align: center; }
.provider-table th:nth-child(7), .provider-table td:nth-child(7) { width: 9%; }
.provider-table th:nth-child(8), .provider-table td:nth-child(8) { width: 9%; white-space: nowrap; }
.provider-table th:nth-child(9), .provider-table td:nth-child(9) { width: 130px; text-align: center; }

.provider-name-cell { display: flex; align-items: center; gap: 10px; min-width: 0; }
.provider-avatar {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 700; color: #FFFFFF;
}
.provider-name {
    font-weight: 600; color: #111827; font-size: 13px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;
}
.contact-email {
    font-size: 12.5px; color: #111827;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.contact-phone { font-size: 12px; color: #9CA3AF; white-space: nowrap; }
.location-cell { display: flex; align-items: flex-start; gap: 5px; min-width: 0; }
.location-cell .pin { color: var(--brand-dark); font-size: 12px; margin-top: 2px; flex-shrink: 0; }
.location-line1 {
    font-size: 12.5px; color: #374151;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.location-line2 { font-size: 11.5px; color: #9CA3AF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.type-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
}
.type-restaurant { background: #E4F5E9; color: #1F8B4C; }
.type-bakery { background: #FDEFDF; color: #C2740A; }
.type-caterer { background: #ECE7FB; color: #6B4FCB; }
.type-supermarket { background: #E7EEFB; color: #2563EB; }
.type-hotel { background: #E4F5E9; color: #1F8B4C; }
.type-sweetshop { background: #FDEFDF; color: #C2740A; }

.status-pill { display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 500; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; }
.status-dot.active { background: #22C55E; }
.status-dot.inactive { background: #F59E0B; }
.status-active-text { color: #16A34A; }
.status-inactive-text { color: #D97706; }

.action-icons { display: flex; gap: 6px; justify-content: center; align-items: center; flex-wrap: nowrap; }
.action-icon {
    width: 30px; height: 30px; border-radius: 6px; border: 1px solid var(--border-soft);
    display: flex; align-items: center; justify-content: center; font-size: 12px; cursor: pointer;
    background: #fff; flex-shrink: 0;
}
.action-icon.danger { color: #EF4444; border-color: #FCE4E4; background: #FEF3F3; }

/* ---------------- Pagination ---------------- */
.pagination-row { display: flex; justify-content: center; align-items: center; gap: 6px; margin-top: 1.25rem; }
.page-btn {
    min-width: 32px; height: 32px; border-radius: 8px; border: 1px solid var(--border-soft);
    background: #FFFFFF; display: flex; align-items: center; justify-content: center;
    font-size: 12.5px; color: #374151; padding: 0 10px;
}
.page-btn.active { background: var(--brand-dark); color: #FFFFFF; border-color: var(--brand-dark); font-weight: 600; }/* ---------------- Professional bordered card shell ----------------
   (matches the card style used elsewhere in the app; applied to any
   st.container(border=True), e.g. the search/filter bar below) */
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background: #FFFFFF;
    border: 0.5px solid var(--border-soft);
    border-radius: 12px;
    padding: 1rem 1.1rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }

/* ---------------- Buttons: never wrap to a second line ---------------- */
div[data-testid="stButton"] > button {
    white-space: nowrap;
}

/* Filter / Refresh buttons: consistent outlined style, vertically aligned
   with the search box and dropdowns next to them */
div.st-key-filter_btn button, div.st-key-refresh_btn button {
    background: #FFFFFF !important;
    border: 1px solid var(--border-soft) !important;
    color: #374151 !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
}
div.st-key-filter_btn button:hover, div.st-key-refresh_btn button:hover {
    border-color: var(--brand-dark) !important;
    color: var(--brand-dark) !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
#  TOP HEADER BAR
# =========================================================
render_html("""
<div class="topbar">
    <div class="topbar-search">🔍&nbsp;&nbsp;Search providers...</div>
    <div class="topbar-right">
        <div class="topbar-bell">🔔<span class="dot"></span></div>
        <div class="topbar-user">
            <div class="topbar-avatar">RK</div>
            <div>
                <div class="topbar-user-name">Ramesh Kumar</div>
                <div class="topbar-user-role">Provider</div>
            </div>
        </div>
    </div>
</div>
""")

# =========================================================
#  PAGE HEADER
# =========================================================
hcol1, hcol2 = st.columns([4, 1])
with hcol1:
    render_html("""
    <div class="page-title">Providers</div>
    <div class="page-subtitle">View and manage all food providers in the system.</div>
    """)
with hcol2:
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    st.button("➕ Add Provider", type="primary", use_container_width=True, key="add_provider_btn")

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# =========================================================
#  DATA
#  Replace this block with real data from get_all_providers().
#  Expected columns: name, email, phone, area, city, type, status,
#  total_listings, total_donations, joined_on
# =========================================================
try:
    providers_df = get_all_providers()
    if providers_df is None or len(providers_df) == 0:
        raise ValueError("empty")
except Exception:
    providers_df = pd.DataFrame([
        {"name": "Foodies Restaurant", "email": "foodies@example.com", "phone": "+91 98765 43210",
         "area": "Banjara Hills", "city": "Hyderabad", "type": "Restaurant", "status": "Active",
         "total_listings": 18, "total_donations": 85, "joined_on": "May 10, 2025"},
        {"name": "Green Valley Bakery", "email": "contact@greenvalley.com", "phone": "+91 91234 56789",
         "area": "Jubilee Hills", "city": "Hyderabad", "type": "Bakery", "status": "Active",
         "total_listings": 12, "total_donations": 40, "joined_on": "Apr 28, 2025"},
        {"name": "Spice Route Caterers", "email": "info@spiceroute.com", "phone": "+91 99876 54321",
         "area": "Madhapur", "city": "Hyderabad", "type": "Caterer", "status": "Active",
         "total_listings": 24, "total_donations": 112, "joined_on": "Apr 15, 2025"},
        {"name": "Fresh Mart Supermarket", "email": "hello@freshmart.com", "phone": "+91 90123 45678",
         "area": "Kukatpally", "city": "Hyderabad", "type": "Supermarket", "status": "Inactive",
         "total_listings": 10, "total_donations": 30, "joined_on": "Mar 30, 2025"},
        {"name": "Hotel Grand Inn", "email": "manager@grandinn.com", "phone": "+91 93456 78901",
         "area": "Gachibowli", "city": "Hyderabad", "type": "Hotel", "status": "Active",
         "total_listings": 8, "total_donations": 25, "joined_on": "Mar 18, 2025"},
        {"name": "Sweet Delights", "email": "hello@sweetdelights.com", "phone": "+91 99099 11223",
         "area": "Ameerpet", "city": "Hyderabad", "type": "Sweet Shop", "status": "Inactive",
         "total_listings": 6, "total_donations": 14, "joined_on": "Feb 20, 2025"},
    ])

TYPE_CLASS = {
    "Restaurant": "type-restaurant",
    "Bakery": "type-bakery",
    "Caterer": "type-caterer",
    "Supermarket": "type-supermarket",
    "Hotel": "type-hotel",
    "Sweet Shop": "type-sweetshop",
}
AVATAR_COLORS = ["#8B4A3B", "#B08968", "#5B4B8A", "#4A6B5B", "#3E4A61", "#8A5B4B"]

# =========================================================
#  NORMALIZE COLUMNS
#  Your real DB table may use different column names (or be
#  missing some entirely, e.g. no "status" column). This maps
#  common alternates onto the names this page expects, and
#  fills in sensible defaults for anything still missing so
#  the page never crashes with a KeyError.
# =========================================================
COLUMN_ALIASES = {
    "name": ["name", "provider_name", "business_name", "provider"],
    "email": ["email", "contact_email", "provider_email"],
    "phone": ["phone", "contact_phone", "phone_number", "mobile"],
    "area": ["area", "locality", "address", "location"],
    "city": ["city", "town"],
    "type": ["type", "provider_type", "category"],
    "status": ["status", "provider_status", "is_active", "active"],
    "total_listings": ["total_listings", "listings_count", "num_listings"],
    "total_donations": ["total_donations", "donations_count", "num_donations"],
    "joined_on": ["joined_on", "created_at", "date_joined", "registered_on"],
}

df = providers_df.copy()
df.columns = [str(c).strip() for c in df.columns]

for target_col, aliases in COLUMN_ALIASES.items():
    if target_col in df.columns:
        continue
    found = next((a for a in aliases if a in df.columns), None)
    if found:
        df[target_col] = df[found]

# Fill anything still missing with safe defaults
if "name" not in df.columns:
    df["name"] = "Unknown Provider"
if "email" not in df.columns:
    df["email"] = "—"
if "phone" not in df.columns:
    df["phone"] = "—"
if "area" not in df.columns:
    df["area"] = "—"
if "city" not in df.columns:
    df["city"] = ""
if "type" not in df.columns:
    df["type"] = "Restaurant"
if "status" not in df.columns:
    # No status data available from the DB — default everyone to Active
    df["status"] = "Active"
else:
    # Normalize boolean/1-0 style status values into "Active"/"Inactive" text
    def _norm_status(v):
        if isinstance(v, str):
            return "Active" if v.strip().lower() in ("active", "true", "1", "yes") else "Inactive"
        return "Active" if bool(v) else "Inactive"
    df["status"] = df["status"].apply(_norm_status)
if "total_listings" not in df.columns:
    df["total_listings"] = 0
if "total_donations" not in df.columns:
    df["total_donations"] = 0
if "joined_on" not in df.columns:
    df["joined_on"] = "—"

df["total_listings"] = pd.to_numeric(df["total_listings"], errors="coerce").fillna(0).astype(int)
df["total_donations"] = pd.to_numeric(df["total_donations"], errors="coerce").fillna(0).astype(int)

providers_df = df

total_providers = len(providers_df)
active_providers = int((providers_df["status"] == "Active").sum())
inactive_providers = int((providers_df["status"] == "Inactive").sum())
total_donations = int(providers_df["total_donations"].sum())

# =========================================================
#  STAT CARDS
# =========================================================
s1, s2, s3, s4 = st.columns(4, gap="medium")
with s1:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon blue">👥</div>
        <div class="stat-content">
            <div class="stat-label">Total Providers</div>
            <div class="stat-value">{total_providers}</div>
            <div class="stat-hint">All time</div>
        </div>
    </div>
    """)
with s2:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon green">✅</div>
        <div class="stat-content">
            <div class="stat-label">Active Providers</div>
            <div class="stat-value">{active_providers}</div>
            <div class="stat-hint">Currently active</div>
        </div>
    </div>
    """)
with s3:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon orange">🕐</div>
        <div class="stat-content">
            <div class="stat-label">Inactive Providers</div>
            <div class="stat-value">{inactive_providers}</div>
            <div class="stat-hint">Not active</div>
        </div>
    </div>
    """)
with s4:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon purple">🎁</div>
        <div class="stat-content">
            <div class="stat-label">Total Donations</div>
            <div class="stat-value">{total_donations}</div>
            <div class="stat-hint">All time</div>
        </div>
    </div>
    """)

# =========================================================
#  FILTER BAR
# =========================================================
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
with st.container(border=True):
    f1, f2, f3, f4, f5, f6 = st.columns([3, 1.3, 1.3, 1.3, 1, 1.1], gap="small")
    with f1:
        search_query = st.text_input("Search", placeholder="🔍  Search by name, email, or phone...",
                                      label_visibility="collapsed", key="provider_search")
    with f2:
        status_filter = st.selectbox("Status", ["All Status", "Active", "Inactive"],
                                      label_visibility="collapsed", key="status_filter")
    with f3:
        locations = ["All Locations"] + sorted(providers_df["area"].unique().tolist())
        location_filter = st.selectbox("Location", locations, label_visibility="collapsed", key="location_filter")
    with f4:
        types = ["All Types"] + sorted(providers_df["type"].unique().tolist())
        type_filter = st.selectbox("Type", types, label_visibility="collapsed", key="type_filter")
    with f5:
        st.button("▽ Filter", use_container_width=True, key="filter_btn")
    with f6:
        st.button("↻ Refresh", use_container_width=True, key="refresh_btn")

# ---- Apply filters ----
filtered = providers_df.copy()
if search_query:
    q = search_query.lower()
    filtered = filtered[
        filtered["name"].str.lower().str.contains(q)
        | filtered["email"].str.lower().str.contains(q)
        | filtered["phone"].str.lower().str.contains(q)
    ]
if status_filter != "All Status":
    filtered = filtered[filtered["status"] == status_filter]
if location_filter != "All Locations":
    filtered = filtered[filtered["area"] == location_filter]
if type_filter != "All Types":
    filtered = filtered[filtered["type"] == type_filter]

# =========================================================
#  TABLE
# =========================================================
st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

rows_html = ""
for i, row in filtered.reset_index(drop=True).iterrows():
    initials = "".join([w[0].upper() for w in row["name"].split()[:2]])
    avatar_color = AVATAR_COLORS[i % len(AVATAR_COLORS)]
    type_cls = TYPE_CLASS.get(row["type"], "type-restaurant")
    status_cls = "active" if row["status"] == "Active" else "inactive"
    status_text_cls = "status-active-text" if row["status"] == "Active" else "status-inactive-text"

    rows_html += f"""
    <tr>
        <td>
            <div class="provider-name-cell">
                <div class="provider-avatar" style="background:{avatar_color};">{initials}</div>
                <div class="provider-name">{row['name']}</div>
            </div>
        </td>
        <td>
            <div class="contact-email">{row['email']}</div>
            <div class="contact-phone">{row['phone']}</div>
        </td>
        <td>
            <div class="location-cell">
                <span class="pin">📍</span>
                <div>
                    <div class="location-line1">{row['area']},</div>
                    <div class="location-line2">{row['city']}</div>
                </div>
            </div>
        </td>
        <td><span class="type-badge {type_cls}">{row['type']}</span></td>
        <td>{row['total_listings']}</td>
        <td>{row['total_donations']}</td>
        <td>
            <span class="status-pill">
                <span class="status-dot {status_cls}"></span>
                <span class="{status_text_cls}">{row['status']}</span>
            </span>
        </td>
        <td>{row['joined_on']}</td>
        <td>
            <div class="action-icons">
                <div class="action-icon">👁</div>
                <div class="action-icon">✏️</div>
                <div class="action-icon danger">🗑</div>
            </div>
        </td>
    </tr>
    """

table_html = f"""
<div style="background:#FFFFFF; border:0.5px solid #E5E7EB; border-radius:12px; overflow:hidden;">
<div class="table-scroll-wrapper">
<table class="provider-table">
    <thead>
        <tr>
            <th>Provider</th>
            <th>Contact Info</th>
            <th>Location</th>
            <th>Type</th>
            <th>Total Listings</th>
            <th>Total Donations</th>
            <th>Status</th>
            <th>Joined On</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {rows_html if rows_html else '<tr><td colspan="9" style="text-align:center; padding:2rem; color:#9CA3AF;">No providers found.</td></tr>'}
    </tbody>
</table>
</div>
</div>
"""
render_html(table_html)

# =========================================================
#  PAGINATION (visual — wire up to real paging as needed)
# =========================================================
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
p1, p2, p3, p4, p5, p6, p7 = st.columns([1.1, 0.5, 0.5, 0.5, 0.5, 0.5, 1.1])
with p1:
    st.button("‹ Previous", use_container_width=True, key="prev_page_btn")
with p2:
    st.button("1", use_container_width=True, key="page_1_btn", type="primary")
with p3:
    st.button("2", use_container_width=True, key="page_2_btn")
with p4:
    st.button("3", use_container_width=True, key="page_3_btn")
with p5:
    st.button("4", use_container_width=True, key="page_4_btn")
with p6:
    st.button("5", use_container_width=True, key="page_5_btn")
with p7:
    st.button("Next ›", use_container_width=True, key="next_page_btn")