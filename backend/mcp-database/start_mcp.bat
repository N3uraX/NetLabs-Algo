@echo off
echo 🚀 Starting MCP Database Server for Cybersecurity Platform...

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
)

REM Check and install required packages
python -c "import mcp, sqlalchemy, bcrypt, jwt" 2>nul
if errorlevel 1 (
    echo ❌ Missing required packages. Installing...
    pip install -r requirements.txt
)

REM Start the MCP server
echo 🔌 Starting MCP Database Server...
python server.py 