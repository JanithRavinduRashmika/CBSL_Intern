import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="CCI Index Dashboard", layout="wide")

# Custom CSS for improved styling
st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
    }
    .stMetric .metric-label {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 Consumer Confidence Index (CCI) Dashboard")
st.markdown("This dashboard provides insights into the Consumer Confidence Index (CCI) trends, moving averages, and projections.")

# Generate dummy monthly CCI index data from 2012 to now
dates = pd.date_range(start="2012-01-01", end=datetime(2025, 1, 14), freq="M")
cci_values = np.random.uniform(80, 120, len(dates))
dummy_cci_data = pd.DataFrame({"Date": dates, "CCI Index": cci_values})

# Calculate moving averages
dummy_cci_data['4-Month MA'] = dummy_cci_data['CCI Index'].rolling(window=4).mean()
dummy_cci_data['1-Year MA'] = dummy_cci_data['CCI Index'].rolling(window=12).mean()

# Generate dummy projection data
last_actual_date = dummy_cci_data["Date"].iloc[-1]
future_dates = pd.date_range(start=last_actual_date, periods=7, freq="M")[1:]
projected_cci_values = np.random.uniform(80, 120, len(future_dates))
dummy_projection_data = pd.DataFrame({
    "Date": future_dates,
    "Projected CCI": projected_cci_values,
    "Lower Bound": projected_cci_values - np.random.uniform(5, 10, len(future_dates)),
    "Upper Bound": projected_cci_values + np.random.uniform(5, 10, len(future_dates))
})

# Sidebar for time period selection
st.sidebar.header("📅 Select Time Period")
time_period = st.sidebar.selectbox("Time Period", ["Max", "3 Years", "1 Year", "6 Months"], index=0)

# Filter data based on selected time period
current_date = datetime(2025, 1, 14)
if time_period == "6 Months":
    start_date = current_date - timedelta(days=6*30)
elif time_period == "1 Year":
    start_date = current_date - timedelta(days=365)
elif time_period == "3 Years":
    start_date = current_date - timedelta(days=3*365)
else:
    start_date = dummy_cci_data["Date"].min()

filtered_data = dummy_cci_data[dummy_cci_data["Date"] >= start_date]

# Sidebar for moving average options
st.sidebar.header("📈 Moving Averages")
show_4month_ma = st.sidebar.checkbox("Show 4-Month Moving Average")
show_1year_ma = st.sidebar.checkbox("Show 1-Year Moving Average")

# Sidebar for projection option
show_projection = st.sidebar.checkbox("Show 6-Month Projection", value=True)

# Create a line chart for the CCI index with moving averages and projection
def plot_cci_with_moving_averages(data, projection_data, show_4month, show_1year, show_projection):
    fig = go.Figure()

    # Add shaded area under the CCI Index
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['CCI Index'],
        fill='tozeroy',
        fillcolor='rgba(0, 123, 255, 0.1)',
        line=dict(color='rgb(0, 123, 255)', width=2),
        name='CCI Index'
    ))

    if show_4month:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['4-Month MA'], mode='lines', name='4-Month MA',
                                 line=dict(color='orange', width=2)))

    if show_1year:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['1-Year MA'], mode='lines', name='1-Year MA',
                                 line=dict(color='green', width=2)))

    if show_projection:
        # Add shaded area for projection confidence interval
        fig.add_trace(go.Scatter(
            x=projection_data['Date'].tolist() + projection_data['Date'].tolist()[::-1],
            y=projection_data['Upper Bound'].tolist() + projection_data['Lower Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.1)',
            line=dict(color='rgba(255, 0, 0, 0)'),
            name='Projection Confidence Interval'
        ))
        
        fig.add_trace(go.Scatter(x=projection_data['Date'], y=projection_data['Projected CCI'], mode='lines', name='Projection',
                                 line=dict(color='red', width=2)))

    fig.update_layout(
        title='CCI Index with Moving Averages and Projection',
        xaxis_title='Date',
        yaxis_title='CCI Index',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    
    # Add range slider
    fig.update_xaxes(rangeslider_visible=True)
    
    return fig

# Generate the plot
cci_plot = plot_cci_with_moving_averages(filtered_data, dummy_projection_data, show_4month_ma, show_1year_ma, show_projection)

# Display the plot in Streamlit
st.plotly_chart(cci_plot, use_container_width=True)

# Display key metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current CCI", f"{filtered_data['CCI Index'].iloc[-1]:.2f}")
with col2:
    change = filtered_data['CCI Index'].iloc[-1] - filtered_data['CCI Index'].iloc[-2]
    st.metric("Monthly Change", f"{change:.2f}")
with col3:
    avg_cci = filtered_data['CCI Index'].mean()
    st.metric("Average CCI", f"{avg_cci:.2f}")

# Display recent data
st.subheader("📅 Recent CCI Data")
st.dataframe(filtered_data[['Date', 'CCI Index']].tail(10).sort_values('Date', ascending=False).reset_index(drop=True))

# Add some analysis
st.subheader("📖 CCI Index Analysis")
st.write("""
The Consumer Confidence Index (CCI) is an indicator that measures consumer confidence in the economy. 
It is based on the premise that if consumers are optimistic, they tend to purchase more goods and services, 
which stimulates the economy.

- A CCI above 100 indicates optimism about the economy.
- A CCI below 100 indicates pessimism about the economy.

The chart above shows the monthly CCI index for the selected time period. You can observe trends and fluctuations 
in consumer confidence over time. The moving averages help to smooth out short-term fluctuations and highlight 
longer-term trends. The projection, if selected, provides an estimate of future CCI values based on historical data.
""")

# Display projection data if selected
if show_projection:
    st.subheader("🔮 6-Month Projection")
    st.dataframe(dummy_projection_data)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and Plotly")
