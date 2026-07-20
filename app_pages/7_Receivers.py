import streamlit as st
import pandas as pd
from db.database import get_all_receivers
from utils.helpers import get_initials, get_avatar_color
from utils.styles import get_custom_css


def render_html(html: str) -> None:
    """Render a raw HTML block via st.markdown.

    ROOT-CAUSE FIX: Streamlit's markdown renderer follows CommonMark, which
    treats any line indented 4+ spaces as a literal "indented code block"
    and prints it as plain text instead of parsing it as HTML. Any HTML
    string built inside a `with` block or a `for` loop naturally picks up
    that indentation from Python's own code formatting -- which is exactly
    why the KPI cards and receiver cards were rendering as raw <div>/<button>
    text instead of actual UI. Left-stripping each line before handing it to
    st.markdown removes that indentation (harmless for HTML, which doesn't
    care about whitespace between tags) while leaving every class,
    attribute, and tag untouched.
    """
    cleaned = "\n".join(line.lstrip() for line in html.strip("\n").split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)


st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown("""
<style>

.receiver-title{
    font-size:38px;
    font-weight:700;
    color:#111827;
    margin-bottom:4px;
}

.receiver-subtitle{
    color:#6B7280;
    font-size:16px;
    margin-bottom:28px;
}

.kpi-card{
    background:#ffffff;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:22px;
    box-shadow:0 5px 18px rgba(0,0,0,.05);
    transition:.25s;
}

.kpi-card:hover{
    transform:translateY(-5px);
    box-shadow:0 15px 30px rgba(0,0,0,.08);
}

.kpi-icon{
    font-size:32px;
    margin-bottom:10px;
}

.kpi-value{
    font-size:32px;
    font-weight:700;
    color:#111827;
}

.kpi-label{
    color:#6B7280;
    font-size:14px;
    margin-top:6px;
}

</style>
""", unsafe_allow_html=True)

render_html("""
<div class="receiver-title">
❤️ Receivers
</div>

<div class="receiver-subtitle">
Manage registered food receivers and organizations.
</div>
""")

REQUIRED_COLUMNS = ["name", "type", "city", "contact"]


@st.cache_data(ttl=60)
def load_receivers():
    return get_all_receivers()


try:
    all_receivers = load_receivers()
    if all_receivers is None:
        raise ValueError("get_all_receivers() returned None")
except Exception as e:
    st.error(f"Couldn't load receivers from the database: {e}")
    all_receivers = pd.DataFrame(columns=REQUIRED_COLUMNS)

# Defensive normalization: guarantee every column this page reads actually
# exists, so a missing/renamed DB column never raises a KeyError.
for col in REQUIRED_COLUMNS:
    if col not in all_receivers.columns:
        all_receivers[col] = "—" if col != "type" else "Unknown"

total_receivers = len(all_receivers)
total_ngo = int((all_receivers["type"] == "NGO").sum())
total_cities = all_receivers["city"].nunique()
total_types = all_receivers["type"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-value">{total_receivers}</div>
        <div class="kpi-label">Total Receivers</div>
    </div>
    """)

with c2:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🏢</div>
        <div class="kpi-value">{total_ngo}</div>
        <div class="kpi-label">NGOs</div>
    </div>
    """)

with c3:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📍</div>
        <div class="kpi-value">{total_cities}</div>
        <div class="kpi-label">Cities</div>
    </div>
    """)

with c4:
    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📋</div>
        <div class="kpi-value">{total_types}</div>
        <div class="kpi-label">Organization Types</div>
    </div>
    """)

st.markdown("<br>", unsafe_allow_html=True)
search_col, filter_col, refresh_col = st.columns([4, 2, 1])

with search_col:
    search_term = st.text_input(
        "Search",
        placeholder="🔍 Search by receiver name, city or organization...",
        label_visibility="collapsed",
        key="receiver_search",
    )

with filter_col:
    type_filter = st.selectbox(
        "Type",
        [
            "All",
            "Shelter",
            "Food Bank",
            "NGO",
            "Community Center",
            "Religious Organization",
            "Senior Center",
            "Youth Center",
        ],
        label_visibility="collapsed",
        key="receiver_type_filter",
    )

with refresh_col:
    if st.button("🔄 Refresh", use_container_width=True, key="receiver_refresh_btn"):
        # Scoped to this page's cached data only -- clearing
        # st.cache_data.clear() would wipe every cached function
        # across the entire app, including other pages.
        load_receivers.clear()
        st.rerun()

filtered_receivers = all_receivers.copy()

if search_term:
    filtered_receivers = filtered_receivers[
        filtered_receivers["name"].astype(str).str.contains(search_term, case=False, na=False)
        | filtered_receivers["city"].astype(str).str.contains(search_term, case=False, na=False)
        | filtered_receivers["type"].astype(str).str.contains(search_term, case=False, na=False)
    ]

if type_filter != "All":
    filtered_receivers = filtered_receivers[filtered_receivers["type"] == type_filter]

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([6, 1])

with left:
    render_html(f"""
    <div style="
    font-size:15px;
    color:#6B7280;
    font-weight:600;
    margin-top:8px;">
    Showing <b>{len(filtered_receivers)}</b> of <b>{len(all_receivers)}</b> receivers
    </div>
    """)

with right:
    st.download_button(
        "⬇ Export",
        filtered_receivers.to_csv(index=False),
        "receivers.csv",
        "text/csv",
        use_container_width=True,
        key="receiver_export_btn",
    )

st.markdown("<br>", unsafe_allow_html=True)

if not filtered_receivers.empty:
    for idx, row in filtered_receivers.iterrows():
        name = row["name"] if pd.notna(row["name"]) else "Unnamed Receiver"
        initials = get_initials(name)
        avatar_color = get_avatar_color(name)

        render_html(f"""
        <div style="
            background:white;
            border:1px solid #E5E7EB;
            border-radius:18px;
            padding:22px;
            margin-bottom:18px;
            box-shadow:0 4px 18px rgba(0,0,0,.05);
            transition:.3s;">

        <div style="display:flex;align-items:center;justify-content:space-between;">

            <div style="display:flex;align-items:center;gap:18px;">

                <div class="avatar {avatar_color}"
                     style="width:70px;height:70px;font-size:24px;">
                     {initials}
                </div>

                <div>

                    <div style="
                        font-size:20px;
                        font-weight:700;
                        color:#111827;">
                        {name}
                    </div>

                    <div style="
                        color:#6B7280;
                        font-size:15px;
                        margin-top:4px;">
                        🏢 {row['type']}
                    </div>

                    <div style="
                        color:#6B7280;
                        font-size:14px;
                        margin-top:6px;">
                        📍 {row['city']}
                    </div>

                    <div style="
                        color:#6B7280;
                        font-size:14px;
                        margin-top:4px;">
                        📞 {row['contact']}
                    </div>

                </div>

            </div>

            <div style="text-align:right;">

                <div style="
                    display:inline-block;
                    background:#DCFCE7;
                    color:#166534;
                    padding:6px 14px;
                    border-radius:20px;
                    font-size:13px;
                    font-weight:600;">
                    Active
                </div>

                <div style="height:18px;"></div>

                <button style="
                    background:#16A34A;
                    color:white;
                    border:none;
                    border-radius:10px;
                    padding:10px 24px;
                    font-size:14px;
                    font-weight:600;
                    cursor:pointer;">
                    View Details
                </button>

            </div>

        </div>

        </div>
        """)

else:
    render_html("""
    <div style="
        background:white;
        border:1px dashed #D1D5DB;
        border-radius:18px;
        padding:70px;
        text-align:center;
        color:#6B7280;">

        <div style="font-size:65px;">❤️</div>

        <div style="
            font-size:24px;
            font-weight:700;
            margin-top:15px;">
            No Receivers Found
        </div>

        <div style="
            margin-top:10px;
            font-size:15px;">
            Try changing your search or filter.
        </div>

    </div>
    """)