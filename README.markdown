# Weather Forecasting Project

## Overview

The Delhi Weather Forecasting Project is a time-series analysis and forecasting application designed to predict daily weather conditions in Delhi, India. It forecasts key weather parameters, including temperature, humidity, wind speed, and atmospheric pressure, using the **Facebook Prophet** model. The project includes comprehensive exploratory data analysis (EDA) and a user-friendly web application deployed via **Streamlit**, enabling users to select a forecast date and view predicted weather conditions interactively.

## Dataset

The project utilizes the **Daily Climate Time Series Data** dataset from Kaggle, https://www.kaggle.com/datasets/sumanthvrao/daily-climate-time-series-data .

### Dataset Details

- **Files**:
  - `DailyDelhiClimateTrain.csv`: Training data with daily weather observations (1462 records).
  - `DailyDelhiClimateTest.csv`: Test data for model evaluation (114 records).
- **Features**:
  - `date`: Date of observation (YYYY-MM-DD).
  - `meantemp`: Mean temperature (°C).
  - `humidity`: Relative humidity (%).
  - `wind_speed`: Wind speed (km/h).
  - `meanpressure`: Atmospheric pressure (hPa).
- **Time Period**: Covers daily observations from January 1, 2013, to April 24, 2017.

## Project Structure

The project is divided into two main components:

1. **Exploratory Data Analysis and Model Training** (`project.py`):

   - **Data Preprocessing**: Converts dates to datetime, sets the date as the index, and checks for missing values and duplicates.
   - **Outlier Detection and Removal**: Identifies outliers using the IQR method for wind speed, humidity, and pressure, removing or imputing them.
   - **EDA**:
     - Visualizes time-series plots, correlation heatmaps, and boxplots using Plotly and Seaborn.
     - Performs stationarity tests (Augmented Dickey-Fuller test) to assess data stationarity.
     - Conducts seasonal decomposition to analyze trends, seasonality, and residuals.
     - Plots Autocorrelation (ACF) and Partial Autocorrelation (PACF) to identify temporal dependencies.
     - Visualizes 30-day moving averages to explore long-term trends.
   - **Model Training**: Trains separate Prophet models for each weather variable (temperature, humidity, wind speed, pressure) and evaluates performance using Mean Absolute Percentage Error (MAPE) and Root Mean Squared Error (RMSE).
   - **Model Performance** (on test data):
     - Temperature: MAPE = 11.65%, RMSE = 2.67
     - Humidity: MAPE = 19.72%, RMSE = 10.32

2. **Streamlit Web Application** (`App_2.py`):

   - **Functionality**: Loads pre-trained Prophet models (`temp (1).pkl`, `hum.pkl`, `wind.pkl`, `pressure.pkl`) and generates forecasts for user-specified dates and forecast horizons (up to 10 days).
   - **User Interface**:
     - Sidebar for selecting forecast date and number of forecast days (1–10).
     - Displays the last date in the training data (2017-01-01) and the current date.
     - Visualizations include:
       - **Current Conditions**: Metric cards for temperature, humidity, wind speed, and pressure.
       - **Daily Forecast**: Cards with weather icons (based on temperature and humidity thresholds) showing daily predictions.
       - **Temperature Gauge**: Interactive Plotly gauge showing the forecasted temperature relative to the mean.
       - **Trend Chart**: Combined Plotly chart of temperature (line) and humidity (bar) trends.
     - Includes an expander with details about the Prophet model.
   - **Features**:
     - Interactive and responsive design with a wide layout.
     - Custom weather icons for intuitive visualization (e.g., for high temperatures, for high humidity).
     - Cached model loading and forecasting for performance optimization (using commented `@st.cache_resource` and `@st.cache_data`).

## Features

- **Forecasting**: Predicts weather conditions for a user-specified date and forecast horizon (1–10 days).
- **Interactive GUI**: Streamlit-based interface with:
  - Date picker and slider for forecast customization.
  - Visualizations including metric cards, daily forecast cards, a temperature gauge, and trend charts.
- **Model**: Employs Facebook Prophet for robust time-series forecasting, capturing trends, seasonality, and changepoints.
- **Data Preprocessing**: Handles outliers, missing values, and non-stationarity through differencing and median imputation.
- **EDA**: Comprehensive analysis with time-series plots, correlation heatmaps, boxplots, seasonal decomposition, ACF/PACF plots, and moving averages.

## Model Details

- **Algorithm**: Facebook Prophet, a univariate time-series forecasting model.
- **Features**:
  - Captures trends, seasonality, and holiday effects.
  - Automatically detects changepoints in weather patterns.
  - Trained separately for temperature, humidity, wind speed, and pressure.
- **Performance**: Evaluated on test data with MAPE and RMSE metrics
- **Suitability**: Ideal for daily weather data with strong seasonal and trend components.

## Future Improvements

- Integrate more recent weather data to enhance relevance.
- Experiment with additional models or ensemble approaches for improved accuracy.
- Incorporate external factors (e.g., precipitation, cloud cover) as exogenous variables in Prophet.
- Enhance the Streamlit app with additional visualizations.
- Deploy the app to a cloud platform for public access.