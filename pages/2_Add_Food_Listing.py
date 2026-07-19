import streamlit as st
import requests
from datetime import datetime, date
from db.database import create_food_listing, get_all_providers
from utils.styles import get_custom_css

st.set_page_config(layout="wide", page_title="Add Food Listing", initial_sidebar_state="expanded")

st.markdown(get_custom_css(), unsafe_allow_html=True)

# =========================================================
#  GLOBAL THEME / SHELL CSS  (sidebar, header, cards, etc.)
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

/* Hide default streamlit chrome */
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* ---------------- Sidebar ---------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--brand-dark) 0%, #163f33 100%);
    padding-top: 0;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0.5rem 1.25rem 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 0.75rem;
}
.sidebar-logo-icon {
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sidebar-logo-title { color: #FFFFFF; font-weight: 700; font-size: 15px; line-height: 1.1; }
.sidebar-logo-sub { color: rgba(255,255,255,0.55); font-size: 10.5px; }

.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    margin: 2px 0.5rem;
    border-radius: 8px;
    color: rgba(255,255,255,0.75);
    font-size: 13.5px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #FFFFFF; }
.nav-item.active { background: #FFFFFF; color: var(--brand-dark); }
.nav-icon { width: 16px; text-align: center; }

.sidebar-footer-card {
    margin: 1.25rem 0.5rem 0.5rem 0.5rem;
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 0.9rem;
    text-align: center;
}
.sidebar-footer-card .emoji { font-size: 26px; margin-bottom: 6px; }
.sidebar-footer-card p {
    color: #FFFFFF; font-size: 12px; font-weight: 500; line-height: 1.4; margin: 0;
}

/* ---------------- Top header ---------------- */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0 1rem 0;
    border-bottom: 1px solid var(--border-soft);
    margin-bottom: 1.25rem;
}
.topbar-search {
    background: var(--bg-soft);
    border: 1px solid var(--border-soft);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    color: #9CA3AF;
    width: 320px;
}
.topbar-right { display: flex; align-items: center; gap: 18px; }
.topbar-bell {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: var(--bg-soft);
    display: flex; align-items: center; justify-content: center;
    position: relative;
}
.topbar-bell .dot {
    position: absolute; top: 6px; right: 7px;
    width: 7px; height: 7px; border-radius: 50%;
    background: #EF4444; border: 1.5px solid #fff;
}
.topbar-user { display: flex; align-items: center; gap: 8px; }
.topbar-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: var(--brand-light); color: var(--brand-dark);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px;
}
.topbar-user-name { font-size: 13px; font-weight: 600; color: #111827; line-height: 1.1; }
.topbar-user-role { font-size: 11px; color: var(--brand-dark); font-weight: 500; }

/* ---------------- Cards / form controls ---------------- */
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background: #FFFFFF;
    border: 0.5px solid var(--border-soft);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }

section[data-testid="stFileUploaderDropzone"] {
    background: var(--bg-soft);
    border: 1.5px dashed #D1D5DB;
    border-radius: 10px;
    padding: 1.5rem;
}
section[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--brand-dark); }

.tip-card { background: var(--brand-light); border-radius: 12px; padding: 1rem 1.1rem; }
.tip-card-title {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; font-weight: 500; color: var(--brand-dark); margin-bottom: 0.6rem;
}
.tip-list-item {
    display: flex; align-items: flex-start; gap: 8px;
    font-size: 12px; color: var(--brand-text-soft); padding: 4px 0;
}

.preview-box {
    background: var(--bg-soft);
    border: 0.5px solid var(--border-soft);
    border-radius: 10px;
    padding: 1.5rem 1rem;
    text-align: center;
    min-height: 160px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.preview-hint { font-size: 11px; color: #9CA3AF; margin-top: 4px; }
.preview-value { font-size: 12px; color: #374151; margin-top: 4px; }

div[data-testid="column"] button { white-space: nowrap; }

/* Primary buttons in brand green */
button[kind="primary"] {
    background-color: var(--brand-dark) !important;
    border-color: var(--brand-dark) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
#  TOP HEADER BAR
# =========================================================
st.markdown("""
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
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("""
<div class="animate-fade-in">
    <h1 class="header-title">Add Food Listing</h1>
    <p class="header-subtitle">Share food with those who need it.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

# ---------------- Session state defaults ----------------
if "location_value" not in st.session_state:
    st.session_state.location_value = ""
if "geo_error" not in st.session_state:
    st.session_state.geo_error = None


def reverse_geocode(lat, lon):
    """Convert lat/lon into a readable address using OpenStreetMap Nominatim."""
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "local-food-wastage-app"},
            timeout=6,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("display_name")
    except Exception:
        pass
    return None


left_col, right_col = st.columns([2, 1], gap="medium")

# ================= LEFT COLUMN =================
with left_col:

    # ---- Card 1: Basic Information ----
    with st.container(border=True):
        st.markdown('<div class="section-title" style="margin-bottom:0.75rem;">Basic Information</div>', unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            food_name = st.text_input("Food Title *", placeholder="e.g., Vegetable Biryani", key="food_name")
        with r1c2:
            food_type = st.selectbox("Food Category *", ["Select Category", "Cooked Food", "Fruits", "Vegetables", "Bakery", "Others"], key="food_type")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            meal_type = st.selectbox("Food Type *", ["Select Type", "Veg", "Non-Veg", "Vegan"], key="meal_type")
        with r2c2:
            qc1, qc2 = st.columns([2, 1])
            with qc1:
                quantity = st.number_input("Quantity *", min_value=0.1, step=0.1, value=1.0, help="e.g., 20 Plates / 5 kg", key="quantity")
            with qc2:
                unit = st.selectbox("Unit", ["Plates", "kg", "liters", "packs", "boxes", "bags"], key="unit")

        description = st.text_area("Food Description", placeholder="Describe the food, ingredients, quality, etc.", height=90, key="description")

        st.markdown('<div style="font-size:13px; font-weight:500; margin-bottom:4px;">Pickup Location *</div>', unsafe_allow_html=True)
        loc_col1, loc_col2 = st.columns([4, 1.3])
        with loc_col1:
            location = st.text_input(
                "Pickup Location",
                value=st.session_state.location_value,
                placeholder="Enter complete address",
                label_visibility="collapsed",
                key="location_input",
            )
            st.session_state.location_value = location
        with loc_col2:
            use_current = st.button("📍 Use my location", use_container_width=True, key="use_location_btn")

        if use_current:
            try:
                # import dynamically to avoid hard dependency at module import time
                import importlib
                mod = importlib.import_module("streamlit_js_eval")
                get_geolocation = getattr(mod, "get_geolocation", None)
                if not get_geolocation:
                    raise ImportError
                geo = get_geolocation()
                if geo and "coords" in geo:
                    lat = geo["coords"]["latitude"]
                    lon = geo["coords"]["longitude"]
                    address = reverse_geocode(lat, lon)
                    if address:
                        st.session_state.location_value = address
                        st.session_state.geo_error = None
                        st.rerun()
                    else:
                        st.session_state.geo_error = "Couldn't resolve an address for your location. Please enter it manually."
                else:
                    st.session_state.geo_error = "Location access denied — please enter your address manually."
            except ImportError:
                st.session_state.geo_error = "Geolocation isn't available. Install `streamlit-js-eval` to enable this, or enter your address manually."

        if st.session_state.geo_error:
            st.warning(st.session_state.geo_error)

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    # ---- Card 2: Additional Details ----
    with st.container(border=True):
        st.markdown('<div class="section-title" style="margin-bottom:0.75rem;">Additional Details</div>', unsafe_allow_html=True)

        d1, d2 = st.columns(2)
        with d1:
            prepared_on = st.date_input("Prepared On", value=date.today(), format="DD-MM-YYYY", key="prepared_on")
        with d2:
            expiry_on = st.date_input("Expiry On", value=date.today(), format="DD-MM-YYYY", key="expiry_on")

        expiry_time_of_day = st.time_input("Expiry Time", value=datetime.now().time(), key="expiry_time_of_day")

        st.markdown('<div style="font-size:13px; font-weight:500; margin:0.75rem 0 4px;">Food Image</div>', unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "Food Image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            help="Drag & drop an image here or click to browse",
            key="uploaded_image",
        )

        providers = get_all_providers()
        provider_options = {f"{row['name']} (ID: {row['id']})": row['id'] for _, row in providers.iterrows()}
        provider_label = st.selectbox("Provider *", list(provider_options.keys()), key="provider_label")
        provider_id = provider_options[provider_label]

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3 = st.columns([3, 1, 1])
    with btn_col2:
        reset = st.button("Reset", use_container_width=True, key="reset_btn")
    with btn_col3:
        submit = st.button("Submit Listing", use_container_width=True, type="primary", key="submit_btn")

    # ---- Handle reset ----
    if reset:
        for key in ["food_name", "food_type", "meal_type", "quantity", "unit",
                     "description", "location_input", "uploaded_image", "geo_error"]:
            st.session_state.pop(key, None)
        st.session_state.location_value = ""
        st.rerun()

    # ---- Handle submission ----
    if submit:
        if food_name and food_type != "Select Category" and quantity and location:
            try:
                expiry_datetime = datetime.combine(expiry_on, expiry_time_of_day)
                image_url = None
                if uploaded_image is not None:
                    image_url = uploaded_image.name  # replace with real save/upload logic as needed

                food_id = create_food_listing(
                    food_name=food_name,
                    food_type=food_type,
                    meal_type=meal_type,
                    quantity=quantity,
                    unit=unit,
                    provider_id=provider_id,
                    location=location,
                    expiry_time=expiry_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    image_url=image_url
                )
                st.success(f"✓ Food listing added successfully! (ID: {food_id})")
                st.balloons()
            except Exception as e:
                st.error(f"Error adding food listing: {str(e)}")
        else:
            st.warning("Please fill in all required fields.")

# ================= RIGHT COLUMN =================
with right_col:
    with st.container(border=True):
        st.markdown('<div class="section-title" style="margin-bottom:0.75rem;">Preview</div>', unsafe_allow_html=True)

        has_image = st.session_state.get("uploaded_image") is not None
        has_title = bool(st.session_state.get("food_name"))
        has_location = bool(st.session_state.get("location_value"))

        if has_image:
            st.image(st.session_state["uploaded_image"], use_container_width=True)
        else:
            st.markdown("""
            <div class="preview-box" style="min-height:110px;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="1.5">
                    <path d="M4 19h16"></path>
                    <path d="M6 19V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v11"></path>
                    <path d="M9 12h6"></path>
                    <path d="M9 16h6"></path>
                </svg>
                <div style="font-size:12.5px; color:#6B7280; margin-top:8px; font-weight:500;">No image selected</div>
            </div>
            """, unsafe_allow_html=True)

        title_html = (
            f'<div class="preview-value" style="font-weight:500; font-size:14px; color:#111827;">{st.session_state.get("food_name")}</div>'
            if has_title else '<div class="preview-hint">Title will appear here</div>'
        )

        qty_val = st.session_state.get("quantity")
        unit_val = st.session_state.get("unit", "")
        quantity_html = (
            f'<div class="preview-value">{qty_val} {unit_val}</div>'
            if qty_val else '<div class="preview-hint">Quantity will appear here</div>'
        )

        location_html = (
            f'<div class="preview-value">{st.session_state.get("location_value")}</div>'
            if has_location else '<div class="preview-hint">Location will appear here</div>'
        )

        st.markdown(f"""
        <div style="margin-top:0.5rem;">
            {title_html}
            {quantity_html}
            {location_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-card">
        <div class="tip-card-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18h6"></path>
                <path d="M10 22h4"></path>
                <path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"></path>
            </svg>
            Tips for better response
        </div>
        <div class="tip-list-item">• Provide accurate information</div>
        <div class="tip-list-item">• Add clear food images</div>
        <div class="tip-list-item">• Mention expiry time</div>
        <div class="tip-list-item">• Respond faster</div>
    </div>
    """, unsafe_allow_html=True)