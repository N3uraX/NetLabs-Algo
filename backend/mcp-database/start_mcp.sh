#!/bin/bash
# MCP Database Server Startup Script

echo "🚀 Starting MCP Database Server for Cybersecurity Platform..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if required packages are installed
python -c "import mcp, sqlalchemy, bcrypt, jwt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing required packages. Installing..."
    pip install -r requirements.txt
fi

# Set environment variables if .env exists
if [ -f ".env" ]; then
    export $(cat .env | xargs)
    echo "✅ Environment variables loaded"
fi

# Start the MCP server
echo "🔌 Starting MCP Database Server..."
python server.py 