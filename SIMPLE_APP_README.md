# 💰 Simple Financial Analysis App

A streamlined, user-friendly application for uploading Excel files and getting AI-powered financial insights.

## 🎯 Features

- ✅ **Simple File Upload** - Just drag & drop your Excel file
- ✅ **Automatic Processing** - Cleans and transforms data automatically
- ✅ **AI-Powered Analysis** - Generates comprehensive insights using Ollama
- ✅ **Clean Interface** - No clutter, just results
- ✅ **Download Results** - Export analysis as JSON

## 🚀 Quick Start

### Step 1: Start Ollama
```bash
ollama serve
```

### Step 2: Run the App
**Option 1 - Double-click:**
```
start_simple_app.bat
```

**Option 2 - Command line:**
```bash
streamlit run app_simple.py
```

### Step 3: Use the App
1. Open browser: http://localhost:8501
2. Upload your Excel file
3. Click "Analyze Financial Data"
4. Wait 1-2 minutes
5. View and download results!

## 📁 Excel File Requirements

Your Excel file should contain financial data sheets like:
- P&L Statement (Profit & Loss)
- Cashflow Statement
- KPI Summary

**Example columns:**
- Date
- Revenue
- Expenses
- EBITDA
- Free_Cash_Flow
- etc.

## 📊 What You Get

The AI generates:
- **Executive Summary** - Overview of financial health
- **Key Metrics** - Revenue trends, profitability, cash flow
- **Risks** - Top 3 financial risks
- **Opportunities** - Top 3 growth opportunities
- **Strategic Actions** - Actionable recommendations
- **Cross-Sheet Analysis** - Insights from all data combined

## ⚙️ System Requirements

- **Python 3.11+**
- **Ollama** with `llama3.1:8b` model
- **Required packages:**
  ```bash
  pip install streamlit pandas openpyxl llama-index httpx
  ```

## 🐛 Troubleshooting

### "Ollama is not running"
```bash
# Start Ollama
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.1:8b
```

### Analysis takes too long
- Use smaller Excel files
- Reduce number of rows in the data
- The app limits to 100 rows per sheet for performance

### Connection errors
- Make sure Ollama is running on port 11434
- Check firewall settings
- Restart Ollama if needed

## 🎨 App Interface

### Upload Section
- Simple file uploader
- Shows file name and size
- System status indicator

### Analysis Section
- Progress indicators
- Step-by-step feedback
- Real-time status updates

### Results Section
- Executive summary (highlighted)
- Key metrics (3 columns)
- Risks & opportunities (side-by-side)
- Strategic actions (expandable)
- Download button for JSON export

## 💡 Tips

1. **File Size**: Keep Excel files under 10MB for best performance
2. **Data Quality**: Clean data = better insights
3. **Sheet Names**: Use descriptive names (P&L, Cashflow, KPI)
4. **Patience**: AI analysis takes 1-2 minutes - be patient!
5. **Download**: Save your analysis for future reference

## 🔄 Workflow

```
Upload Excel → Process Data → Clean & Transform → AI Analysis → Display Results
```

**Simple, fast, powerful!**

## 📞 Support

If you encounter issues:
1. Check Ollama is running
2. Verify model is installed: `ollama list`
3. Try with a smaller file first
4. Check terminal logs for errors

---

**Built with ❤️ using Streamlit, Pandas, and AI**
