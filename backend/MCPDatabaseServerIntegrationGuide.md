# MCP Database Server Integration Guide

## Overview
This guide explains how to integrate the MCP Database Management Server into your cybersecurity platform project without disrupting existing development. The MCP server provides automated database operations, user authentication, and schema management for your cybersecurity platform.

## Project Structure

```
cybersecurity-platform/
├── frontend/                    # Your existing Vite + TypeScript frontend
├── backend/                     # Your main FastAPI backend
├── mcp-database/               # New MCP database server
│   ├── __init__.py
│   ├── server.py               # Main MCP server code
│   ├── requirements.txt        # Python dependencies
│   ├── alembic.ini            # Database migration config (optional)
│   └── migrations/            # Database migration files (optional)
├── docker-compose.yml          # Updated with MCP service
└── README.md
```

## Installation Steps

### 1. Create MCP Database Directory
```bash
mkdir mcp-database
cd mcp-database
```

### 2. Create Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Create `requirements.txt`:
```txt
mcp==1.0.0
sqlalchemy>=2.0.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.0
bcrypt>=4.0.0
PyJWT>=2.8.0
alembic>=1.13.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Add the MCP Server Code
Create `server.py` and paste the provided MCP database server code.

### 5. Create Initialization File
Create `__init__.py`:
```python
"""MCP Database Management Server for Cybersecurity Platform"""
from .server import DatabaseMCPServer

__version__ = "1.0.0"
__all__ = ["DatabaseMCPServer"]
```

## Configuration

### 1. Environment Variables
Create `.env` file in the `mcp-database/` directory:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/cybersec_db
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/cybersec_db

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# MCP Server Configuration
MCP_SERVER_NAME=cybersec-database
MCP_SERVER_VERSION=1.0.0
```

### 2. Update Docker Compose (Optional)
Add MCP service to your existing `docker-compose.yml`:
```yaml
services:
  # Your existing services...
  
  mcp-database:
    build: 
      context: ./mcp-database
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/cybersec_db
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - postgres
    volumes:
      - ./mcp-database:/app
    stdin_open: true
    tty: true
```

Create `mcp-database/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]
```

## Integration with Your Backend

### 1. Backend API Integration
In your FastAPI backend, create an MCP client to communicate with the database server:

Create `backend/mcp_client.py`:
```python
import asyncio
import json
from typing import Dict, Any, Optional

class MCPDatabaseClient:
    """Client to communicate with MCP Database Server"""
    
    def __init__(self):
        self.process = None
        self.reader = None
        self.writer = None
    
    async def connect(self):
        """Connect to MCP database server"""
        self.process = await asyncio.create_subprocess_exec(
            'python', '../mcp-database/server.py',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.reader = self.process.stdout
        self.writer = self.process.stdin
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool and return result"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Send request
        request_json = json.dumps(request) + '\n'
        self.writer.write(request_json.encode())
        await self.writer.drain()
        
        # Read response
        response_line = await self.reader.readline()
        response = json.loads(response_line.decode())
        
        return response.get('result', {})
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        if self.process:
            await self.process.wait()

# Global MCP client instance
mcp_client = MCPDatabaseClient()
```

### 2. Update FastAPI Dependencies
In your `backend/main.py` or `backend/dependencies.py`:
```python
from .mcp_client import mcp_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mcp_client.connect()
    yield
    # Shutdown
    await mcp_client.disconnect()

# Update your FastAPI app
app = FastAPI(lifespan=lifespan)
```

### 3. Database Operations via MCP
Replace direct database calls with MCP tool calls:

```python
# Example: User creation endpoint
@app.post("/auth/register")
async def register_user(user_data: UserCreate):
    result = await mcp_client.call_tool("create_user", {
        "email": user_data.email,
        "password": user_data.password,
        "full_name": user_data.full_name,
        "role": user_data.role
    })
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

# Example: User authentication endpoint
@app.post("/auth/login")
async def login_user(credentials: UserLogin):
    result = await mcp_client.call_tool("authenticate_user", {
        "email": credentials.email,
        "password": credentials.password
    })
    
    if result.get("status") == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    
    return {"access_token": result["token"], "user": result["user"]}
```

## Database Schema Management

### 1. Initialize Database
```python
# Run this once to set up your database
await mcp_client.call_tool("connect_database", {
    "database_url": "postgresql://user:pass@localhost:5432/cybersec_db"
})

await mcp_client.call_tool("create_tables", {
    "include_sample_data": True  # For development
})
```

### 2. Available Database Tables
The MCP server creates these cybersecurity-specific tables:
- `users` - User accounts and authentication
- `organizations` - Client organizations
- `assets` - IT assets and devices
- `threats` - Security threats and incidents
- `vulnerabilities` - Vulnerability management
- `security_events` - Security event logs
- `network_monitoring` - Network device monitoring

## Available MCP Tools

### Database Management
- `connect_database` - Connect to PostgreSQL database
- `create_tables` - Create cybersecurity platform tables
- `get_table_info` - Get database schema information
- `execute_query` - Execute raw SQL queries
- `seed_sample_data` - Insert sample data for testing

### User Management
- `create_user` - Create new user with hashed password
- `authenticate_user` - Login and generate JWT token
- `verify_token` - Validate JWT tokens

### Operations
- `backup_database` - Create database backups (placeholder)
- `run_migrations` - Run database migrations (placeholder)

## Frontend Integration

### 1. Update API Calls
Your frontend API calls remain the same since the MCP server works behind the scenes through your FastAPI backend.

### 2. Authentication Flow
```typescript
// frontend/src/services/auth.ts
export const authService = {
  async login(email: string, password: string) {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
    }
    return data;
  },
  
  async register(userData: RegisterData) {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  }
};
```

## Running the System

### 1. Start MCP Database Server
```bash
cd mcp-database
python server.py
```

### 2. Start Your Backend
```bash
cd backend
uvicorn main:app --reload
```

### 3. Start Your Frontend
```bash
cd frontend
npm run dev
```

## Development Workflow

### 1. Database Operations
Use MCP tools through your backend instead of direct SQL:
```python
# Instead of direct SQLAlchemy
# user = User(email=email, password_hash=hash_password(password))
# db.add(user)
# db.commit()

# Use MCP tool
result = await mcp_client.call_tool("create_user", user_data)
```

### 2. Schema Changes
Modify the `_create_tables` method in the MCP server to add new tables or columns, then recreate tables.

### 3. Testing
```python
# Seed test data
await mcp_client.call_tool("seed_sample_data", {"data_type": "full"})

# Query data
result = await mcp_client.call_tool("execute_query", {
    "query": "SELECT * FROM threats WHERE severity = :severity",
    "params": {"severity": "high"}
})
```

## Security Considerations

1. **JWT Secret**: Use a strong, unique JWT secret in production
2. **Database Credentials**: Use environment variables for database credentials
3. **Input Validation**: The MCP server includes basic validation, but add additional validation in your FastAPI endpoints
4. **Network Security**: Run MCP server on localhost or secure network
5. **Password Hashing**: The server uses bcrypt for secure password hashing

## Benefits of This Integration

1. **Separation of Concerns**: Database operations are handled by a dedicated service
2. **Consistent Schema**: Predefined cybersecurity-focused database schema
3. **Built-in Security**: JWT authentication and password hashing included
4. **Easy Management**: Tools for database setup, user management, and operations
5. **Development Ready**: Sample data seeding for testing
6. **Future-Proof**: Easy to extend with additional database operations

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check database URL and credentials
2. **Tool Call Errors**: Verify MCP server is running and accessible
3. **Authentication Issues**: Check JWT secret configuration
4. **Table Creation Fails**: Ensure database exists and user has permissions

### Debug Mode
Set environment variable for detailed logging:
```bash
export MCP_DEBUG=true
python server.py
```

## Next Steps

1. Test the integration with your existing codebase
2. Migrate existing database operations to use MCP tools
3. Set up proper migration system with Alembic
4. Configure backup and monitoring
5. Add additional cybersecurity-specific tools as needed

This integration provides a robust, automated database management system specifically designed for cybersecurity platforms while maintaining compatibility with your existing development workflow.