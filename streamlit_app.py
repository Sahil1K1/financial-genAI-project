import streamlit as st
import requests
import json
import pandas as pd
from pathlib import Path
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Financial Analysis Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_summary():
    """Get financial summary from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/summary", timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get('detail', 'Unknown error')
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Make sure the FastAPI server is running."
    except Exception as e:
        return None, str(e)


def display_executive_summary(data):
    """Display executive summary section"""
    st.markdown('<p class="section-header">📊 Executive Summary</p>', unsafe_allow_html=True)
    
    if 'executive_summary' in data:
        st.markdown(f'<div class="info-box">{data["executive_summary"]}</div>', unsafe_allow_html=True)
    else:
        st.info("Executive summary not available")


def display_key_metrics(data):
    """Display key metrics section"""
    st.markdown('<p class="section-header">📈 Key Metrics</p>', unsafe_allow_html=True)
    
    if 'key_metrics' in data:
        metrics = data['key_metrics']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Revenue Trend**")
            st.write(metrics.get('revenue_trend', 'N/A'))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Profitability**")
            st.write(metrics.get('profitability', 'N/A'))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Cash Flow**")
            st.write(metrics.get('cash_flow', 'N/A'))
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Key metrics not available")


def display_risks(data):
    """Display risks section"""
    st.markdown('<p class="section-header">⚠️ Key Risks</p>', unsafe_allow_html=True)
    
    if 'risks' in data and isinstance(data['risks'], list):
        for i, risk in enumerate(data['risks'], 1):
            st.markdown(f"**{i}.** {risk}")
    else:
        st.info("Risk analysis not available")


def display_opportunities(data):
    """Display opportunities section"""
    st.markdown('<p class="section-header">💡 Opportunities</p>', unsafe_allow_html=True)
    
    if 'opportunities' in data and isinstance(data['opportunities'], list):
        for i, opportunity in enumerate(data['opportunities'], 1):
            st.markdown(f"**{i}.** {opportunity}")
    else:
        st.info("Opportunities analysis not available")


def display_strategic_actions(data):
    """Display strategic actions section"""
    st.markdown('<p class="section-header">🎯 Strategic Actions</p>', unsafe_allow_html=True)
    
    if 'strategic_actions' in data and isinstance(data['strategic_actions'], list):
        for i, action in enumerate(data['strategic_actions'], 1):
            with st.expander(f"Action {i}: {action.get('title', 'N/A')}"):
                st.markdown(f"**Rationale:** {action.get('rationale', 'N/A')}")
                if 'expected_impact' in action:
                    st.markdown(f"**Expected Impact:** {action.get('expected_impact')}")
    elif 'actions' in data and isinstance(data['actions'], list):
        # Fallback to 'actions' field
        for i, action in enumerate(data['actions'], 1):
            with st.expander(f"Action {i}: {action.get('title', 'N/A')}"):
                st.markdown(f"**Rationale:** {action.get('rationale', 'N/A')}")
    else:
        st.info("Strategic actions not available")


def display_cross_sheet_insights(data):
    """Display cross-sheet insights"""
    st.markdown('<p class="section-header">🔍 Cross-Sheet Analysis</p>', unsafe_allow_html=True)
    
    if 'cross_sheet_insights' in data:
        st.markdown(f'<div class="info-box">{data["cross_sheet_insights"]}</div>', unsafe_allow_html=True)
    else:
        st.info("Cross-sheet insights not available")


def display_raw_response(data):
    """Display raw response in expandable section"""
    with st.expander("📄 View Raw JSON Response"):
        st.json(data)


def main():
    # Header
    st.markdown('<p class="main-header">💰 Financial Analysis Dashboard</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/financial-growth-analysis.png", width=100)
        st.markdown("### 📊 Dashboard Controls")
        
        # API Status
        st.markdown("---")
        st.markdown("#### API Status")
        if check_api_health():
            st.markdown('<div class="success-box">✅ API is running</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ API is not running</div>', unsafe_allow_html=True)
            st.markdown("""
            **To start the API:**
            ```bash
            python -m src.app
            ```
            or
            ```bash
            uvicorn src.app:app --reload
            ```
            """)
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Analysis", type="primary", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Info section
        st.markdown("#### ℹ️ About")
        st.info("""
        This dashboard displays comprehensive financial analysis including:
        - Executive Summary
        - Key Metrics
        - Risk Analysis
        - Opportunities
        - Strategic Actions
        """)
        
        st.markdown("---")
        st.markdown("#### 🔗 API Endpoints")
        st.code(f"{API_BASE_URL}/summary", language="text")
        st.code(f"{API_BASE_URL}/health", language="text")
    
    # Main content
    if not check_api_health():
        st.markdown('<div class="error-box">⚠️ API is not running. Please start the FastAPI server first.</div>', unsafe_allow_html=True)
        st.markdown("""
        ### How to start the API:
        
        **Option 1: Using Python module**
        ```bash
        python -m src.app
        ```
        
        **Option 2: Using Uvicorn**
        ```bash
        uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
        ```
        """)
        return
    
    # Load summary
    with st.spinner("Loading financial analysis..."):
        summary_data, error = get_summary()
    
    if error:
        st.markdown(f'<div class="error-box">❌ Error: {error}</div>', unsafe_allow_html=True)
        
        if "Run the pipeline first" in error or "No summaries found" in error:
            st.markdown("""
            ### 📋 Next Steps:
            
            The analysis hasn't been generated yet. Please run the pipeline first:
            
            ```bash
            python -m workflow.pipeline2
            ```
            
            This will:
            1. Load and process financial data
            2. Clean and transform the data
            3. Generate comprehensive AI-powered insights
            4. Save results to `data/outputs/llm_output.json`
            
            After the pipeline completes, refresh this page to view the analysis.
            """)
        return
    
    if not summary_data:
        st.error("No data received from API")
        return
    
    # Handle raw response
    if 'raw_response' in summary_data:
        st.markdown('<div class="info-box">ℹ️ The LLM response is in raw text format (not JSON). Displaying as-is.</div>', unsafe_allow_html=True)
        st.markdown("### LLM Response:")
        st.text_area("Response", summary_data['raw_response'], height=400)
        display_raw_response(summary_data)
        return
    
    # Display all sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚠️ Risks & Opportunities", "🎯 Strategic Actions", "📄 Raw Data"])
    
    with tab1:
        display_executive_summary(summary_data)
        display_key_metrics(summary_data)
        display_cross_sheet_insights(summary_data)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            display_risks(summary_data)
        with col2:
            display_opportunities(summary_data)
    
    with tab3:
        display_strategic_actions(summary_data)
    
    with tab4:
        display_raw_response(summary_data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Financial Analysis Dashboard v1.0.0 | Powered by AI & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
