@echo off
echo ========================================
echo Simple Financial Analysis App
echo ========================================
echo.

echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Ollama is not running!
    echo Please start Ollama in another terminal:
    echo    ollama serve
    echo.
    pause
)

echo.
echo Starting Streamlit app...
echo.
echo The app will open in your browser at http://localhost:8501
echo.

streamlit run app_simple.py

pause
