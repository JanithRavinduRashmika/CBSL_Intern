import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="CCI Index Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Theme colors */
    :root {
        --primary: #6366F1;
        --secondary: #22C55E;
        --background: #0F172A;
        --card: #1E293B;
        --text: #F8FAFC;
        --accent: #38BDF8;
    }

    /* Main container */
    .main {
        background: linear-gradient(180deg, var(--background), #020617);
        color: var(--text);
    }

    /* Metric cards */
    .stMetric {
        background: linear-gradient(145deg, var(--card), #2D3B55);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideUp 0.5s ease-out;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, var(--card), #151E2F);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text);
        font-weight: 600;
        animation: fadeIn 0.5s ease-out;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #F8FAFC; font-size: 24px;">CCI Index Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.markdown("### 📅 Time Period")
time_period = st.sidebar.selectbox(
    "",
    ["6 Months", "1 Year", "3 Years", "10 Years", "Max"],
    index=0
)

st.sidebar.markdown("### 📈 Analysis Tools")
show_ma = st.sidebar.multiselect(
    "Moving Averages",
    ["4-Month MA", "1-Year MA"],
    default=["4-Month MA"]
)

# Generate sample data
def generate_sample_data():
    current_date = datetime(2025, 1, 14)
    dates = pd.date_range(end=current_date, periods=120, freq='M')

    # Create base trend with some seasonality and noise
    t = np.linspace(0, 10, len(dates))
    base_trend = 50 + 25 * np.sin(t * 2 * np.pi / 12)
    noise = np.random.normal(0, 5, len(dates))
    cci_values = base_trend + noise

    data = pd.DataFrame({
        'Date': dates,
        'CCI Index': cci_values
    })

    # Calculate moving averages
    data['4-Month MA'] = data['CCI Index'].rolling(window=4).mean()
    data['1-Year MA'] = data['CCI Index'].rolling(window=12).mean()

    return data

# Generate and filter data
data = generate_sample_data()
period_months = {
    "6 Months": 6,
    "1 Year": 12,
    "3 Years": 36,
    "10 Years": 120,
    "Max": len(data)
}
filtered_data = data.tail(period_months[time_period])

# Generate projection data
def generate_projection(data, months=12):
    last_value = data['CCI Index'].iloc[-1]
    last_date = data['Date'].iloc[-1]
    dates = pd.date_range(start=last_date, periods=months + 1, freq='M')[1:]

    # Create smooth projection with uncertainty cone
    t = np.linspace(0, 1, months)
    projected = last_value + 10 * np.sin(t * 2 * np.pi) + 5 * t
    uncertainty = t * 10

    return pd.DataFrame({
        'Date': dates,
        'Projected': projected,
        'Upper': projected + uncertainty,
        'Lower': projected - uncertainty
    })

projection_data = generate_projection(filtered_data)

# Create main chart
def create_chart(data, projection_data, show_ma):
    fig = go.Figure()

    # Main CCI line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['CCI Index'],
        name='CCI Index',
        line=dict(color='#6366F1', width=2),
        fill='tonexty',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))

    # Moving averages
    if "4-Month MA" in show_ma:
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['4-Month MA'],
            name='4-Month MA',
            line=dict(color='#22C55E', width=1.5)
        ))

    if "1-Year MA" in show_ma:
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['1-Year MA'],
            name='1-Year MA',
            line=dict(color='#38BDF8', width=1.5)
        ))

    # Projection
    fig.add_trace(go.Scatter(
        x=[data['Date'].iloc[-1]] + projection_data['Date'].tolist(),
        y=[data['CCI Index'].iloc[-1]] + projection_data['Projected'].tolist(),
        name='Projection',
        line=dict(color='#F43F5E', width=2)
    ))

    # Projection cone
    fig.add_trace(go.Scatter(
        x=projection_data['Date'].tolist() + projection_data['Date'].tolist()[::-1],
        y=projection_data['Upper'].tolist() + projection_data['Lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(244, 63, 94, 0.1)',
        line=dict(width=0),
        name='Projection Range'
    ))

    # Layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        height=600,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        yaxis=dict(
            title='CCI Value',
            range=[0, 100],
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)',
            rangeslider=dict(visible=True)
        ),
        hovermode='x unified'
    )

    return fig

# Create and display chart
fig = create_chart(filtered_data, projection_data, show_ma)
st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'scrollZoom': True,
    'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
})

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_value = filtered_data['CCI Index'].iloc[-1]
    st.metric(
        "Current Value",
        f"{current_value:.2f}",
        delta=f"{(current_value - filtered_data['CCI Index'].iloc[-2]):.2f}"
    )

with col2:
    daily_change = (filtered_data['CCI Index'].iloc[-1] - filtered_data['CCI Index'].iloc[-2])
    daily_pct = (daily_change / filtered_data['CCI Index'].iloc[-2] * 100)
    st.metric(
        "Monthly Change",
        f"{daily_change:.2f}",
        delta=f"{daily_pct:.1f}%"
    )

with col3:
    volatility = filtered_data['CCI Index'].rolling(window=4).std().iloc[-1]
    st.metric(
        "4-Month Volatility",
        f"{volatility:.2f}"
    )

with col4:
    if not projection_data.empty:
        proj_value = projection_data['Projected'].iloc[-1]
        proj_change = proj_value - current_value
        st.metric(
            "12-Month Projection",
            f"{proj_value:.2f}",
            delta=f"{proj_change:.2f}"
        )

# Footer
st.markdown("""
    <div style='position: fixed; bottom: 20px; right: 20px; padding: 10px; 
    background: rgba(30, 41, 59, 0.8); border-radius: 8px; font-size: 12px;'>
        Last updated: {}
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
