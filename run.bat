@echo off
title TechHub - Multi-Source Technical Q&A with Consensus Detection
echo ============================================================
echo   Starting TechHub Application
echo ============================================================
cd /d "%~dp0"

echo [1/2] Checking Python dependencies...
python -m pip install -r backend\requirements.txt --quiet

echo [2/2] Launching TechHub server...
start http://localhost:5000
python start_server.py
pause
