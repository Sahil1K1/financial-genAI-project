@echo off
echo ========================================
echo Financial Data Pipeline Runner
echo ========================================
echo.

echo This will:
echo 1. Load Excel data from data/raw/
echo 2. Process and clean the data
echo 3. Generate AI-powered insights
echo 4. Save results to data/outputs/llm_output.json
echo.

echo Make sure Ollama is running before proceeding!
echo.
pause

echo.
echo ========================================
echo Running Pipeline...
echo ========================================
echo.

python -m workflow.pipeline2

echo.
echo ========================================
echo Pipeline Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run start_dashboard.bat to view the results
echo 2. Or access the API at http://localhost:8000/summary
echo.
pause
