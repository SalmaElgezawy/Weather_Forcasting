import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import pickle

# Page configuration
st.set_page_config(
    page_title="🌦️ Delhi Weather Forecast",
    page_icon=":partly_sunny:",
    layout="wide"
)
df = pd.read_csv("DailyDelhiClimateTrain.csv")
df['date'] = pd.to_datetime(df['date']) 
df.set_index(df['date'], inplace=True)
df.drop(columns=['date'], inplace=True)   

# print the last date in the original data set 
last_date = df.index[-1]
last_date = last_date.date()

# --- Load Model ---
#@st.cache_resource
def load_model(file):
    with open(file, "rb") as f:
        model = pickle.load(f)
    return model

# --- Generate Forecast ---
#@st.cache_data
def generate_forecast(_model, n_day ,steps):
    # Generate forecast using the input model
    future = _model.make_future_dataframe(periods=n_day+steps)
    forecast = _model.predict(future)

    # Create date frame
    forecast_df = forecast[['ds', 'yhat']].copy()
    forecast_df.set_index('ds', inplace=True)
    # st.write(forecast_df)
    return forecast_df.tail(steps+1)

# --- User Inputs ---
today = datetime.date.today()
max_forecast_days = 10  

with st.sidebar:
    st.header("⚙️ Forecast Parameters")
    st.write(f"Current date: {today.strftime('%Y-%m-%d')}")
    st.markdown("---")
    st.write(f'the last date in the original data set ')
    st.write( last_date)
    st.markdown("---")
    # User input for the date and number of days
    st.write('Choose The Day you Want : ')
    date_input = st.date_input("choose day", datetime.date.today())
    # User selects number of forecast days
    forecast_days = st.slider(
        "🔢 Number of forecast days",
        min_value=1,
        max_value=max_forecast_days,
        value=7
    )

n_day = (date_input - last_date).days
# Load model and generate forecast
model_wind = load_model("wind.pkl")
model_humidity = load_model("hum.pkl")
model_pressure = load_model("pressure.pkl")
model_tempreture = load_model("temp (1).pkl")

df_wind = generate_forecast(model_wind,n_day , forecast_days)
df_Humidity = generate_forecast(model_humidity,n_day ,forecast_days)
df_pressure = generate_forecast(model_pressure,n_day ,forecast_days)
df_tempreture = generate_forecast(model_tempreture, n_day ,forecast_days)
# raname columns
df_wind = df_wind[['yhat']].rename(columns={'yhat': 'Wind Speed (km/h)'})
df_Humidity = df_Humidity[['yhat']].rename(columns={'yhat': 'Humidity (%)'})
df_pressure = df_pressure[['yhat']].rename(columns={'yhat': 'Pressure (hPa)'})
df_tempreture = df_tempreture[['yhat']].rename(columns={'yhat': 'Temperature (°C)'})
# one dataframe collect all forcasts
df = pd.concat([df_tempreture, df_Humidity, df_wind, df_pressure], axis=1)
#df.columns = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (km/h)', 'Pressure (hPa)']
# st.write(df)
st.write("\n")
# --- UI Components ---
st.title('🌦️ Delhi Weather Forecast')
st.markdown(f"### Prophet Model {forecast_days}-day weather outlook")

# 1. Current Conditions Cards
st.subheader(f"🔄 Forecasted Conditions for {date_input}")
current = df.iloc[0]
cols = st.columns(4)
cols[0].metric("🌡️ Temperature", f"{current['Temperature (°C)']:.1f}°C", 
               help="Daily average temperature")
cols[1].metric("💧 Humidity", f"{current['Humidity (%)']:.1f}%", 
               "Relative humidity percentage")
cols[2].metric("🌬️ Wind", f"{current['Wind Speed (km/h)']:.1f} km/h", 
               "Wind speed at 10m height")
cols[3].metric("⏲️ Pressure", f"{current['Pressure (hPa)']:.1f} hPa", 
               "Atmospheric pressure")

st.markdown("---")
# 2. Daily Forecast Cards with Icons
st.subheader(f"📅 {forecast_days}-Days Forecast")

def get_weather_icon(temp, humidity):
    if temp > 32: return "☀️"
    elif temp > 25: return "⛅"
    elif humidity > 70: return "🌧️"
    else: return "🌤️"

# Create columns based on selected days
forecast_cols = st.columns(min(forecast_days, 7)) 

for i, (date, row) in enumerate(df.iloc[1:].iterrows()):
    with forecast_cols[i % len(forecast_cols)]:  # Wrap columns if more than 7 days
        icon = get_weather_icon(row["Temperature (°C)"], row["Humidity (%)"])
        day = date.strftime('%a')
        date_num = date.strftime('%d')
        
        st.markdown(f"""
        <div style='border-radius:10px; padding:10px; background-color:#f0f2f6; text-align:center'>
            <h4>{day}</h4>
            <h3>{date_num}</h3>
            <h2>{icon}</h2>
            <p>{row['Temperature (°C)']:.1f}°C</p>
            <p>💧 {row['Humidity (%)']:.1f}%</p>
            <p>🌬️ {row['Wind Speed (km/h)']:.1f} km/h</p>
            <p> {row['Pressure (hPa)']:.1f}hPa</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown("---")  

# 3. Interactive Temperature Gauge
st.subheader("🌡️ Temperature Trend")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=current['Temperature (°C)'],
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Forecasted Temperature"},
    delta={'reference': df['Temperature (°C)'].mean(), 'increasing': {'color': "red"}, 'decreasing': {'color': "blue"}},
    gauge={
        'axis': {'range': [min(df['Temperature (°C)'])-5, max(df['Temperature (°C)'])+5]},
        'bar': {'color': "darkorange"},
        'steps': [
            {'range': [0, 25], 'color': "lightblue"},
            {'range': [25, 35], 'color': "orange"},
            {'range': [35, 50], 'color': "red"}],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': df['Temperature (°C)'].mean()}
    }))
st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")
#4. Combined Trend Chart
st.subheader("📈 Weather Trends")
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=df.index, y=df['Temperature (°C)'],
    name='Temperature (°C)',
    line=dict(color='red', width=3),
    yaxis='y1'))

fig_trend.add_trace(go.Bar(
    x=df.index, y=df['Humidity (%)'],
    name='Humidity (%)',
    marker_color='blue',
    opacity=0.5,
    yaxis='y2'))

fig_trend.update_layout(
    yaxis=dict(title='Temperature (°C)', side='left'),
    yaxis2=dict(title='Humidity (%)', side='right', overlaying='y'),hovermode="x unified")
st.plotly_chart(fig_trend, use_container_width=True)


# Model Information
with st.expander("ℹ️ About the Forecast Model"):
    st.markdown("""
    ** **Facebook Prophet Model Details:** (Prophet) Model Details:**
    **Facebook Prophet Model Details:**
    - Univariate time series forecasting model developed by Meta (Facebook)
    - Captures trends, seasonality, and holiday effects
    - Automatically detects change points in weather pattern    
    - Trained separately for each weather variable (Temperature, Humidity, Wind Speed, Pressure)
    - Ideal for daily weather data with seasonality and trend
    """)
# additional information
st.markdown("---")
st.markdown(f"""
**Weather Dashboard Features:**
- Scientific {forecast_days}-day forecast starting from {today.strftime('%Y-%m-%d')}
- Prophet model-based predictions
- Interactive visualizations of all weather parameters
""")