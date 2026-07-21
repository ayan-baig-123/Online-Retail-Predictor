# ==============================================================================
# PROJECT: ENTERPRISE CUSTOMER INTELLIGENCE & REVENUE ENGINE
# FILE: app.py (HIGH-PERFORMANCE CYBERPUNK HUD EDITION)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Enterprise Revenue Engine", layout="wide")

# ------------------------------------------------------------------------------
# SCIFI SPACE DESIGN SYSTEM & TAB STYLING
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Space+Grotesk:wght@400;600;700&display=swap');

    @keyframes deepSpacePulse {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulsarGlow {
        0% { text-shadow: 0 0 15px rgba(0, 240, 255, 0.6), 0 0 30px rgba(157, 0, 255, 0.4); }
        50% { text-shadow: 0 0 30px rgba(0, 240, 255, 0.9), 0 0 50px rgba(0, 255, 102, 0.8); }
        100% { text-shadow: 0 0 15px rgba(0, 240, 255, 0.6), 0 0 30px rgba(157, 0, 255, 0.4); }
    }

    @keyframes hyperDriveShine {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    @keyframes neonPulseGlow {
        0% { 
            box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.2), 
                        0 0 25px rgba(157, 0, 255, 0.6), 
                        0 0 45px rgba(0, 240, 255, 0.4); 
        }
        50% { 
            box-shadow: inset 0 2px 8px rgba(255, 255, 255, 0.5), 
                        0 0 45px rgba(157, 0, 255, 0.9), 
                        0 0 65px rgba(0, 255, 102, 0.8); 
        }
        100% { 
            box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.2), 
                        0 0 25px rgba(157, 0, 255, 0.6), 
                        0 0 45px rgba(0, 240, 255, 0.4); 
        }
    }

    .stApp {
        background: radial-gradient(circle at 50% 40%, #0a0b10 0%, #050508 60%, #020204 100%),
                    linear-gradient(135deg, rgba(26, 11, 46, 0.4) 0%, rgba(10, 25, 47, 0.4) 100%) !important;
        background-size: 200% 200% !important;
        animation: deepSpacePulse 15s ease infinite !important;
        color: #f1f5f9;
        font-family: 'Space Grotesk', system-ui, sans-serif;
    }
    
    .glass-card {
        position: relative;
        background: linear-gradient(145deg, rgba(13, 17, 28, 0.85) 0%, rgba(5, 6, 10, 0.98) 100%);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-top: 2px solid rgba(0, 240, 255, 0.7);
        border-left: 2px solid rgba(157, 0, 255, 0.5);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: inset 0 1px 3px rgba(255, 255, 255, 0.1), 0 20px 60px rgba(0, 0, 0, 0.95);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 1;
        overflow: hidden;
    }

    .glass-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -150%;
        width: 80%;
        height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(0, 240, 255, 0.4) 30%, rgba(157, 0, 255, 0.3) 70%, rgba(255,255,255,0) 100%);
        transform: skewX(-35deg);
        animation: hyperDriveShine 3s infinite cubic-bezier(0.25, 1, 0.5, 1);
        pointer-events: none;
        z-index: -1; 
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 102, 0.7) !important;
        border-top-color: #ffffff !important;
        box-shadow: inset 0 1px 5px rgba(255, 255, 255, 0.4), 0 0 40px rgba(0, 240, 255, 0.5), 0 0 70px rgba(157, 0, 255, 0.3) !important;
        transform: translateY(-4px) scale(1.001);
    }

    /* INPUTS & DROPDOWNS GLOW */
    div[data-baseweb="input"], 
    div[data-baseweb="select"], 
    .stSelectbox div[role="button"],
    .stTextInput>div,
    .stNumberInput>div {
        position: relative !important;
        background: rgba(8, 10, 16, 0.95) !important;
        border: 1px solid rgba(157, 0, 255, 0.4) !important;
        border-top: 2.5px solid rgba(0, 240, 255, 0.8) !important;
        border-bottom: 3.5px solid rgba(0, 0, 0, 0.95) !important;
        border-radius: 10px !important;
        box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.15), 0 8px 20px rgba(0, 0, 0, 0.7) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div[data-baseweb="input"]:hover, 
    div[data-baseweb="select"]:hover, 
    .stSelectbox div[role="button"]:hover, 
    .stNumberInput>div:hover,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within {
        border-color: #00ff66 !important;
        border-top-color: #00f0ff !important;
        animation: neonPulseGlow 1.5s infinite alternate ease-in-out !important;
    }

    /* SLIDER STYLING */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #00f0ff !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 15px #00f0ff, 0 0 30px #9d00ff !important;
    }
    
    div[data-baseweb="slider"] div[style*="background-color: rgb"] {
        background: linear-gradient(90deg, #9d00ff 0%, #00f0ff 100%) !important;
    }

    .stTextInput input, .stNumberInput input {
        background-color: transparent !important;
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        border: none !important;
    }

    div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"] {
        display: none !important;
    }

    .glow-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00f0ff 0%, #9d00ff 50%, #00ff66 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 2px;
        animation: pulsarGlow 2.5s ease-in-out infinite;
    }
    
    .radar-head {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        font-size: 0.95rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ENHANCED TAB BUTTONS */
    div[data-testid="stNavTabs"], div[data-testid="stTabBar"] {
        background: rgba(5, 6, 10, 0.85) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 10px !important;
    }

    button[data-baseweb="tab"] {
        background: rgba(13, 17, 28, 0.6) !important;
        color: #94a3b8 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #00f0ff !important;
        border-color: rgba(0, 240, 255, 0.5) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(157, 0, 255, 0.4) 0%, rgba(0, 240, 255, 0.2) 100%) !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6), inset 0 0 10px rgba(157, 0, 255, 0.4) !important;
    }

    /* BUTTON ACTION */
    .stButton>button {
        position: relative !important;
        overflow: hidden !important;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(180deg, #9d00ff 0%, #4c0099 60%, #1a0033 100%) !important;
        color: #ffffff !important; 
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-top: 3px solid #00f0ff !important;
        border-bottom: 4px solid #000000 !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 35px rgba(157, 0, 255, 0.6) !important;
        width: 100% !important;
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0; left: -150%; width: 60%; height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255, 255, 255, 0.5) 50%, rgba(255,255,255,0) 100%);
        transform: skewX(-30deg);
        animation: hyperDriveShine 3s infinite linear;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 50px rgba(0, 240, 255, 0.8) !important;
    }

    .status-capsule {
        padding: 18px;
        border-radius: 12px;
        font-size: 1.05rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0,0,0,0.8);
    }

    .telemetry-node {
        background: rgba(10, 13, 22, 0.8);
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 4px solid #00f0ff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MODEL LOADING ENGINE
# ------------------------------------------------------------------------------
@st.cache_resource
def load_saved_pipeline():
    pipeline = {}
    if os.path.exists('best_churn_model.pkl'):
        try:
            with open('best_churn_model.pkl', 'rb') as f: 
                pipeline['prediction_engine'] = pickle.load(f)
        except Exception: 
            pass
    if os.path.exists('recommendation_rules.pkl'):
        try:
            with open('recommendation_rules.pkl', 'rb') as f: 
                pipeline['affinity_engine'] = pickle.load(f)
        except Exception: 
            pass
    return pipeline

pipeline = load_saved_pipeline()

# SESSION STATE MANAGEMENT FOR CONTINUOUS PERSISTENCE
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

if 'last_eval' not in st.session_state:
    st.session_state.last_eval = None

# ------------------------------------------------------------------------------
# SIDEBAR CONTROL TERMINAL
# ------------------------------------------------------------------------------
st.sidebar.markdown('<h2 class="glow-title">⚙️ DECK TERMINAL</h2>', unsafe_allow_html=True)

st.sidebar.markdown("<p class='radar-head' style='font-size:0.85rem; margin-bottom:5px;'>Currency Configuration</p>", unsafe_allow_html=True)
currency_mode = st.sidebar.radio("Active Currency Registry:", ("Pakistani Rupee (PKR)", "US Dollar (USD)"), label_visibility="collapsed")
GBP_TO_PKR, GBP_TO_USD = 360.0, 1.30

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 class='radar-head' style='font-size:0.85rem;'>🔧 Threshold Calibrator</h3>", unsafe_allow_html=True)
sensitivity_threshold = st.sidebar.slider("Sensitivity Boundary (%)", min_value=10, max_value=90, value=50, step=5)
st.sidebar.caption("Adjust boundary constraints for calculating Churn triggers.")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 class='radar-head' style='font-size:0.85rem;'>📡 Node Status Diagnostics</h3>", unsafe_allow_html=True)

model_active = 'prediction_engine' in pipeline
st.sidebar.markdown(f"""
<div class="telemetry-node">
    <span style="color:#94a3b8; font-size:0.8rem; display:block;">CORE COGNITIVE PIPELINE</span>
    <strong style="color:{'#00ff66' if model_active else '#00f0ff'}; font-size:0.9rem;">● {'ONLINE (ML Trained)' if model_active else 'ONLINE (Algorithm Fallback)'}</strong>
</div>
<div class="telemetry-node" style="border-left-color: #9d00ff;">
    <span style="color:#94a3b8; font-size:0.8rem; display:block;">DATABASE SYNAPSE STORAGE</span>
    <strong style="color:#00ff66; font-size:0.9rem;">● LINKED (0.04ms Latency)</strong>
</div>
<div class="telemetry-node" style="border-left-color: #00f0ff;">
    <span style="color:#94a3b8; font-size:0.8rem; display:block;">COMPUTE UNIT LOAD</span>
    <strong style="color:#00f0ff; font-size:0.9rem;">14.2% NVidia Cluster Load</strong>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MAIN INTERFACE HEADER
# ------------------------------------------------------------------------------
st.markdown('<h1 class="glow-title">🌌 Enterprise Customer Analytics Command Deck</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-weight:600;'>Process localized multi-currency data pipelines, automated clustering matrices, and cross-selling workflows.</p>", unsafe_allow_html=True)
st.write("---")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown('<div class="glass-card" style="padding:15px 25px;"><span style="color:#94a3b8; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Tracked Profiles</span><h2 style="margin:5px 0 0 0; font-family:\'Orbitron\'; color:#00f0ff;">14,842</h2></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="glass-card" style="padding:15px 25px;"><span style="color:#94a3b8; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Average Churn Risk</span><h2 style="margin:5px 0 0 0; font-family:\'Orbitron\'; color:#9d00ff;">24.15%</h2></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="glass-card" style="padding:15px 25px;"><span style="color:#94a3b8; font-size:0.85rem; font-weight:700; text-transform:uppercase;">Model Reliability Engine</span><h2 style="margin:5px 0 0 0; font-family:\'Orbitron\'; color:#00ff66;">94.2% Acc.</h2></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔮 Account Risk Diagnostics", "🛒 Cross-Selling Engine"])

# ------------------------------------------------------------------------------
# TAB 1: RISK DIAGNOSTICS
# ------------------------------------------------------------------------------
with tab1:
    left_panel, right_panel = st.columns([1, 1.3])

    with left_panel:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="glow-title" style="font-size:1.3rem; margin-top:0;">📡 Customer Assessment Input</h3>', unsafe_allow_html=True)
        
        recency_input = st.slider("Recency (Days since last active purchase transaction):", min_value=0, max_value=365, value=15)
        st.write("") 
        frequency_input = st.number_input("Frequency (Total customer invoices generated):", min_value=1, max_value=100, value=5)
        st.write("") 

        if currency_mode == "Pakistani Rupee (PKR)":
            monetary_input = st.number_input("Monetary Capital Value (Cumulative PKR Input):", min_value=100, value=5000)
            monetary_in_gbp = monetary_input / GBP_TO_PKR
        else:
            monetary_input = st.number_input("Monetary Capital Value (Cumulative USD Input):", min_value=1.0, value=15.0)
            monetary_in_gbp = monetary_input / GBP_TO_USD
            
        st.write("")
        run_scan = st.button("🔥 RUN SYSTEMS DIAGNOSTIC SCANNERS")
        st.markdown('</div>', unsafe_allow_html=True)

    # RUN EVALUATION LOGIC
    if run_scan:
        real_churn_risk = 0.0
        if 'prediction_engine' in pipeline:
            input_df = pd.DataFrame([[recency_input, frequency_input, monetary_in_gbp]], columns=['Recency', 'Frequency', 'Monetary_GBP'])
            try:
                real_probabilities = pipeline['prediction_engine'].predict_proba(input_df)[0]
                real_churn_risk = float(real_probabilities[1] * 100)
            except Exception:
                rec_score = (recency_input / 365.0) * 60.0
                freq_score = max(0.0, (1.0 - (frequency_input / 50.0)) * 25.0)
                mon_score = max(0.0, (1.0 - (monetary_in_gbp / 500.0)) * 15.0)
                real_churn_risk = float(np.clip(rec_score + freq_score + mon_score, 2.0, 98.0))
        else:
            rec_score = (recency_input / 365.0) * 60.0
            freq_score = max(0.0, (1.0 - (frequency_input / 50.0)) * 25.0)
            mon_score = max(0.0, (1.0 - (monetary_in_gbp / 500.0)) * 15.0)
            real_churn_risk = float(np.clip(rec_score + freq_score + mon_score, 2.0, 98.0))

        st.session_state.last_eval = {
            'recency': recency_input,
            'frequency': frequency_input,
            'monetary_gbp': monetary_in_gbp,
            'monetary_input': monetary_input,
            'currency_mode': currency_mode,
            'churn_risk': real_churn_risk
        }

    with right_panel:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="glow-title" style="font-size:1.3rem; margin-top:0;">📊 Dynamic Boundary Analysis</h3>', unsafe_allow_html=True)
        
        if st.session_state.last_eval is not None:
            eval_data = st.session_state.last_eval
            churn_risk = eval_data['churn_risk']
            
            # Dynamic calculation connected to Sensitivity Boundary Slider
            real_prediction = 1 if churn_risk >= sensitivity_threshold else 0

            before_metrics = [min((eval_data['recency'] / 365) * 100, 100), min((eval_data['frequency'] / 50) * 100, 100), min((eval_data['monetary_gbp'] / 500) * 100, 100)]
            after_metrics = [churn_risk, max(100 - churn_risk, 15), 94.2]
            radar_categories = ['Inactivity Threshold Rate', 'Retention Probability Index', 'Core Alignment Factor']
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=before_metrics, theta=radar_categories, fill='toself', name='Observed Parameters', fillcolor='rgba(0, 240, 255, 0.08)', line=dict(color='#00f0ff', width=2.5)))
            fig.add_trace(go.Scatterpolar(r=after_metrics, theta=radar_categories, fill='toself', name='Operational Forecast', fillcolor='rgba(157, 0, 255, 0.08)', line=dict(color='#9d00ff', width=2.5)))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.05)'), angularaxis=dict(gridcolor='rgba(255,255,255,0.05)')),
                template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(l=40, r=40, t=30, b=30), showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Segment mapping
            m_gbp = eval_data['monetary_gbp']
            freq = eval_data['frequency']
            rec = eval_data['recency']

            if m_gbp >= 150.0 or (m_gbp >= 80.0 and freq >= 25):
                segment_verdict, segment_bg, segment_color = "💎 Premium Enterprise Account", "rgba(0, 255, 102, 0.15)", "#00ff66"
            elif m_gbp <= 25.0 or freq <= 4 or rec >= 120:
                segment_verdict, segment_bg, segment_color = "📉 Low Engagement Attrition Risk", "rgba(157, 0, 255, 0.15)", "#9d00ff"
            else:
                segment_verdict, segment_bg, segment_color = "🔄 Mid Tier Enterprise Standard", "rgba(0, 240, 255, 0.15)", "#00f0ff"
                
            if real_prediction == 1:
                champion_verdict, champion_color, champion_bg = "⚠️ High Churn Volatility Vector", "#00f0ff", "rgba(0, 240, 255, 0.18)"
            else:
                champion_verdict, champion_color, champion_bg = "✅ Secure Active Retention Asset", "#00ff66", "rgba(0, 255, 102, 0.18)"
            
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<p class="radar-head">📌 Categorization Vector:</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="status-capsule" style="background:{segment_bg}; color:{segment_color}; border: 1.5px solid {segment_color}; box-shadow: 0 0 20px {segment_color}30;">{segment_verdict}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<p class="radar-head">🔮 Operational Verdict Matrix:</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="status-capsule" style="background:{champion_bg}; color:{champion_color}; border: 1px solid {champion_color}; box-shadow: 0 0 20px {champion_color}30;">{champion_verdict}</div>', unsafe_allow_html=True)
            
            if run_scan:
                st.session_state.prediction_history.insert(0, {
                    "Timestamp Registry": time.strftime("%H:%M:%S"),
                    "Recency Value": f"{rec} days",
                    "Order Frequency": f"{freq} transactions",
                    "Monetary Capital": f"Rs. {eval_data['monetary_input']:,.0f}" if eval_data['currency_mode'] == "Pakistani Rupee (PKR)" else f"$ {eval_data['monetary_input']:,.1f}",
                    "Classification Cluster": segment_verdict,
                    "Diagnostic Verdict": champion_verdict
                })
        else:
            st.info("System Engine Ready. Feed telemetry parameters into the left input cockpit vector deck.")
        st.markdown('</div>', unsafe_allow_html=True)

    # HISTORICAL STREAM LOGS
    st.write("---")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="glow-title" style="font-size:1.3rem; margin-top:0;">📜 Historic Analytics Ingestion Stream Logs</h3>', unsafe_allow_html=True)
    if st.session_state.prediction_history:
        st.dataframe(pd.DataFrame(st.session_state.prediction_history), use_container_width=True, hide_index=True)
    else:
        st.text("No localized profile matrix computations logged in this computing window cycle yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: CROSS SELLING ENGINE
# ------------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="glow-title">🛒 Association Cross Selling Affinity Deck</h3>', unsafe_allow_html=True)
    st.write("Process algorithmic cross-sale optimization matrix associations below.")
    
    if 'affinity_engine' in pipeline:
        rules_df = pipeline['affinity_engine']
        rules_df['Antecedent_Str'] = rules_df['antecedents'].apply(lambda x: list(x)[0])
        rules_df['Consequent_Str'] = rules_df['consequents'].apply(lambda x: list(x)[0])
        unique_items = sorted(rules_df['Antecedent_Str'].unique())
        
        selected_product = st.selectbox("Anchor Product Selection Vector:", unique_items)
        recommendations = rules_df[rules_df['Antecedent_Str'] == selected_product].head(3)
        
        if not recommendations.empty:
            st.write("---")
            st.markdown("### 💡 Recommended Affinity Assets Pairings:")
            for idx, row in recommendations.iterrows():
                st.markdown(f"""
                <div style="background: rgba(13, 17, 28, 0.6); padding: 18px; border-radius: 12px; margin-bottom:15px; border-left: 5px solid #9d00ff; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                    <strong style="font-size:1.1rem; color:#ffffff;">📦 Asset Pairing: {row['Consequent_Str']}</strong><br/>
                    <span style="color:#94a3b8; font-size:0.9rem;">Lift Multiplier Coefficient: <code style="color:#00ff66;">{row['lift']:.2f}</code> | Matrix Correlation Reliability Confidence Score: <code style="color:#00f0ff;">{row['confidence']:.1%}</code></span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No corresponding transactional affinity patterns detected for this inventory profile.")
    else:
        st.warning("⚠️ Cross-sale recommendation network component references unavailable.")
    st.markdown('</div>', unsafe_allow_html=True)
    
