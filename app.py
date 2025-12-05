"""
EditalShield Web Dashboard
Powered by Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from editalshield.modules import MemorialProtector, EditalMatcher, JuridicalAgent, KnowledgeConnector

# Page Config
st.set_page_config(
    page_title="EditalShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyberpunk Look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        color: #00ff00;
        border-color: #00ff00;
        background-color: transparent;
    }
    .stButton>button:hover {
        background-color: #00ff00;
        color: #000000;
    }
    h1, h2, h3 {
        color: #00ff00 !important;
        font-family: 'Courier New', monospace;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ EditalShield")
st.sidebar.markdown("---")
mode = st.sidebar.radio("Mode", ["🔍 Analyze & Protect", "🎯 Find Opportunities", "📊 Dashboard"])

# Initialize Modules
@st.cache_resource
def load_modules():
    protector = MemorialProtector()
    matcher = EditalMatcher()
    matcher.load_editals_from_db()
    juridical = JuridicalAgent()
    connector = KnowledgeConnector()
    return protector, matcher, juridical, connector

protector, matcher, juridical, connector = load_modules()

if mode == "🔍 Analyze & Protect":
    st.title("Memorial Analysis Protocol")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Stream")
        text_input = st.text_area("Paste your technical memorial here...", height=400)
        
        if st.button("INITIATE SCAN"):
            if text_input:
                with st.spinner("Scanning for IP risks..."):
                    # 1. Technical Analysis
                    analysis = protector.analyze_memorial(text_input)
                    protected, _ = protector.generate_protected_memorial(text_input)
                    
                    # 2. Legal Analysis
                    legal_opinion = juridical.analyze_legal_risk(analysis)
                    
                    st.session_state['analysis'] = analysis
                    st.session_state['protected'] = protected
                    st.session_state['legal_opinion'] = legal_opinion
                    st.session_state['text_input'] = text_input
    
    with col2:
        st.subheader("Analysis Result")
        if 'analysis' in st.session_state:
            analysis = st.session_state['analysis']
            legal = st.session_state['legal_opinion']
            
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            m1.metric("Risk Score", f"{analysis.overall_risk_score}/100", 
                     delta="-High Risk" if analysis.overall_risk_score > 50 else "Safe",
                     delta_color="inverse")
            m2.metric("Legal Status", legal.status)
            m3.metric("Violations", len(legal.citations))
            
            # Legal Alert Box
            if legal.risk_level == "HIGH":
                st.error(f"⚖️ **LEGAL ALERT:** {legal.recommendation}")
            elif legal.risk_level == "MODERATE":
                st.warning(f"⚖️ **LEGAL WARNING:** {legal.recommendation}")
            else:
                st.success(f"⚖️ **LEGAL OPINION:** {legal.recommendation}")

            # Radar Chart (Pentagram Shape - 5 Axes)
            categories = ['Entropy', 'Zipf', 'Patterns', 'Technicality', 'Legal Risk']
            
            # Calculate Legal Risk Value
            legal_val = 0.2
            if legal.risk_level == "MODERATE": legal_val = 0.6
            if legal.risk_level == "HIGH": legal_val = 1.0

            values = [
                analysis.paragraphs[0].entropy_normalized if analysis.paragraphs else 0,
                0.8 if analysis.overall_risk_score > 50 else 0.2, 
                min(1.0, analysis.overall_risk_score/100),
                0.9,
                legal_val
            ]
            
            # Close the loop for the chart
            categories = [*categories, categories[0]]
            values = [*values, values[0]]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line_color='#00ff00'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Novelty Check Button
            st.markdown("---")
            st.subheader("🌐 External Validation")
            if st.button("CHECK PATENT CONFLICTS (USPTO/Google)"):
                with st.spinner("Searching global patent databases..."):
                    # Extract keywords from text (simple heuristic)
                    keywords = [w for w in st.session_state['text_input'].split() if len(w) > 6][:3]
                    results = connector.search_patents(keywords)
                    
                    if results:
                        st.warning(f"⚠️ Found {len(results)} potential patent conflicts!")
                        for r in results:
                            st.markdown(f"- [{r.title}]({r.url}) ({r.source})")
                    else:
                        st.success("✅ No direct patent conflicts found in USPTO/Google Patents.")
            
            # Protected Text Tab
            with st.expander("🛡️ VIEW PROTECTED VERSION", expanded=True):
                st.code(st.session_state['protected'], language='text')

elif mode == "🎯 Find Opportunities":
    st.title("Edital Matcher System")
    
    query = st.text_input("Describe your project/startup:")
    sector = st.selectbox("Sector", ["All", "Agritech", "Healthtech", "Fintech", "Biotech"])
    
    if st.button("SEARCH DATABASE"):
        if query:
            matches = matcher.match_project(query, sector=None if sector == "All" else sector.lower())
            
            for m in matches:
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{m.name}</h3>
                        <p style="color: #00ccff">{m.agency}</p>
                        <p>Match Score: <b style="color: #00ff00">{m.match_score:.1f}%</b></p>
                        <p><i>{m.relevance_reason}</i></p>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)

elif mode == "📊 Dashboard":
    st.title("Ecosystem Overview")
    st.info("Coming soon: Real-time analytics of Brazilian innovation grants.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("EditalShield v0.3.0")
st.sidebar.caption("Developed by **Symbeon Labs**")

