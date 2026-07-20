import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from db.database import get_food_type_distribution, get_meal_type_distribution, get_top_locations, get_claims_trend, get_claim_status_distribution
from utils.styles import get_custom_css

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<div class="animate-fade-in"><h1 class="header-title">Analytics</h1><p class="header-subtitle">View detailed analytics and insights about food wastage management.</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Time period selector
period = st.selectbox("Time Period", ["Last 30 Days", "Last 7 Days", "Last 90 Days"], key="analytics_period")

# First row - Food Type and Meal Type
st.markdown('<div class="chart-container animate-slide-up">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Food Type Distribution</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_food_type_data():
        return get_food_type_distribution()
    
    with st.spinner("Loading food type data..."):
        food_type_data = load_food_type_data()
    
    if not food_type_data.empty:
        colors = ['#1B4D3E', '#2D6B5A', '#4CAF50', '#81C784', '#A5D6A7']
        
        fig = px.pie(
            food_type_data,
            values='count',
            names='food_type',
            hole=0.4,
            color_discrete_sequence=colors[:len(food_type_data)]
        )
        fig.update_traces(
            textinfo='percent+label',
            textposition='outside',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=11)
            )
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No food type data available.")

with col2:
    st.markdown('<div class="section-title">Meal Type Distribution</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_meal_type_data():
        return get_meal_type_distribution()
    
    with st.spinner("Loading meal type data..."):
        meal_type_data = load_meal_type_data()
    
    if not meal_type_data.empty:
        colors = ['#1B4D3E', '#2D6B5A', '#4CAF50', '#81C784', '#A5D6A7']
        
        fig = px.bar(
            meal_type_data,
            x='meal_type',
            y='count',
            color='meal_type',
            color_discrete_sequence=colors[:len(meal_type_data)]
        )
        fig.update_traces(
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Count",
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No meal type data available.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Second row - Top Locations and Claims Trend
st.markdown('<div class="chart-container animate-slide-up">', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-title">Top Locations</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_top_locations():
        return get_top_locations(10)
    
    with st.spinner("Loading location data..."):
        locations_data = load_top_locations()
    
    if not locations_data.empty:
        colors = ['#1B4D3E', '#2D6B5A', '#4CAF50', '#81C784', '#A5D6A7']
        
        fig = px.bar(
            locations_data.head(10),
            x='count',
            y='location',
            orientation='h',
            color='count',
            color_continuous_scale=['#E8F5E9', '#1B4D3E']
        )
        fig.update_traces(
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig.update_layout(
            xaxis_title="Listings",
            yaxis_title=None,
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No location data available.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown('<div class="chart-container animate-slide-up">', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="section-title">Claims Trend</div>', unsafe_allow_html=True)
    
    @st.cache_data(ttl=60)
    def load_claims_trend_data():
        return get_claims_trend('month' if period == "Last 30 Days" else 'week' if period == "Last 7 Days" else 'quarter')
    
    with st.spinner("Loading claims trend data..."):
        claims_trend_data = load_claims_trend_data()
    
    if not claims_trend_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=claims_trend_data['date'],
            y=claims_trend_data['count'],
            mode='lines+markers',
            line=dict(color='#1B4D3E', width=2),
            marker=dict(color='#1B4D3E', size=6),
            fill='tozeroy',
            fillcolor='rgba(27, 77, 62, 0.2)',
            hovertemplate='<b>%{x}</b><br>Claims: %{y}<extra></extra>'
        ))
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Claims",
            hovermode='x unified',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No claims trend data available.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# Third row - Claim Status Distribution
st.markdown('<div class="section-title animate-fade-in">Claim Status Distribution</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container animate-slide-up">', unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_claim_status_data():
    return get_claim_status_distribution()

with st.spinner("Loading claim status data..."):
    claim_status_data = load_claim_status_data()

if not claim_status_data.empty:
    status_colors = {
        'Pending': '#FEF3C7',
        'Approved': '#D1FAE5',
        'Completed': '#D1FAE5',
        'Rejected': '#FEE2E2'
    }
    
    colors = [status_colors.get(status, '#E5E7EB') for status in claim_status_data['status']]
    border_colors = ['#92400E', '#065F46', '#065F46', '#991B1B']
    
    fig = px.pie(
        claim_status_data,
        values='count',
        names='status',
        hole=0.4,
        color='status',
        color_discrete_map={status: color for status, color in zip(claim_status_data['status'], colors)}
    )
    fig.update_traces(
        textinfo='percent+label',
        textposition='outside',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=11)
        )
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No claim status data available.")

st.markdown('</div>', unsafe_allow_html=True)
