import streamlit as st
import pandas as pd
from db.database import get_all_food_listings, get_all_claims, get_all_providers, get_all_receivers, get_kpi_counts
from utils.styles import get_custom_css

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="animate-fade-in"><h1 class="header-title">Reports</h1><p class="header-subtitle">Generate and export comprehensive reports.</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Report type selector
st.markdown('<div class="card animate-slide-up">', unsafe_allow_html=True)
report_type = st.selectbox(
    "Select Report Type",
    ["Food Listings Summary", "Claims Summary", "Providers Summary", "Receivers Summary", "Overall KPI Report"],
    key="report_type"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

if report_type == "Food Listings Summary":
    st.markdown('<div class="section-title animate-fade-in">Food Listings Summary</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_food_listings_report():
        return get_all_food_listings()
    
    with st.spinner("Loading food listings data..."):
        food_data = load_food_listings_report()
    
    if not food_data.empty:
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Listings", len(food_data))
        with col2:
            st.metric("Available", len(food_data[food_data['status'] == 'Available']))
        with col3:
            st.metric("Claimed", len(food_data[food_data['status'] == 'Claimed']))
        with col4:
            st.metric("Expired", len(food_data[food_data['status'] == 'Expired']))
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display table
        display_columns = ['food_name', 'food_type', 'meal_type', 'quantity', 'unit', 'location', 'status', 'created_at']
        display_data = food_data[display_columns].copy()
        display_data.columns = ['Food Name', 'Food Type', 'Meal Type', 'Quantity', 'Unit', 'Location', 'Status', 'Created At']
        
        st.dataframe(display_data, width='stretch', height=400)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="food_listings_report.csv",
                mime="text/csv"
            )
    else:
        st.info("No food listings data available.")

elif report_type == "Claims Summary":
    st.markdown('<div class="section-title animate-fade-in">Claims Summary</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_claims_report():
        return get_all_claims()
    
    with st.spinner("Loading claims data..."):
        claims_data = load_claims_report()
    
    if not claims_data.empty:
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Claims", len(claims_data))
        with col2:
            st.metric("Pending", len(claims_data[claims_data['status'] == 'Pending']))
        with col3:
            st.metric("Approved", len(claims_data[claims_data['status'] == 'Approved']))
        with col4:
            st.metric("Completed", len(claims_data[claims_data['status'] == 'Completed']))
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display table
        display_columns = ['receiver_name', 'food_name', 'quantity_claimed', 'status', 'claimed_at']
        display_data = claims_data[display_columns].copy()
        display_data.columns = ['Receiver', 'Food Item', 'Quantity Claimed', 'Status', 'Claimed At']
        
        st.dataframe(display_data, width='stretch', height=400)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="claims_report.csv",
                mime="text/csv"
            )
    else:
        st.info("No claims data available.")

elif report_type == "Providers Summary":
    st.markdown('<div class="section-title animate-fade-in">Providers Summary</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_providers_report():
        return get_all_providers()
    
    with st.spinner("Loading providers data..."):
        providers_data = load_providers_report()
    
    if not providers_data.empty:
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Providers", len(providers_data))
        with col2:
            st.metric("Verified", len(providers_data[providers_data['verified'] == 1]))
        with col3:
            st.metric("Unverified", len(providers_data[providers_data['verified'] == 0]))
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display table
        display_columns = ['name', 'type', 'city', 'contact', 'verified']
        display_data = providers_data[display_columns].copy()
        display_data.columns = ['Name', 'Type', 'City', 'Contact', 'Verified']
        display_data['Verified'] = display_data['Verified'].map({1: 'Yes', 0: 'No'})
        
        st.dataframe(display_data, width='stretch', height=400)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="providers_report.csv",
                mime="text/csv"
            )
    else:
        st.info("No providers data available.")

elif report_type == "Receivers Summary":
    st.markdown('<div class="section-title animate-fade-in">Receivers Summary</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_receivers_report():
        return get_all_receivers()
    
    with st.spinner("Loading receivers data..."):
        receivers_data = load_receivers_report()
    
    if not receivers_data.empty:
        # Summary stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Receivers", len(receivers_data))
        with col2:
            st.metric("Cities Covered", receivers_data['city'].nunique())
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Display table
        display_columns = ['name', 'type', 'city', 'contact']
        display_data = receivers_data[display_columns].copy()
        display_data.columns = ['Name', 'Type', 'City', 'Contact']
        
        st.dataframe(display_data, width='stretch', height=400)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="receivers_report.csv",
                mime="text/csv"
            )
    else:
        st.info("No receivers data available.")

elif report_type == "Overall KPI Report":
    st.markdown('<div class="section-title animate-fade-in">Overall KPI Report</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_kpi_report():
        return get_kpi_counts()
    
    with st.spinner("Loading KPI data..."):
        kpi_data = load_kpi_report()
    
    # Create summary dataframe
    summary_data = pd.DataFrame({
        'Metric': ['Total Food Listings', 'Total Providers', 'Total Receivers', 'Total Claims'],
        'Count': [kpi_data['total_listings'], kpi_data['total_providers'], kpi_data['total_receivers'], kpi_data['total_claims']]
    })
    
    st.dataframe(summary_data, use_container_width=True, height=200)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export buttons
    csv = summary_data.to_csv(index=False)
    st.download_button(
        label="Download KPI Report CSV",
        data=csv,
        file_name="kpi_report.csv",
        mime="text/csv"
    )
