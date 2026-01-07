import streamlit as st
import requests
import json
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import your pipeline functions
from src.ingestion.load_data2 import load_excel_to_dfs, save_processed
from src.preprocessing.clean_transform import process_sheet
from src.llm.prompt_template2 import build_summary_prompt
from src.llm.generate_insights import call_llm

# Page config
st.set_page_config(
    page_title="Financial Analysis AI",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for clean design
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #1f77b4;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .info-msg {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def process_uploaded_file(uploaded_file):
    """
    Process the uploaded Excel file through the complete pipeline
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        dict: Analysis results or error
    """
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Save uploaded file
            input_path = temp_dir / "input.xlsx"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info("📥 File uploaded successfully")
            
            # Step 1: Load Excel sheets
            with st.spinner("📊 Loading Excel sheets..."):
                sheets = load_excel_to_dfs(input_path)
                st.success(f"✅ Loaded {len(sheets)} sheets: {', '.join(sheets.keys())}")
            
            # Step 2: Save to processed directory
            processed_dir = temp_dir / "processed"
            processed_dir.mkdir(exist_ok=True)
            
            with st.spinner("💾 Processing sheets..."):
                save_processed(sheets=sheets, output_dir=processed_dir)
            
            # Step 3: Clean and transform data
            all_dfs = {}
            output_dir = temp_dir / "output"
            output_dir.mkdir(exist_ok=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, sheet_name in enumerate(sheets.keys()):
                status_text.text(f"🔄 Cleaning {sheet_name}...")
                
                input_csv = processed_dir / f"{sheet_name.replace(' ', '_')}.csv"
                output_csv = output_dir / f"cleaned_{sheet_name.replace(' ', '_')}.csv"
                
                # Clean the data
                process_sheet(csv_path=input_csv, out_path=output_csv)
                
                # Load cleaned data (limit rows for performance)
                df = pd.read_csv(output_csv).head(100)
                all_dfs[sheet_name] = df
                
                progress_bar.progress((idx + 1) / len(sheets))
            
            status_text.text("✅ Data cleaning complete")
            progress_bar.empty()
            
            # Step 4: Combine all sheets
            with st.spinner("🔗 Combining data from all sheets..."):
                combined_context = build_combined_context(all_dfs)
                st.success(f"✅ Combined {len(all_dfs)} sheets ({len(combined_context)} characters)")
            
            # Step 5: Build prompt
            with st.spinner("📝 Building analysis prompt..."):
                final_prompt = build_summary_prompt(combined_context)
            
            # Step 6: Generate AI insights
            with st.spinner("🤖 Generating AI insights (this may take 1-2 minutes)..."):
                try:
                    llm_response = call_llm(prompt=final_prompt, model='llama3.1:8b')
                    
                    # Try to parse as JSON
                    try:
                        analysis = json.loads(llm_response)
                    except json.JSONDecodeError:
                        analysis = {"raw_response": llm_response}
                    
                    st.success("✅ Analysis complete!")
                    return analysis, None
                    
                except Exception as llm_error:
                    return None, f"LLM Error: {str(llm_error)}"
    
    except Exception as e:
        return None, f"Processing Error: {str(e)}"


def build_combined_context(dataframes_dict):
    """Combine all DataFrames into a single context string"""
    all_context = []
    
    for sheet_name, df in dataframes_dict.items():
        all_context.append("=" * 60)
        all_context.append(f"Sheet: {sheet_name}")
        all_context.append("=" * 60)
        all_context.append(f"Rows: {len(df)}, Columns: {list(df.columns)}")
        all_context.append("")
        
        csv_data = df.to_csv(index=False)
        all_context.append(csv_data)
        all_context.append("")
    
    return '\n'.join(all_context)


def display_analysis(analysis):
    """Display the analysis results in a clean format"""
    
    # Executive Summary
    if 'executive_summary' in analysis:
        st.markdown('<div class="section-header">📊 Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-msg">{analysis["executive_summary"]}</div>', unsafe_allow_html=True)
    
    # Key Metrics
    if 'key_metrics' in analysis:
        st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
        metrics = analysis['key_metrics']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**💰 Revenue Trend**")
            st.write(metrics.get('revenue_trend', 'N/A'))
        with col2:
            st.markdown("**📊 Profitability**")
            st.write(metrics.get('profitability', 'N/A'))
        with col3:
            st.markdown("**💵 Cash Flow**")
            st.write(metrics.get('cash_flow', 'N/A'))
    
    # Risks and Opportunities
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">⚠️ Key Risks</div>', unsafe_allow_html=True)
        if 'risks' in analysis and isinstance(analysis['risks'], list):
            for i, risk in enumerate(analysis['risks'], 1):
                st.markdown(f"**{i}.** {risk}")
        else:
            st.info("No risks identified")
    
    with col2:
        st.markdown('<div class="section-header">💡 Opportunities</div>', unsafe_allow_html=True)
        if 'opportunities' in analysis and isinstance(analysis['opportunities'], list):
            for i, opp in enumerate(analysis['opportunities'], 1):
                st.markdown(f"**{i}.** {opp}")
        else:
            st.info("No opportunities identified")
    
    # Strategic Actions
    st.markdown('<div class="section-header">🎯 Strategic Actions</div>', unsafe_allow_html=True)
    
    actions = analysis.get('strategic_actions') or analysis.get('actions', [])
    if actions and isinstance(actions, list):
        for i, action in enumerate(actions, 1):
            with st.expander(f"**Action {i}: {action.get('title', 'N/A')}**"):
                st.markdown(f"**Rationale:** {action.get('rationale', 'N/A')}")
                if 'expected_impact' in action:
                    st.markdown(f"**Expected Impact:** {action.get('expected_impact')}")
    else:
        st.info("No strategic actions available")
    
    # Cross-Sheet Insights
    if 'cross_sheet_insights' in analysis:
        st.markdown('<div class="section-header">🔍 Cross-Sheet Analysis</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-msg">{analysis["cross_sheet_insights"]}</div>', unsafe_allow_html=True)
    
    # Raw Response (if JSON parsing failed)
    if 'raw_response' in analysis:
        st.markdown('<div class="section-header">📄 Raw Analysis</div>', unsafe_allow_html=True)
        st.text_area("Full Response", analysis['raw_response'], height=300)
    
    # Download button
    st.markdown("---")
    st.download_button(
        label="📥 Download Analysis (JSON)",
        data=json.dumps(analysis, indent=2),
        file_name="financial_analysis.json",
        mime="application/json"
    )


def main():
    # Header
    st.markdown('<p class="main-title">💰 Financial Analysis AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your financial data and get AI-powered insights</p>', unsafe_allow_html=True)
    
    # Check Ollama status
    with st.expander("⚙️ System Status"):
        try:
            import httpx
            response = httpx.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                st.markdown('<div class="success-msg">✅ Ollama is running</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-msg">❌ Ollama is not responding</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="error-msg">❌ Ollama is not running. Start it with: <code>ollama serve</code></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Upload Financial Data (Excel file)",
        type=['xlsx', 'xls'],
        help="Upload an Excel file with multiple sheets (P&L, Cashflow, KPI, etc.)"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.markdown(f"**📄 File:** {uploaded_file.name}")
        st.markdown(f"**📦 Size:** {uploaded_file.size / 1024:.2f} KB")
        
        # Process button
        if st.button("🚀 Analyze Financial Data", type="primary", use_container_width=True):
            
            # Clear previous results
            if 'analysis_result' in st.session_state:
                del st.session_state['analysis_result']
            
            # Process the file
            analysis, error = process_uploaded_file(uploaded_file)
            
            if error:
                st.markdown(f'<div class="error-msg">❌ {error}</div>', unsafe_allow_html=True)
                
                # Show helpful tips
                if "Ollama" in error or "timeout" in error.lower():
                    st.markdown("""
                    ### 💡 Troubleshooting Tips:
                    1. Make sure Ollama is running: `ollama serve`
                    2. Verify the model is available: `ollama list`
                    3. Pull the model if needed: `ollama pull llama3.1:8b`
                    4. Try with a smaller file or fewer rows
                    """)
            else:
                # Store in session state
                st.session_state['analysis_result'] = analysis
                st.markdown('<div class="success-msg">✅ Analysis completed successfully!</div>', unsafe_allow_html=True)
    
    # Display results if available
    if 'analysis_result' in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        display_analysis(st.session_state['analysis_result'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Financial Analysis AI v2.0 | Powered by Ollama & Python</p>
        <p style='font-size: 0.9rem;'>Upload → Process → Analyze → Download</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
