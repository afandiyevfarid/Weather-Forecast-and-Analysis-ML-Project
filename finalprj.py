import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set up page configuration
st.set_page_config(
    page_title="Advanced Weather Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern CSS styling with enhanced design
st.markdown("""
    <style>
        :root {
            --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --info: #3b82f6;
        }
        
        * {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
        
        html, body, .main, .stApp {
            background: #0a0a0a !important;
            color: #e2e8f0;
        }
        
        [data-testid="stAppViewContainer"] {
            background: #0a0a0a !important;
        }
        
        [data-testid="stVerticalBlock"] {
            background: #0a0a0a !important;
        }
        
        .stApp > header {
            background: transparent !important;
        }
        
        h1 {
            background: var(--primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0 10px 20px rgba(102, 126, 234, 0.2);
        }
        
        h2 {
            color: #e0e7ff;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 2rem;
        }
        
        h3 {
            color: #c7d2fe;
            font-weight: 600;
            font-size: 1.3rem;
        }
        
        .stMetric {
            background: #0f0f0f !important;
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
            border-left-color: #f093fb;
        }
        
        .stMetricLabel {
            color: #cbd5e1;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .stMetricValue {
            color: #f1f5f9;
            font-size: 2.2rem;
            font-weight: 700;
            background: var(--primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stSelectbox, .stNumberInput, .stSlider, .stTextInput {
            color: #e2e8f0;
        }
        
        .stSelectbox > div > div, .stNumberInput > div > div {
            background: #0f0f0f !important;
            border: 1px solid #374151 !important;
            border-radius: 10px;
            color: #e2e8f0 !important;
            padding: 10px 15px;
        }
        
        .stSelectbox > div > div:hover, .stNumberInput > div > div:hover {
            border-color: #667eea !important;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.2) !important;
        }
        
        /* Selectbox text styling */
        .stSelectbox > div > div > div {
            color: #e2e8f0 !important;
        }
        
        /* Dropdown menu styling */
        [role="option"] {
            color: #e2e8f0 !important;
            background: #1a1a2e !important;
        }
        
        [role="option"]:hover {
            background: #667eea !important;
            color: #ffffff !important;
        }
        
        [role="option"][aria-selected="true"] {
            background: #667eea !important;
            color: #ffffff !important;
        }
        
        /* Selectbox input text */
        .stSelectbox input, .stNumberInput input {
            color: #e2e8f0 !important;
            background: #0f0f0f !important;
        }
        
        /* Fix selectbox dropdown container */
        .stSelectbox > div > div > div:first-child {
            color: #e2e8f0 !important;
        }
        
        ul[role="listbox"] {
            background: #1a1a2e !important;
            border: 1px solid #374151 !important;
        }
        
        ul[role="listbox"] li {
            color: #e2e8f0 !important;
        }
        
        .stButton > button {
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 12px 32px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        .stSuccess {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-left: 4px solid #10b981;
            padding: 15px 20px;
            border-radius: 10px;
            color: #6ee7b7;
            font-weight: 500;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
            border-left: 4px solid #ef4444;
            padding: 15px 20px;
            border-radius: 10px;
            color: #fca5a5;
            font-weight: 500;
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
            border-left: 4px solid #3b82f6;
            padding: 15px 20px;
            border-radius: 10px;
            color: #93c5fd;
            font-weight: 500;
        }
        
        .stDivider {
            border-color: #374151;
            border-top: 2px solid;
            background: linear-gradient(to right, transparent, #667eea, transparent);
            margin: 2rem 0;
        }
        
        .stDataFrame {
            border: 1px solid #374151;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .stDataFrame table {
            background: #0f0f0f !important;
        }
        
        .stDataFrame thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }
        
        .stDataFrame th {
            font-weight: 700;
            padding: 12px;
            color: #fff;
        }
        
        .stDataFrame td {
            color: #e2e8f0;
            padding: 10px 12px;
            border-color: #374151;
        }
        
        .stDataFrame tbody tr:hover {
            background: rgba(102, 126, 234, 0.1);
        }
        
        .sidebar .sidebar-content {
            background: #0a0a0a !important;
            border-right: 2px solid #374151 !important;
        }
        
        [data-testid="stSidebar"] {
            background: #0a0a0a !important;
        }
        
        [data-testid="stSidebar"] > div {
            background: #0a0a0a !important;
        }
        
        [data-testid="stSidebarNav"] {
            background: #0a0a0a !important;
        }
        
        [data-testid="stSidebarNav"] a {
            color: #cbd5e1 !important;
        }
        
        [data-testid="stSidebarNav"] a:hover {
            color: #667eea !important;
            background: rgba(102, 126, 234, 0.1) !important;
        }
        
        [data-testid="stSidebarNav"] {
            background: #0a0a0a !important;
        }
        
        [data-testid="stSidebarNav"] a {
            color: #cbd5e1 !important;
        }
        
        [data-testid="stSidebarNav"] a:hover {
            color: #667eea !important;
            background: rgba(102, 126, 234, 0.1) !important;
        }
        
        .stRadio > label {
            color: #e2e8f0 !important;
        }
        
        .stRadio > label > div {
            background: #1a1a2e !important;
            border-radius: 10px;
            padding: 12px 16px;
            margin: 8px 0;
            color: #e2e8f0 !important;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }
        
        .stRadio > label > div:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border-left-color: #f093fb;
        }
        
        .stRadio > label > div[data-active="true"] {
            background: var(--primary) !important;
            color: #fff !important;
            border-left-color: #f093fb;
        }
        
        /* Chart styling */
        .stPlotlyChart, .stPyplotChart {
            border-radius: 15px;
            padding: 20px;
            background: #0f0f0f !important;
            border: 1px solid #374151;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* Custom card style */
        .card {
            background: #0f0f0f !important;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #374151;
            margin: 15px 0;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        .card:hover {
            border-color: #667eea;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px;
            color: #fff;
            text-align: center;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 45px rgba(102, 126, 234, 0.4);
        }
        
        .metric-card-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 10px 0;
        }
        
        .metric-card-label {
            font-size: 1rem;
            opacity: 0.9;
            font-weight: 500;
        }
        
        /* Markdown text styling */
        p, li {
            color: #cbd5e1;
            line-height: 1.6;
        }
        
        /* Footer styling */
        .footer {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-top: 40px;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

# Directories - Use project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
sarima_dir = os.path.join(project_root, "saved_models1")
reg_dir = os.path.join(project_root, "saved_models_reg")
clasf_dir = os.path.join(project_root, "saved_models_clasf")
cluster_dir = os.path.join(project_root, "saved_models_clustering")

# Title with modern design
col_empty1, col_title, col_empty2 = st.columns([0.5, 2, 0.5])
with col_title:
    st.title("🌍 Weather Analytics")
st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 1.1rem; margin-top: -1.5rem;'>AI-Powered Weather Prediction & Analysis</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Last Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M') + "</p>", unsafe_allow_html=True)
st.markdown("")

# Sidebar navigation with modern style
with st.sidebar:
    st.markdown("<h2 style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>📊 Dashboard</h2>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "Select Module",
        ["🏠 Home", "📈 Time Series", "🌬️ Regression", "🧮 Classification", "🎯 Clustering"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("<h3 style='color: #e0e7ff;'>📊 Capabilities</h3>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 3px solid #667eea;'>
            <p style='color: #93c5fd; font-weight: 600; margin: 5px 0;'>📈 Forecasting</p>
            <p style='color: #cbd5e1; font-size: 0.85rem; margin: 5px 0;'>SARIMA 30-day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 3px solid #667eea;'>
            <p style='color: #93c5fd; font-weight: 600; margin: 5px 0;'>🤖 Regression</p>
            <p style='color: #cbd5e1; font-size: 0.85rem; margin: 5px 0;'>1300+ models</p>
        </div>
        """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 3px solid #667eea;'>
            <p style='color: #93c5fd; font-weight: 600; margin: 5px 0;'>🧮 Classification</p>
            <p style='color: #cbd5e1; font-size: 0.85rem; margin: 5px 0;'>4 targets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); 
                    padding: 15px; border-radius: 10px; border-left: 3px solid #667eea;'>
            <p style='color: #93c5fd; font-weight: 600; margin: 5px 0;'>🎯 Clustering</p>
            <p style='color: #cbd5e1; font-size: 0.85rem; margin: 5px 0;'>5 algorithms</p>
        </div>
        """, unsafe_allow_html=True)

# Home page with modern design
if page == "🏠 Home":
    st.markdown("<h2 style='text-align: center; border: none; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>Welcome to Your Weather Analytics Hub</h2>", unsafe_allow_html=True)
    
    # Stats row with gradient cards
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("📍", "Cities", "200+", col1),
        ("🤖", "Models", "5,268", col2),
        ("📊", "Features", "10+", col3),
        ("⚡", "Speed", "<2sec", col4)
    ]
    
    for emoji, label, value, col in stats:
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 2.5rem;'>{emoji}</div>
                <div class='metric-card-label'>{label}</div>
                <div class='metric-card-value'>{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Features section with tabs
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #e0e7ff; margin-top: 0;'>🚀 Key Features</h3>
            <ul style='color: #cbd5e1; line-height: 1.8;'>
                <li><b style='color: #93c5fd;'>Intelligent Forecasting</b> - Multi-step predictions with confidence intervals</li>
                <li><b style='color: #93c5fd;'>Advanced Regression</b> - 1,300+ weather prediction models</li>
                <li><b style='color: #93c5fd;'>Smart Classification</b> - Real-time weather condition detection</li>
                <li><b style='color: #93c5fd;'>Pattern Clustering</b> - Identify weather patterns globally</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class='card'>
            <h3 style='color: #e0e7ff; margin-top: 0;'>📋 How It Works</h3>
            <ol style='color: #cbd5e1; line-height: 1.8;'>
                <li><b style='color: #93c5fd;'>Select a Module</b> from the sidebar</li>
                <li><b style='color: #93c5fd;'>Choose Location</b> from 200+ cities</li>
                <li><b style='color: #93c5fd;'>Provide Input</b> or select target</li>
                <li><b style='color: #93c5fd;'>Get Results</b> instantly with visualizations</li>
                <li><b style='color: #93c5fd;'>Analyze Data</b> and make decisions</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Models overview
    st.markdown("<h3 style='color: #e0e7ff;'>🔬 Available Models</h3>", unsafe_allow_html=True)
    
    models_col1, models_col2, models_col3, models_col4 = st.columns(4)
    
    model_info = [
        ("Time Series", "187", "SARIMA", models_col1),
        ("Regression", "1,316", "Linear/Advanced", models_col2),
        ("Classification", "3,760", "Multi-class", models_col3),
        ("Clustering", "5", "KMeans/GMM", models_col4)
    ]
    
    for title, count, type_, col in model_info:
        with col:
            st.markdown(f"""
            <div class='card' style='text-align: center;'>
                <p style='color: #93c5fd; font-weight: 600; margin-bottom: 5px;'>{title}</p>
                <p style='font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 10px 0;'>{count}</p>
                <p style='color: #64748b; font-size: 0.9rem;'>{type_}</p>
            </div>
            """, unsafe_allow_html=True)

# Time Series Forecast with modern design
elif page == "📈 Time Series":
    st.markdown("<h2>📈 Temperature Forecasting</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 1.05rem;'>Advanced SARIMA-based forecasting for up to 30 days ahead with confidence intervals</p>", unsafe_allow_html=True)
    
    sarima_models = [f for f in os.listdir(sarima_dir) if f.endswith("_sarima_model.pkl")]
    cities = sorted([f.replace("_sarima_model.pkl", "") for f in sarima_models])

    if not cities:
        st.error("❌ No SARIMA models found.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_city = st.selectbox("🏙️ Select a City", cities, key="sarima_city")
        with col2:
            forecast_steps = st.slider("📅 Forecast Days", 1, 30, 7)
        st.markdown("</div>", unsafe_allow_html=True)
        
        try:
            model_path = os.path.join(sarima_dir, f"{selected_city}_sarima_model.pkl")
            with open(model_path, "rb") as f:
                model = pickle.load(f)

            forecast = model.get_forecast(steps=forecast_steps)
            forecast_mean = forecast.predicted_mean
            forecast_ci = forecast.conf_int()
            
            # Create forecast dataframe
            dates = pd.date_range(start=datetime.now(), periods=forecast_steps, freq='D')
            forecast_df = pd.DataFrame({
                "Date": dates,
                "Predicted Temp (°C)": forecast_mean.values,
                "Lower 95% CI": forecast_ci.iloc[:, 0].values,
                "Upper 95% CI": forecast_ci.iloc[:, 1].values
            })
            
            st.success(f"✅ Forecast generated for {selected_city}")
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌡️ Avg Forecast Temp", f"{forecast_mean.mean():.1f}°C")
            with col2:
                st.metric("📈 Max Forecast", f"{forecast_mean.max():.1f}°C")
            with col3:
                st.metric("📉 Min Forecast", f"{forecast_mean.min():.1f}°C")
            
            st.divider()
            st.subheader(f"Detailed Forecast - {selected_city}")
            st.dataframe(forecast_df.set_index("Date").round(2), use_container_width=True)
            
            # Visualization
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(forecast_df["Date"], forecast_mean, marker="o", linewidth=2.5, label="Forecast", color="#1f77b4", markersize=8)
            ax.fill_between(forecast_df["Date"], forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1],
                           color="skyblue", alpha=0.3, label="95% Confidence Interval")
            ax.set_title(f"{forecast_steps}-Day Temperature Forecast for {selected_city}", fontsize=14, fontweight="bold")
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Temperature (°C)", fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend(loc="best", fontsize=11)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Regression Analysis with modern design
elif page == "🌬️ Regression":
    st.markdown("<h2>🌬️ Weather Variable Prediction</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 1.05rem;'>Predict Wind Speed, Humidity, Rainfall, and UV Index with advanced regression models</p>", unsafe_allow_html=True)
    
    reg_models = [f for f in os.listdir(reg_dir) if f.endswith(".pkl")]

    # Build mapping: {city: {target: {"model": path, "features": path}}}
    reg_map = {}
    for f in reg_models:
        parts = f.replace(".pkl", "").split("_")
        if len(parts) < 3:
            continue

        if "model" in parts:
            type_ = "model"
            parts.remove("model")
        elif "features" in parts:
            type_ = "features"
            parts.remove("features")
        else:
            continue

        city = parts[0]
        target = "_".join(parts[1:])

        reg_map.setdefault(city, {}).setdefault(target, {})[type_] = f

    if not reg_map:
        st.error("❌ No regression models found.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            selected_city = st.selectbox("🏙️ Select City", sorted(reg_map.keys()), key="reg_city")
        with col2:
            available_targets = list(reg_map[selected_city].keys())
            target = st.selectbox("🎯 Target Variable", sorted(available_targets), key="reg_target")
        st.markdown("</div>", unsafe_allow_html=True)

        try:
            model_path = os.path.join(reg_dir, reg_map[selected_city][target].get("model"))
            features_path = os.path.join(reg_dir, reg_map[selected_city][target].get("features"))

            with open(model_path, "rb") as f:
                reg_model = pickle.load(f)
            with open(features_path, "rb") as f:
                feature_columns = pickle.load(f)

            st.divider()
            st.markdown(f"<h3 style='color: #e0e7ff;'>Input Parameters for {target.replace('_', ' ').title()}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            # Input section
            col1, col2 = st.columns(2)
            input_data = {}
            
            feature_list = list(feature_columns)
            for i, col in enumerate(feature_list):
                with col1 if i % 2 == 0 else col2:
                    if col in ["temperature", "dew_point", "pressure"]:
                        input_data[col] = st.number_input(f"🌡️ {col.replace('_', ' ').title()}", value=25.0, step=0.1, key=f"reg_{col}")
                    else:
                        input_data[col] = st.number_input(f"📊 {col.replace('_', ' ').title()}", value=0.0, step=0.1, key=f"reg_{col}")
            
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔮 Predict", use_container_width=True):
                input_df = pd.DataFrame([input_data])[feature_columns]
                pred = reg_model.predict(input_df)[0]
                
                st.divider()
                st.success(f"✅ Prediction Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"Predicted {target.title()}", f"{pred:.2f}", "Units")
                with col2:
                    st.info(f"**Model**: Regression for {selected_city}")
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.barh(["Prediction"], [pred], color="#1f77b4", height=0.5)
                ax.set_xlabel(target.replace('_', ' ').title(), fontsize=12)
                ax.set_title(f"Predicted {target.replace('_', ' ').title()} for {selected_city}", fontsize=14, fontweight="bold")
                ax.grid(axis='x', alpha=0.3)
                st.pyplot(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Classification with modern design
elif page == "🧮 Classification":
    st.markdown("<h2>🧮 Weather Classification</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 1.05rem;'>Classify weather conditions including cloud cover, rain, snowfall, and wind direction</p>", unsafe_allow_html=True)
    
    clasf_files = [f for f in os.listdir(clasf_dir) if f.endswith("_model.pkl")]

    # Parse classification filenames
    clasf_map = {}
    for f in clasf_files:
        parts = f[:-10].split("_")
        if len(parts) < 2:
            continue
        city = "_".join(parts[:-2]) if len(parts) > 2 else parts[0]
        target = parts[-2] + "_" + parts[-1] if len(parts) > 2 else parts[1]

        clasf_map.setdefault(city, {}).setdefault(target, {})["model"] = f

        # Add associated files
        base = f.replace("_model.pkl", "")
        for suffix in ["_scaler.pkl", "_features.pkl", "_feature_encoder.pkl", "_label_encoder.pkl"]:
            path = base + suffix
            if os.path.exists(os.path.join(clasf_dir, path)):
                key = suffix.replace(".pkl", "").replace("_", "")
                clasf_map[city][target][key] = path

    if not clasf_map:
        st.error("❌ No classification models found.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            selected_city = st.selectbox("🏙️ Select City", sorted(clasf_map.keys()), key="clasf_city")
        with col2:
            selected_target = st.selectbox("🎯 Target Variable", sorted(clasf_map[selected_city].keys()), key="clasf_target")
        st.markdown("</div>", unsafe_allow_html=True)

        try:
            files = clasf_map[selected_city][selected_target]
            model_path = os.path.join(clasf_dir, files["model"])
            scaler_path = os.path.join(clasf_dir, files.get("scaler", ""))
            features_path = os.path.join(clasf_dir, files.get("features", ""))

            with open(model_path, "rb") as f:
                clf_model = pickle.load(f)

            scaler = None
            if scaler_path and os.path.exists(scaler_path):
                with open(scaler_path, "rb") as f:
                    scaler = pickle.load(f)

            feature_columns = []
            if features_path and os.path.exists(features_path):
                with open(features_path, "rb") as f:
                    feature_columns = pickle.load(f)

            st.divider()
            st.markdown(f"<h3 style='color: #e0e7ff;'>Input Parameters for {selected_target.replace('_', ' ').title()}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            # Input section
            col1, col2 = st.columns(2)
            user_input_features = ["temperature", "humidity", "pressure", "dew_point"]
            input_features = {}
            
            for i, feat in enumerate(user_input_features):
                with col1 if i % 2 == 0 else col2:
                    input_features[feat] = st.number_input(f"🌡️ {feat.replace('_', ' ').title()}", value=25.0, step=0.1, key=f"clasf_{feat}")
            
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔮 Classify", use_container_width=True):
                # Build input dataframe
                input_df = pd.DataFrame([{col: input_features.get(col, 0) for col in feature_columns}])
                
                # Scale input
                if scaler:
                    input_scaled = scaler.transform(input_df)
                else:
                    input_scaled = input_df

                pred_class = clf_model.predict(input_scaled)[0]
                
                st.divider()
                st.success(f"✅ Classification Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"Predicted Class", f"**{pred_class}**", selected_target.title())
                with col2:
                    st.info(f"**Location**: {selected_city}")
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.barh(["Prediction"], [1], color="#2ecc71", height=0.5)
                ax.text(0.5, 0, str(pred_class), ha='center', va='center', fontsize=20, fontweight='bold', color='white')
                ax.set_xlim(0, 1)
                ax.set_title(f"Predicted {selected_target.replace('_', ' ').title()}", fontsize=14, fontweight="bold")
                ax.axis('off')
                st.pyplot(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Clustering with modern design
elif page == "🎯 Clustering":
    st.markdown("<h2>🎯 Weather Pattern Clustering</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 1.05rem;'>Discover and analyze weather patterns using advanced clustering algorithms</p>", unsafe_allow_html=True)
    
    cluster_files = [f for f in os.listdir(cluster_dir) if f.endswith(".pkl")]
    
    if not cluster_files:
        st.error("❌ No clustering models found.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            selected_model = st.selectbox("🤖 Clustering Algorithm", 
                                         sorted(set([f.split("_")[0] for f in cluster_files])))
        
        # Find matching files
        matching_files = [f for f in cluster_files if f.startswith(selected_model)]
        
        with col2:
            selected_file = st.selectbox("📦 Model Variant", matching_files)
        st.markdown("</div>", unsafe_allow_html=True)

        try:
            model_path = os.path.join(cluster_dir, selected_file)
            with open(model_path, "rb") as f:
                cluster_model = pickle.load(f)

            st.divider()
            st.subheader(f"Model: {selected_model.upper()}")
            
            # Display model info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if hasattr(cluster_model, 'n_clusters'):
                    st.metric("📍 Number of Clusters", cluster_model.n_clusters)
            
            with col2:
                if hasattr(cluster_model, 'inertia_'):
                    st.metric("📊 Inertia", f"{cluster_model.inertia_:.2f}")
            
            with col3:
                st.metric("✅ Model Type", selected_model.upper())
            
            # Display labels if available
            if hasattr(cluster_model, 'labels_'):
                st.divider()
                st.subheader("Cluster Distribution")
                unique_labels, counts = np.unique(cluster_model.labels_, return_counts=True)
                cluster_dist = pd.DataFrame({
                    'Cluster': unique_labels,
                    'Count': counts
                })
                st.dataframe(cluster_dist, use_container_width=True)
                
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 5))
                colors = plt.cm.viridis(np.linspace(0, 1, len(unique_labels)))
                ax.bar(unique_labels, counts, color=colors, edgecolor='black', linewidth=1.5)
                ax.set_xlabel('Cluster', fontsize=12)
                ax.set_ylabel('Number of Samples', fontsize=12)
                ax.set_title(f'Cluster Distribution - {selected_model.upper()}', fontsize=14, fontweight="bold")
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("ℹ️ This model does not have cluster labels available")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer with modern design
st.divider()
st.markdown("""
    <div class='footer'>
        <h3 style='color: #fff; margin-top: 0;'>🌍 Weather Analytics Dashboard</h3>
        <p style='color: rgba(255,255,255,0.9); margin: 10px 0;'>Powered by Advanced Machine Learning | 5,268 Models | 200+ Cities</p>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 0;'>© 2026 Data Science Academy | AI-Powered Weather Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

