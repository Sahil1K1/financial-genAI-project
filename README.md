# 💰 Financial Analysis Dashboard with AI

A comprehensive financial analysis system that uses AI to analyze financial data and generate actionable insights through an interactive web dashboard.

## 🌟 Features

- **📊 Data Pipeline**: Automated ETL pipeline for financial data processing
- **🤖 AI-Powered Analysis**: Uses Ollama LLM (llama3.1:8b) for intelligent insights
- **🚀 REST API**: FastAPI backend for serving analysis results
- **🎨 Interactive Dashboard**: Beautiful Streamlit UI for visualization
- **📈 Comprehensive Analysis**:
  - Executive summaries
  - Risk identification
  - Opportunity detection
  - Strategic recommendations
  - Cross-sheet financial analysis

## 📋 Prerequisites

### Required Software:
- **Python 3.11+**
- **Ollama** ([Download](https://ollama.ai/download))

### Required Python Packages:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Option 1: Using Batch Files (Windows - Easiest)

1. **Run the Pipeline:**
   ```bash
   run_pipeline.bat
   ```

2. **Start the Dashboard:**
   ```bash
   start_dashboard.bat
   ```

3. **Open Browser:**
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

1. **Start Ollama (Terminal 1):**
   ```bash
   ollama serve
   ```

2. **Run the Data Pipeline (Terminal 1, after Ollama starts):**
   ```bash
   python -m workflow.pipeline2
   ```

3. **Start FastAPI Backend (Terminal 2):**
   ```bash
   python -m src.app
   ```

4. **Start Streamlit Dashboard (Terminal 3):**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📁 Project Structure

```
financial-gen-ai-project/
│
├── data/
│   ├── raw/                          # Input Excel files
│   │   └── Financial_data_final.xlsx
│   ├── processed/                    # Processed CSV files
│   └── outputs/                      # AI-generated insights
│       └── llm_output.json
│
├── src/
│   ├── app.py                        # FastAPI application
│   ├── ingestion/
│   │   └── load_data2.py            # Data loading utilities
│   ├── preprocessing/
│   │   └── clean_transform.py       # Data cleaning
│   ├── llm/
│   │   ├── prompt_template2.py      # Prompt engineering
│   │   └── generate_insights.py    # LLM integration
│   └── utils/
│       └── logger.py                # Logging utilities
│
├── workflow/
│   ├── pipeline2.py                 # Main data pipeline
│   └── pipeline2_fixed.py          # Enhanced pipeline version
│
├── streamlit_app.py                 # Streamlit dashboard UI
├── run_pipeline.bat                 # Pipeline runner script
├── start_dashboard.bat              # Dashboard launcher script
├── requirements.txt                 # Python dependencies
└── HOW_TO_RUN.md                   # Detailed instructions

```

## 🔄 Complete Workflow

```
┌─────────────┐
│ Excel Data  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Data Pipeline       │
│ (workflow/pipeline2)│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Ollama LLM         │
│ (llama3.1:8b)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ JSON Output        │
│ (llm_output.json)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ FastAPI Backend    │
│ (src/app.py)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Streamlit Dashboard│
│ (streamlit_app.py) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ User Browser       │
│ localhost:8501     │
└────────────────────┘
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/summary` | GET | Financial analysis summary |
| `/docs` | GET | Interactive API documentation |

## 🖥️ Dashboard Features

### 📊 Overview Tab
- Executive summary with AI-generated insights
- Key metrics (Revenue, Profitability, Cash Flow)
- Cross-sheet analysis

### ⚠️ Risks & Opportunities Tab
- Top 3 financial risks
- Top 3 growth opportunities
- Side-by-side comparison

### 🎯 Strategic Actions Tab
- Actionable recommendations
- Detailed rationale for each action
- Expected business impact

### 📄 Raw Data Tab
- Complete JSON response
- Useful for debugging and detailed analysis

## 🔧 Configuration

### Adjust LLM Timeout (if needed):
Edit `src/llm/generate_insights.py`:
```python
llm = Ollama(model=model, request_timeout=700)  # Increase if needed
```

### Change LLM Model:
Edit `workflow/pipeline2.py`:
```python
llm_response = call_llm(prompt=prompt, model='llama3.1:8b')  # Change model here
```

### Modify Data Rows:
Edit `workflow/pipeline2.py`:
```python
df = pd.read_csv(output_csv).head(100)  # Adjust row limit
```

## 🐛 Troubleshooting

### Issue: "API is not running"
**Solution:**
```bash
python -m src.app
```

### Issue: "No summaries found"
**Solution:**
```bash
python -m workflow.pipeline2
```

### Issue: "Cannot connect to Ollama"
**Solution:**
```bash
# Start Ollama
ollama serve

# Pull the model
ollama pull llama3.1:8b
```

### Issue: JSON parsing errors
**Solution:**
- Check `data/outputs/llm_output.json` for valid JSON
- Re-run the pipeline with: `python -m workflow.pipeline2`

### Issue: Timeout errors
**Solution:**
- Increase timeout in `generate_insights.py`
- Use smaller data samples (reduce `.head()` rows)
- Use a smaller/faster model

## 📊 Sample Output

The AI generates structured JSON with:

```json
{
  "executive_summary": "...",
  "key_metrics": {
    "revenue_trend": "...",
    "profitability": "...",
    "cash_flow": "..."
  },
  "risks": ["...", "...", "..."],
  "opportunities": ["...", "...", "..."],
  "strategic_actions": [
    {
      "title": "...",
      "rationale": "...",
      "expected_impact": "..."
    }
  ],
  "cross_sheet_insights": "..."
}
```

## 🚀 Performance Tips

1. **Limit data rows**: Use `.head(50)` or `.head(100)` for faster processing
2. **Use SSD**: Store data on SSD for faster I/O
3. **Increase timeout**: For large datasets, increase LLM timeout
4. **Use smaller model**: Switch to `llama3.2:1b` for faster (but less accurate) results

## 📝 License

This project is for educational and internal use.

## 🤝 Contributing

This is an internal project. For suggestions or issues, contact the development team.

## 📞 Support

For help:
1. Check `HOW_TO_RUN.md` for detailed instructions
2. Review terminal logs for error messages
3. Verify all services are running (Ollama, FastAPI, Streamlit)

---

**Built with ❤️ using Python, FastAPI, Streamlit, and AI**
