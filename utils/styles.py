CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');

/* ============================================
   FLAT DESIGN COLOR PALETTE
   ============================================ */
:root {
    --primary-dark: #0F2E24;
    --primary: #1B4D3E;
    --accent: #22C55E;
    --background: #F7F8F7;
    --card: #FFFFFF;
    --border: #E5E7EB;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --text-muted: #9CA3AF;
    --muted-green: #9DBFAE;
    --muted-green-dark: #5F8672;
    --muted-green-light: #AFCBBB;
    --light-green: #7FD8A6;
    --light-green-bg: #E9F3EC;
    --dark-green-text: #3F6C57;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --info: #3B82F6;
}

/* ============================================
   GLOBAL STYLES
   ============================================ */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--background);
    color: var(--text-primary);
}

/* Hide Streamlit default elements */
.stDeployButton, #MainMenu, .stDecoration {
    visibility: hidden;
    height: 0;
}

/* Main Container */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 1400px;
    margin: 0 auto;
}

/* ============================================
   SIDEBAR - PREMIUM SAAS DESIGN
   ============================================ */
@keyframes sidebarFadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B2E22 0%, #134E3A 100%) !important;
    padding: 0 !important;
    width: 280px !important;
    max-width: 280px !important;
    min-width: 280px !important;
    border-right: none;
    border-top-right-radius: 20px !important;
    border-bottom-right-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18) !important;
    overflow: hidden !important;
}

/* Hide the default Streamlit sidebar header and collapse controls */
[data-testid="stSidebar"] > div > div:first-child,
[data-testid="stSidebar"] button[aria-label="Collapse sidebar"],
[data-testid="stSidebar"] button[aria-label="Expand sidebar"],
[data-testid="stSidebar"] button[title*="Collapse sidebar"],
[data-testid="stSidebar"] button[title*="Expand sidebar"],
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] > div > div:last-child {
    background: transparent !important;
    padding: 1.6rem 1.15rem 1.25rem 1.15rem !important;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    animation: sidebarFadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Custom Scrollbar for Sidebar */
[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 4px;
}

[data-testid="stSidebar"]::-webkit-scrollbar-track {
    background: transparent;
}

[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 2px;
}

[data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Sidebar Logo */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 2rem;
    padding: 0.5rem 0.25rem;
}

.sidebar-logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(20, 184, 166, 0.2) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.sidebar-logo-title {
    font-weight: 700;
    font-size: 14.5px;
    color: #FFFFFF;
    line-height: 1.2;
    letter-spacing: 0.2px;
}

.sidebar-logo-subtitle {
    font-weight: 500;
    font-size: 10.5px;
    color: #9DBFAE;
    margin-top: 0.1rem;
}

/* Sidebar Nav Items */
.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.85rem 1rem;
    border-radius: 14px;
    font-size: 13.5px;
    font-weight: 500;
    color: #D1FAE5 !important;
    border-left: 3px solid transparent !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer;
    margin-bottom: 0.5rem;
    text-decoration: none;
}

.sidebar-nav-item span {
    color: #D1FAE5 !important;
    transition: color 0.3s ease;
}

.sidebar-nav-item:hover {
    background: #DCFCE7 !important;
    transform: scale(1.02) !important;
    border-left: 3px solid #22C55E !important;
}

.sidebar-nav-item:hover span {
    color: #166534 !important;
}

.sidebar-nav-item.active {
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    border-left: 3px solid #22C55E !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18) !important;
}

.sidebar-nav-item.active span {
    color: #FFFFFF !important;
    font-weight: 600;
}

.sidebar-nav-item.active:hover {
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    transform: scale(1.02) !important;
}

.sidebar-nav-item.active:hover span {
    color: #FFFFFF !important;
}

.sidebar-nav-icon,
.sidebar-nav-item svg {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: #A7F3D0 !important;
    stroke: #A7F3D0 !important;
    fill: none !important;
    stroke-width: 2px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.sidebar-nav-item:hover .sidebar-nav-icon,
.sidebar-nav-item:hover svg {
    color: #16A34A !important;
    stroke: #16A34A !important;
}

.sidebar-nav-item.active .sidebar-nav-icon,
.sidebar-nav-item.active svg,
.sidebar-nav-item.active:hover .sidebar-nav-icon,
.sidebar-nav-item.active:hover svg {
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Form button navigation - style buttons to look like nav items */
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    text-align: left !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    padding: 0.85rem 1rem !important;
    margin-bottom: 0.5rem !important;
    border-radius: 14px !important;
    border-left: 3px solid transparent !important;
    text-align: left !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.85rem !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #D1FAE5 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover {
    background: #DCFCE7 !important;
    border-left: 3px solid #22C55E !important;
    transform: scale(1.02) !important;
    color: #166534 !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover span {
    color: #166534 !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:active,
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"]:active button {
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    border-left: 3px solid #22C55E !important;
    color: #FFFFFF !important;
    transform: scale(1.02) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18) !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button svg,
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button span {
    color: #A7F3D0 !important;
    stroke: #A7F3D0 !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover svg,
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover span {
    color: #16A34A !important;
    stroke: #16A34A !important;
}

[data-testid="stSidebar"] [data-testid="stFormSubmitButton"]:active button svg,
[data-testid="stSidebar"] [data-testid="stFormSubmitButton"]:active button span {
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Remove form styling in sidebar */
[data-testid="stSidebar"] [data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Sidebar Section Label */
.sidebar-section-label {
    font-size: 10.5px;
    font-weight: 600;
    color: #86EFAC !important;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin: 1.5rem 0 0.75rem 0;
    padding: 0 0.75rem;
}

/* Sidebar Bottom Card */
.sidebar-bottom-card {
    background: #14532D !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 0.75rem 0.85rem !important;
    margin-top: auto !important;
    margin-bottom: 0.5rem;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    box-sizing: border-box !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18) !important;
}

.sidebar-bottom-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #166534 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.sidebar-bottom-text-container {
    display: flex;
    flex-direction: column;
}

.sidebar-bottom-title {
    font-size: 11.5px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.25;
}

.sidebar-bottom-subtitle {
    font-size: 10px;
    font-weight: 500;
    color: #9DBFAE;
    line-height: 1.25;
}

/* ============================================
   TOP NAVBAR - FLAT DESIGN
   ============================================ */
.top-navbar {
    background: #FFFFFF;
    border-bottom: 0.5px solid var(--border);
    padding: 0.75rem 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    height: 60px;
}

.top-navbar-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.top-navbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Search Bar */
.search-bar {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    max-width: 320px;
    transition: border-color 0.2s ease;
}

.search-bar:focus-within {
    border-color: var(--text-muted);
}

.search-bar input {
    border: none;
    background: transparent;
    outline: none;
    flex: 1;
    font-size: 13px;
    color: var(--text-primary);
}

.search-bar input::placeholder {
    color: var(--text-muted);
}

.search-bar-icon {
    width: 16px;
    height: 16px;
    color: var(--text-muted);
}

.search-bar-badge {
    font-size: 11px;
    color: var(--text-muted);
    background: var(--background);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    border: 1px solid var(--border);
}

/* Notification Bell */
.notification-bell {
    position: relative;
    cursor: pointer;
    width: 20px;
    height: 20px;
    color: var(--text-muted);
}

.notification-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: var(--danger);
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 500;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* User Profile */
.user-profile {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--primary);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 500;
}

.user-info {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-size: 12.5px;
    font-weight: 500;
    color: var(--text-primary);
}

.user-role {
    font-size: 10.5px;
    color: var(--accent);
    font-weight: 400;
}

/* ============================================
   CARD STYLES - FLAT DESIGN
   ============================================ */
.card {
    background: var(--card);
    border-radius: 12px;
    padding: 1rem;
    border: 0.5px solid var(--border);
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease;
}

.card:hover {
    border-color: var(--text-muted);
}

/* ============================================
   KPI CARD STYLES - FLAT DESIGN
   ============================================ */
.kpi-card {
    background: var(--card);
    border-radius: 12px;
    padding: 1rem;
    border: 0.5px solid var(--border);
    transition: border-color 0.2s ease;
}

.kpi-card:hover {
    border-color: var(--text-muted);
}

.kpi-icon {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.75rem;
}

.kpi-icon-green {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
}

.kpi-icon-blue {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info);
}

.kpi-icon-purple {
    background: rgba(139, 92, 246, 0.1);
    color: #8B5CF6;
}

.kpi-icon-amber {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
}

.kpi-label {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 400;
    margin-bottom: 0.25rem;
}

.kpi-value {
    font-size: 24px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.kpi-trend {
    font-size: 11px;
    color: var(--success);
    font-weight: 400;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
}

/* ============================================
   BUTTON STYLES - FLAT DESIGN
   ============================================ */
.btn-primary {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    padding: 0.625rem 1rem;
    font-weight: 500;
    font-size: 12.5px;
    transition: background-color 0.2s ease;
    cursor: pointer;
}

.btn-primary:hover {
    background: var(--primary-dark) !important;
}

.btn-secondary {
    background: transparent;
    color: var(--primary) !important;
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 0.625rem 1rem;
    font-weight: 500;
    font-size: 12px;
    transition: all 0.2s ease;
    cursor: pointer;
}

.btn-secondary:hover {
    background: var(--primary);
    color: #FFFFFF !important;
}

.btn-pill {
    background: var(--primary);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    font-size: 12px;
    transition: background-color 0.2s ease;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-pill:hover {
    background: var(--primary-dark);
}

.btn-light-pill {
    background: #FFFFFF;
    color: var(--primary);
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    font-size: 12px;
    transition: background-color 0.2s ease;
    cursor: pointer;
}

.btn-light-pill:hover {
    background: var(--background);
}

/* ============================================
   STATUS BADGES - FLAT DESIGN
   ============================================ */
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.625rem;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.status-available {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-pending {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.status-expired {
    background: rgba(156, 163, 175, 0.1);
    color: var(--text-secondary);
    border: 1px solid rgba(156, 163, 175, 0.2);
}

.status-claimed {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info);
    border: 1px solid rgba(59, 130, 246, 0.2);
}

.status-completed {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-rejected {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-approved {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
    border: 1px solid rgba(34, 197, 94, 0.2);
}

/* ============================================
   WELCOME BANNER - FLAT DESIGN
   ============================================ */
.welcome-banner {
    background: var(--primary);
    border-radius: 12px;
    padding: 1rem;
    min-width: 260px;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.welcome-banner-text {
    flex: 1;
}

.welcome-banner-title {
    font-size: 13.5px;
    font-weight: 500;
    color: #FFFFFF;
    line-height: 1.4;
    margin-bottom: 0.5rem;
}

.welcome-banner-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* ============================================
   ACTIVITY ROW STYLES
   ============================================ */
.activity-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 0.5px solid var(--border);
}

.activity-row:last-child {
    border-bottom: none;
}

.activity-icon {
    width: 38px;
    height: 38px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.activity-icon-green {
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
}

.activity-icon-blue {
    background: rgba(59, 130, 246, 0.1);
    color: var(--info);
}

.activity-icon-purple {
    background: rgba(139, 92, 246, 0.1);
    color: #8B5CF6;
}

.activity-icon-amber {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
}

.activity-content {
    flex: 1;
    min-width: 0;
}

.activity-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.activity-subtitle {
    font-size: 11px;
    color: var(--text-secondary);
}

.activity-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(34, 197, 94, 0.1);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 500;
    flex-shrink: 0;
}

/* ============================================
   CTA BANNER - FLAT DESIGN
   ============================================ */
.cta-banner {
    background: var(--light-green-bg);
    border-radius: 12px;
    padding: 18px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
}

.cta-banner-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.cta-banner-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    flex-shrink: 0;
}

.cta-banner-text {
    display: flex;
    flex-direction: column;
}

.cta-banner-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--primary);
    margin-bottom: 0.25rem;
}

.cta-banner-subtitle {
    font-size: 12px;
    color: var(--dark-green-text);
}

/* ============================================
   LINK STYLES
   ============================================ */
.link {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
    font-size: 12px;
    transition: color 0.2s ease;
}

.link:hover {
    color: var(--primary);
}

/* ============================================
   HEADER STYLES
   ============================================ */
.header-title {
    font-size: 20px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.header-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 400;
    line-height: 1.4;
}

/* ============================================
   SECTION TITLE
   ============================================ */
.section-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
}

/* ============================================
   CHART CARD STYLES
   ============================================ */
.chart-card {
    background: var(--card);
    border-radius: 12px;
    padding: 1rem;
    border: 0.5px solid var(--border);
}

.chart-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.chart-dropdown {
    font-size: 12px;
    padding: 0.375rem 0.75rem;
    border: 0.5px solid var(--border);
    border-radius: 6px;
    background: var(--background);
    color: var(--text-primary);
}

/* ============================================
   DONUT CHART CENTER
   ============================================ */
.donut-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.donut-center-value {
    font-size: 24px;
    font-weight: 500;
    color: var(--text-primary);
}

.donut-center-label {
    font-size: 11px;
    color: var(--text-secondary);
}

/* ============================================
   LEGEND STYLES
   ============================================ */
.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 3px;
}

.legend-label {
    font-size: 12px;
    color: var(--text-primary);
}

.legend-value {
    font-size: 12px;
    color: var(--text-secondary);
    margin-left: auto;
}
</style>
"""

def get_custom_css():
    """Return the custom CSS string."""
    return CUSTOM_CSS
