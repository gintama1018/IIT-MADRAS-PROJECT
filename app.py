
import streamlit as st
import pandas as pd
import altair as alt
import sys
import os
import time
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.pipeline import RiskClassificationPipeline

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DebtRisk AI | Enterprise Edition",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS (The "Smooth" Factor)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Font & Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Smooth page transitions */
    .main .block-container {
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Cards */
    .stCard {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    /* Metrics - Responsive with colored backgrounds */
    div[data-testid="stMetricValue"] {
        font-size: clamp(1.5rem, 4vw, 2rem);
        font-weight: 700;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 16px;
        border: none;
        transition: all 0.3s ease;
        color: white !important;
    }
    div[data-testid="stMetric"] > div {
        color: white !important;
    }
    div[data-testid="stMetric"] label {
        color: rgba(255,255,255,0.9) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Risk Badges */
    .risk-badge {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high { background: linear-gradient(135deg, #ff4b4b 0%, #d32f2f 100%); }
    .risk-medium { background: linear-gradient(135deg, #ffa726 0%, #f57c00 100%); }
    .risk-low { background: linear-gradient(135deg, #66bb6a 0%, #388e3c 100%); }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
    }
    
    /* Responsive Buttons - All buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        font-size: clamp(0.85rem, 2vw, 1rem);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Primary button special styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {
        background: #f0f2f6;
        color: #333;
        border: 2px solid #e0e0e0;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #e8eaed;
        border-color: #667eea;
    }
    
    /* Modern Compact Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 6px 10px;
        border-radius: 50px;
        width: fit-content;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 22px;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 50px;
        background-color: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        transform: scale(1.02);
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: white;
        background-color: rgba(255, 255, 255, 0.15);
    }
    .stTabs [aria-selected="true"]:hover {
        background: white;
        color: #667eea !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Responsive containers */
    [data-testid="stVerticalBlock"] > div {
        transition: all 0.2s ease;
    }
    
    /* Better selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .stSelectbox > div > div:hover {
        border-color: #667eea;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Container with border improvements */
    [data-testid="stExpander"], div[data-testid="stContainer"] {
        transition: all 0.3s ease;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Dataframe improvements */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
    }
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
    }
    
    /* Status widget styling */
    [data-testid="stStatusWidget"] {
        border-radius: 12px;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 0 12px;
            font-size: 0.8rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE & INITIALIZATION
# -----------------------------------------------------------------------------
if 'pipeline' not in st.session_state:
    api_key = os.environ.get('GEMINI_API_KEY', '')
    use_demo = not api_key
    st.session_state.pipeline = RiskClassificationPipeline(
        gemini_api_key=api_key,
        use_demo=use_demo
    )

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("DebtRisk AI")
    st.caption("Enterprise Recovery Intelligence")
    
    st.divider()
    
    st.subheader("⚙️ System Status")
    if st.session_state.pipeline.demo_mode:
        st.warning("⚠️ DEMO MODE ACTIVE")
        st.caption("Using rule-based logic. Add API Key for full AI reasoning.")
        
        api_key_input = st.text_input("Enter Gemini API Key", type="password")
        if st.button("Activate AI Engine"):
            if api_key_input:
                st.session_state.pipeline = RiskClassificationPipeline(gemini_api_key=api_key_input)
                st.rerun()
    else:
        st.success("✅ AI ENGINE ONLINE")
        st.caption("Powered by Gemini 1.5 Flash")
        if st.button("Switch to Demo Mode"):
            st.session_state.pipeline = RiskClassificationPipeline(use_demo=True)
            st.rerun()

    st.divider()
    st.info("💡 **Tip for Judges:** Check the 'Under the Hood' section in Analysis to see how we transform raw data into AI context.")

# -----------------------------------------------------------------------------
# MAIN CONTENT
# -----------------------------------------------------------------------------

# Tabs for navigation
tab_dashboard, tab_analysis, tab_audit = st.tabs(["📊 Executive Dashboard", "🔍 Case Analysis", "📜 Audit Log"])

# --- TAB 1: DASHBOARD ---
with tab_dashboard:
    st.markdown("### 📈 Portfolio Overview")
    
    # Get stats
    stats = st.session_state.pipeline.get_statistics()
    cases = st.session_state.pipeline.get_all_cases()
    
    # Calculate KPIs from case data
    total_cases = len(cases)
    total_outstanding = sum(c['amount'] for c in cases)
    
    # SLA Compliance: cases where days_overdue < sla_days
    sla_compliant = sum(1 for c in cases if c.get('days_overdue', 0) < c.get('sla_days', 30))
    sla_compliance_rate = round((sla_compliant / total_cases) * 100, 1) if total_cases > 0 else 0
    
    # Priority breakdown
    priority_counts = {}
    for c in cases:
        p = c.get('priority', 'Normal')
        priority_counts[p] = priority_counts.get(p, 0) + 1
    
    # DCA performance
    dca_stats = {}
    for c in cases:
        dca = c.get('assigned_dca', 'Unassigned')
        if dca not in dca_stats:
            dca_stats[dca] = {'count': 0, 'total_amount': 0}
        dca_stats[dca]['count'] += 1
        dca_stats[dca]['total_amount'] += c['amount']
    
    # Top KPI Metrics Row
    st.markdown("#### 🎯 Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Total Cases", total_cases)
    with kpi2:
        st.metric("Portfolio Value", f"₹{total_outstanding:,.0f}")
    with kpi3:
        st.metric("SLA Compliance", f"{sla_compliance_rate}%", delta="Target: 85%")
    with kpi4:
        critical_count = priority_counts.get('Critical', 0)
        st.metric("Critical Cases", critical_count, delta="Needs Action", delta_color="inverse")
    with kpi5:
        st.metric("Active DCAs", len(dca_stats))
    
    st.markdown("---")
    
    # AI Analysis Metrics Row
    st.markdown("#### 🤖 AI Risk Classification Results")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cases Analyzed", stats['total'], delta=None)
    with col2:
        st.metric("High Risk", stats['high'], delta=f"{stats.get('high_percentage', 0)}%", delta_color="inverse")
    with col3:
        st.metric("Medium Risk", stats['medium'], delta=f"{stats.get('medium_percentage', 0)}%", delta_color="off")
    with col4:
        st.metric("Low Risk", stats['low'], delta=f"{stats.get('low_percentage', 0)}%", delta_color="normal")
    
    st.markdown("---")
    
    # Charts Row 1: Risk Distribution & DCA Performance
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 📊 Risk Distribution")
        if stats['total'] > 0:
            chart_data = pd.DataFrame({
                'Risk Level': ['High', 'Medium', 'Low'],
                'Count': [stats['high'], stats['medium'], stats['low']]
            })
            
            # Handle empty data case for Altair to prevent "Infinite extent" error
            y_scale = alt.Scale(nice=True)
            if chart_data['Count'].sum() == 0:
                y_scale = alt.Scale(domain=[0, 1])

            # Use Altair for custom colors per bar
            c = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('Risk Level', sort=['High', 'Medium', 'Low'], axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Count', scale=y_scale),
                color=alt.Color('Risk Level', scale=alt.Scale(
                    domain=['High', 'Medium', 'Low'],
                    range=['#ff4b4b', '#ffa726', '#66bb6a']
                ), legend=None),
                tooltip=['Risk Level', 'Count']
            ).properties(
                height=280
            )
            st.altair_chart(c, width="stretch")
        else:
            st.info("Run AI analysis on cases to see risk distribution.")
            
    with col_chart2:
        st.markdown("#### 🏢 DCA Portfolio Allocation")
        if dca_stats:
            dca_df = pd.DataFrame([
                {'DCA': dca, 'Cases': data['count'], 'Amount': data['total_amount']}
                for dca, data in dca_stats.items()
            ])
            
            dca_chart = alt.Chart(dca_df).mark_bar().encode(
                x=alt.X('Cases:Q'),
                y=alt.Y('DCA:N', sort='-x'),
                color=alt.Color('DCA:N', scale=alt.Scale(scheme='purples'), legend=None),
                tooltip=['DCA', 'Cases', alt.Tooltip('Amount:Q', format=',.0f')]
            ).properties(
                height=280
            )
            st.altair_chart(dca_chart, width="stretch")
    
    # Charts Row 2: Priority & SLA
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown("#### ⚡ Case Priority Breakdown")
        priority_order = ['Critical', 'High', 'Normal', 'Low']
        priority_df = pd.DataFrame([
            {'Priority': p, 'Count': priority_counts.get(p, 0)}
            for p in priority_order if priority_counts.get(p, 0) > 0
        ])
        
        if not priority_df.empty:
            priority_chart = alt.Chart(priority_df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta('Count:Q'),
                color=alt.Color('Priority:N', scale=alt.Scale(
                    domain=['Critical', 'High', 'Normal', 'Low'],
                    range=['#d32f2f', '#ff5722', '#2196f3', '#4caf50']
                )),
                tooltip=['Priority', 'Count']
            ).properties(
                height=280
            )
            st.altair_chart(priority_chart, width="stretch")
        else:
            st.info("No priority data available.")
    
    with col_chart4:
        st.markdown("#### ⏱️ SLA Status Overview")
        sla_breached = total_cases - sla_compliant
        sla_df = pd.DataFrame({
            'Status': ['Within SLA', 'SLA Breached'],
            'Count': [sla_compliant, sla_breached]
        })
        
        sla_chart = alt.Chart(sla_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('Count:Q'),
            color=alt.Color('Status:N', scale=alt.Scale(
                domain=['Within SLA', 'SLA Breached'],
                range=['#4caf50', '#f44336']
            )),
            tooltip=['Status', 'Count']
        ).properties(
            height=280
        )
        st.altair_chart(sla_chart, width="stretch")
    
    st.markdown("---")
    
    # Recent Activity & Quick Guide
    col_activity, col_guide = st.columns([1.5, 1])
    
    with col_activity:
        st.markdown("#### 🕐 Recent AI Decisions")
        decisions = st.session_state.pipeline.get_all_decisions()
        if decisions:
            recent_df = pd.DataFrame(decisions[-5:])
            if not recent_df.empty:
                display_df = pd.DataFrame({
                    "Time": recent_df['timestamp'].apply(lambda x: x.split('T')[1][:5]),
                    "Case": recent_df['case_id'],
                    "Risk": recent_df['ai_decision'].apply(lambda x: x['risk_level'])
                })
                st.dataframe(display_df, hide_index=True, width="stretch")
        else:
            st.info("No AI decisions yet. Go to Case Analysis to run assessments.")
    
    with col_guide:
        with st.container(border=True):
            st.markdown("**💡 Quick Start Guide**")
            st.markdown("""
            1. **Case Analysis** → Select & analyze cases
            2. **AI Assessment** → Get risk classification
            3. **Audit Log** → Track all decisions
            """)
            st.divider()
            mode = "🟢 AI Mode" if not st.session_state.pipeline.demo_mode else "🟡 Demo Mode"
            st.markdown(f"**System:** {mode}")
            st.markdown(f"**Decisions Made:** {stats['total']}")

# --- TAB 2: ANALYSIS ---
with tab_analysis:
    col_input, col_output = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.markdown("### 📂 Case File")
        
        # Fetch cases
        cases = st.session_state.pipeline.get_all_cases()
        case_options = {f"{c['case_id']} | {c['customer_name']}": c['case_id'] for c in cases}
        
        selected_option = st.selectbox("Select Case Record", options=list(case_options.keys()))
        selected_case_id = case_options[selected_option]
        
        # Get case details
        case_data = next(c for c in cases if c['case_id'] == selected_case_id)
        
        # Case File Card using native Streamlit components
        with st.container(border=True):
            # Header row with Case ID and Priority Badge
            header_col1, header_col2, header_col3 = st.columns([2.5, 1, 1])
            with header_col1:
                st.subheader(case_data['customer_name'])
            with header_col2:
                st.markdown(f"<span style='background-color: #e3f2fd; color: #1f77b4; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold;'>{case_data['case_id']}</span>", unsafe_allow_html=True)
            with header_col3:
                # Priority badge with color coding
                priority = case_data.get('priority', 'Normal')
                priority_colors = {
                    'Critical': '#d32f2f',
                    'High': '#ff5722',
                    'Normal': '#2196f3',
                    'Low': '#4caf50'
                }
                p_color = priority_colors.get(priority, '#2196f3')
                st.markdown(f"<span style='background-color: {p_color}; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold;'>{priority}</span>", unsafe_allow_html=True)
            
            # Financial details grid
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.caption("Amount Outstanding")
                st.markdown(f"**₹{case_data['amount']:,}**")
                st.caption("Loan Type")
                st.markdown(f"**{case_data['loan_type']}**")
            with detail_col2:
                st.caption("Days Overdue")
                st.markdown(f"<span style='color: #d32f2f; font-weight: bold;'>{case_data['days_overdue']} days</span>", unsafe_allow_html=True)
                st.caption("Customer Type")
                st.markdown(f"**{case_data['customer_type']}**")
            
            st.divider()
            
            # DCA & SLA Information Row
            dca_col1, dca_col2 = st.columns(2)
            with dca_col1:
                st.caption("🏢 Assigned DCA")
                st.markdown(f"**{case_data.get('assigned_dca', 'Unassigned')}**")
                st.caption("🌍 Region")
                st.markdown(f"**{case_data.get('region', 'N/A')}**")
            with dca_col2:
                sla_days = case_data.get('sla_days', 30)
                days_overdue = case_data.get('days_overdue', 0)
                sla_remaining = sla_days - days_overdue
                
                st.caption("⏱️ SLA Target")
                st.markdown(f"**{sla_days} days**")
                
                st.caption("📊 SLA Status")
                if sla_remaining > 10:
                    st.markdown(f"<span style='color: #4caf50; font-weight: bold;'>✅ On Track ({sla_remaining} days left)</span>", unsafe_allow_html=True)
                elif sla_remaining > 0:
                    st.markdown(f"<span style='color: #ff9800; font-weight: bold;'>⚠️ At Risk ({sla_remaining} days left)</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color: #f44336; font-weight: bold;'>🚨 BREACHED ({abs(sla_remaining)} days over)</span>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown(f"🔄 **Recovery Attempts:** {case_data['past_attempts']}")
        
        st.write("") # Spacer
        
        analyze_btn = st.button("⚡ RUN AI RISK ASSESSMENT", type="primary")
        
        if analyze_btn:
            with st.status("🤖 AI Agent Working...", expanded=True) as status:
                st.write("📥 Fetching case data from secure DB...")
                time.sleep(0.5)
                st.write("🔄 Preprocessing & Normalizing attributes...")
                time.sleep(0.5)
                st.write("🧠 Generating risk profile with Gemini 1.5...")
                st.session_state.analysis_result = st.session_state.pipeline.process_case(selected_case_id)
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

    with col_output:
        st.markdown("### 🛡️ Risk Assessment Report")
        
        result = st.session_state.analysis_result
        
        if result and result['case_id'] == selected_case_id:
            classification = result['classification']
            risk = classification['risk_level']
            
            # Main Verdict Card
            badge_color = "#ff4b4b" if risk == "HIGH" else "#ffa726" if risk == "MEDIUM" else "#66bb6a"
            
            # Recovery prediction
            recovery_prob = classification.get('recovery_probability', 'MODERATE')
            recovery_pct = classification.get('recovery_percentage', 50)
            recovery_color = "#4caf50" if recovery_pct >= 60 else "#ff9800" if recovery_pct >= 40 else "#f44336"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {badge_color} 0%, {badge_color}dd 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 0.9em; opacity: 0.9; letter-spacing: 1px;">RISK CLASSIFICATION</div>
                <div style="font-size: 2.5em; font-weight: 800; margin: 5px 0;">{risk} RISK</div>
                <div style="font-size: 0.9em; background: rgba(255,255,255,0.2); display: inline-block; padding: 2px 10px; border-radius: 15px;">Confidence: {classification.get('confidence', 0):.0%}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Recovery Prediction Card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {recovery_color}22 0%, {recovery_color}11 100%); padding: 15px; border-radius: 10px; border-left: 4px solid {recovery_color}; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.85em; color: #666; text-transform: uppercase; letter-spacing: 1px;">Recovery Prediction</div>
                        <div style="font-size: 1.3em; font-weight: 700; color: {recovery_color};">{recovery_prob}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 2em; font-weight: 800; color: {recovery_color};">{recovery_pct}%</div>
                        <div style="font-size: 0.75em; color: #888;">Estimated Recovery</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs for details
            tab_reason, tab_action, tab_tech = st.tabs(["📝 Reasoning", "🚀 Action Plan", "⚙️ Under the Hood"])
            
            with tab_reason:
                st.info(classification.get('reason'))
                
            with tab_action:
                st.success(f"**Recommended Strategy:**\n\n{classification.get('recommended_action')}")
                
            with tab_tech:
                st.markdown("**Explainability Module**")
                st.caption("See how raw data is transformed into AI-ready context.")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("`Raw Input`")
                    st.json({
                        "amount": case_data['amount'],
                        "days": case_data['days_overdue'],
                        "attempts": case_data['past_attempts']
                    })
                with c2:
                    st.markdown("`AI Context`")
                    # Extract relevant lines from context
                    context_lines = result['processed_context'].strip().split('\n')
                    # Filter for interesting lines
                    filtered_context = [line for line in context_lines if line.strip() and not line.startswith("CASE DETAILS")]
                    st.code("\n".join(filtered_context[:6]) + "\n...", language="text")
            
            # Action buttons after analysis
            st.markdown("---")
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🔄 Analyze Another Case", width="stretch"):
                    st.session_state.analysis_result = None
                    st.rerun()
            with btn_col2:
                st.markdown("👉 Check **Audit Log** tab to see full history")

        else:
            # Empty State
            st.markdown("""
            <div style="text-align:center; padding: 4rem 2rem; color: #aaa; border: 2px dashed #eee; border-radius: 12px; background: #fafafa;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">👈</div>
                <p style="font-size: 1.1rem; font-weight: 500;">Select a case and run analysis</p>
                <p style="font-size: 0.9rem;">AI will generate a comprehensive risk profile here.</p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 3: AUDIT LOG ---
with tab_audit:
    st.markdown("### 📜 Decision Audit Trail")
    st.caption("Full history of AI decisions for governance and compliance.")
    
    all_decisions = st.session_state.pipeline.get_all_decisions()
    
    if all_decisions:
        # Flatten data for table
        table_data = []
        for d in all_decisions:
            table_data.append({
                "Decision ID": d['decision_id'],
                "Timestamp": d['timestamp'][:19].replace("T", " "),
                "Case ID": d['case_id'],
                "Customer": d['customer_name'],
                "Risk Level": d['ai_decision']['risk_level'],
                "Confidence": f"{d['ai_decision'].get('confidence', 0):.2f}",
                "Reason": d['ai_decision']['reason']
            })
        
        df = pd.DataFrame(table_data)
        
        # Better Filter UX with toggle buttons
        st.markdown("**Filter by Risk Level:**")
        filter_cols = st.columns([1, 1, 1, 2])
        
        # Initialize filter state
        if 'filter_high' not in st.session_state:
            st.session_state.filter_high = False
        if 'filter_medium' not in st.session_state:
            st.session_state.filter_medium = False
        if 'filter_low' not in st.session_state:
            st.session_state.filter_low = False
        
        with filter_cols[0]:
            if st.button("🔴 HIGH", width="stretch", type="primary" if st.session_state.filter_high else "secondary"):
                st.session_state.filter_high = not st.session_state.filter_high
                st.rerun()
        with filter_cols[1]:
            if st.button("🟠 MEDIUM", width="stretch", type="primary" if st.session_state.filter_medium else "secondary"):
                st.session_state.filter_medium = not st.session_state.filter_medium
                st.rerun()
        with filter_cols[2]:
            if st.button("🟢 LOW", width="stretch", type="primary" if st.session_state.filter_low else "secondary"):
                st.session_state.filter_low = not st.session_state.filter_low
                st.rerun()
        with filter_cols[3]:
            if st.button("🔄 Clear Filters", width="stretch"):
                st.session_state.filter_high = False
                st.session_state.filter_medium = False
                st.session_state.filter_low = False
                st.rerun()
        
        # Apply filters
        active_filters = []
        if st.session_state.filter_high:
            active_filters.append("HIGH")
        if st.session_state.filter_medium:
            active_filters.append("MEDIUM")
        if st.session_state.filter_low:
            active_filters.append("LOW")
        
        if active_filters:
            df = df[df["Risk Level"].isin(active_filters)]
            st.caption(f"Showing: {', '.join(active_filters)} ({len(df)} records)")
        else:
            st.caption(f"Showing all records ({len(df)} total)")
        
        st.dataframe(
            df, 
            width="stretch",
            column_config={
                "Risk Level": st.column_config.TextColumn(
                    "Risk Level",
                    help="AI Determined Risk",
                    validate="^(HIGH|MEDIUM|LOW)$"
                ),
            },
            hide_index=True
        )
        
        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Audit Report (CSV)",
            csv,
            "risk_audit_report.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No decisions recorded yet.")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
    AI-Driven Risk Classification System • IIT Kharagpur Project<br>
    Built for Explainability, Accountability & Speed
</div>
""", unsafe_allow_html=True)
