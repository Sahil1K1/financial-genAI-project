@echo off
echo ========================================
echo Financial Analysis Dashboard Launcher
echo ========================================
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 1: Check Ollama
echo ========================================
echo.
echo Please make sure Ollama is running in another terminal:
echo    ollama serve
echo.
pause

echo.
echo ========================================
echo STEP 2: Starting FastAPI Backend...
echo ========================================
echo.
echo Starting API server on http://localhost:8000
echo API Docs will be available at http://localhost:8000/docs
echo.

start "FastAPI Backend" cmd /k "cd /d %~dp0 && python -m src.app"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo STEP 3: Starting Streamlit Dashboard...
echo ========================================
echo.
echo Dashboard will open in your browser at http://localhost:8501
echo.

timeout /t 3 /nobreak >nul

streamlit run streamlit_app.py

echo.
echo ========================================
echo Dashboard Closed
echo ========================================
pause
