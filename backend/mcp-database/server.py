#!/usr/bin/env python3
"""
MCP Database Management Server for Cybersecurity Platform
Handles database creation, table management, migrations, and auth operations
"""

import sys
import logging
print("MCP Database Server script started (top of script).", flush=True, file=sys.stderr)
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence
import bcrypt
import jwt
import traceback
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic import command
from alembic.config import Config
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# --- Enhanced Logging Setup ---
logger = logging.getLogger(__name__)
LOG_FILE_NAME = "mcp_server.log"
log_file_path_calculated = "NOT_CALCULATED_YET"

try:
    # Determine current working directory and script directory for clarity
    cwd = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to place log file in the script's directory first
    log_file_path_calculated = os.path.join(script_dir, LOG_FILE_NAME)
    
    print(f"MCP Script CWD: {cwd}", flush=True, file=sys.stderr)
    print(f"MCP Script Dir: {script_dir}", flush=True, file=sys.stderr)
    print(f"Attempting to configure logging to: {log_file_path_calculated}", flush=True, file=sys.stderr)

    logging.basicConfig(
        filename=log_file_path_calculated,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        filemode="w"
    )
    logger.info("--- MCP Database Server script started and file logger configured. ---")
    # Test if file was actually created by trying to append
    with open(log_file_path_calculated, "a") as f:
        f.write("Test log entry from direct open.\\n")
    logger.info(f"Successfully wrote test entry to {log_file_path_calculated}")

except Exception as e_log_setup:
    print(f"CRITICAL_ERROR_CONFIGURING_LOGGING to {log_file_path_calculated}: {type(e_log_setup).__name__} - {e_log_setup}", flush=True, file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    # Fallback to basic console logging if file logging fails
    logging.basicConfig(
        level=logging.DEBUG,
        format="CONSOLE_LOG_FALLBACK: %(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    logger.error(f"File logging failed. Switched to console logging. Error: {e_log_setup}")
# --- End Enhanced Logging Setup ---

# Database Models Base
Base = declarative_base()

class DatabaseMCPServer:
    """MCP Server for database operations in the cybersecurity platform"""
    
    def __init__(self):
        logger.info("DatabaseMCPServer.__init__ called.")
        self.server = Server("cybersec-database")
        logger.info(f"MCP Server instance created for '{self.server.name}'.")
        self.engine = None
        self.async_engine = None
        self.session_factory = None
        self.async_session_factory = None
        self.metadata = MetaData()
        
        # JWT Configuration
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
        self.jwt_algorithm = "HS256"
        self.jwt_expiration_hours = 24
        
        self._setup_handlers()
        logger.info("DatabaseMCPServer handlers setup.")
    
    def _setup_handlers(self):
        """Setup MCP handlers for database operations"""
        logger.info("DatabaseMCPServer._setup_handlers called.")
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available database resources"""
            return [
                Resource(
                    uri="database://connection",
                    name="Database Connection",
                    description="Current database connection status and info",
                    mimeType="application/json",
                ),
                Resource(
                    uri="database://schema",
                    name="Database Schema",
                    description="Current database schema and tables",
                    mimeType="application/json",
                ),
                Resource(
                    uri="database://migrations",
                    name="Migration Status",
                    description="Database migration history and status",
                    mimeType="application/json",
                ),
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read database resource information"""
            logger.info(f"handle_read_resource called for URI: {uri}")
            if uri == "database://connection":
                return await self._get_connection_info()
            elif uri == "database://schema":
                return await self._get_schema_info()
            elif uri == "database://migrations":
                return await self._get_migration_status()
            else:
                logger.error(f"Unknown resource URI: {uri}")
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            print("server.py: handle_list_tools called", flush=True, file=sys.stderr)
            logger.info("handle_list_tools called.")
            """List available database tools"""
            return [
                Tool(
                    name="connect_database",
                    description="Connect to PostgreSQL database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database_url": {"type": "string", "description": "Database connection URL"},
                            "async_url": {"type": "string", "description": "Async database connection URL (optional)"}
                        },
                        "required": ["database_url"]
                    },
                ),
                Tool(
                    name="create_tables",
                    description="Create cybersecurity platform database tables",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_sample_data": {"type": "boolean", "default": False, "description": "Include sample data for testing"}
                        }
                    },
                ),
                Tool(
                    name="run_migrations",
                    description="Run database migrations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "direction": {"type": "string", "enum": ["upgrade", "downgrade"], "default": "upgrade"},
                            "revision": {"type": "string", "description": "Target revision (optional)"}
                        }
                    },
                ),
                Tool(
                    name="create_user",
                    description="Create a new user with hashed password",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email": {"type": "string", "format": "email"},
                            "password": {"type": "string", "minLength": 8},
                            "full_name": {"type": "string"},
                            "role": {"type": "string", "enum": ["admin", "analyst", "viewer"], "default": "analyst"},
                            "is_active": {"type": "boolean", "default": True}
                        },
                        "required": ["email", "password", "full_name"]
                    },
                ),
                Tool(
                    name="authenticate_user",
                    description="Authenticate user and generate JWT token",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email": {"type": "string", "format": "email"},
                            "password": {"type": "string"}
                        },
                        "required": ["email", "password"]
                    },
                ),
                Tool(
                    name="verify_token",
                    description="Verify JWT token and return user info",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "token": {"type": "string"}
                        },
                        "required": ["token"]
                    },
                ),
                Tool(
                    name="execute_query",
                    description="Execute raw SQL query (use with caution)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "SQL query to execute"},
                            "params": {"type": "object", "description": "Query parameters (optional)"}
                        },
                        "required": ["query"]
                    },
                ),
                Tool(
                    name="get_table_info",
                    description="Get information about database tables",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {"type": "string", "description": "Specific table name (optional)"}
                        }
                    },
                ),
                Tool(
                    name="backup_database",
                    description="Create database backup",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "backup_path": {"type": "string", "description": "Path to store backup file"}
                        }
                    },
                ),
                Tool(
                    name="seed_sample_data",
                    description="Insert sample data for development/testing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_type": {"type": "string", "enum": ["minimal", "full"], "default": "minimal"}
                        }
                    },
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls"""
            logger.info(f"handle_call_tool called for tool: {name} with args: {arguments}")
            try:
                if name == "connect_database":
                    result = await self._connect_database(arguments)
                elif name == "create_tables":
                    result = await self._create_tables(arguments)
                elif name == "run_migrations":
                    result = await self._run_migrations(arguments)
                elif name == "create_user":
                    result = await self._create_user(arguments)
                elif name == "authenticate_user":
                    result = await self._authenticate_user(arguments)
                elif name == "verify_token":
                    result = await self._verify_token(arguments)
                elif name == "execute_query":
                    result = await self._execute_query(arguments)
                elif name == "get_table_info":
                    result = await self._get_table_info(arguments)
                elif name == "backup_database":
                    result = await self._backup_database(arguments)
                elif name == "seed_sample_data":
                    result = await self._seed_sample_data(arguments)
                else:
                    logger.error(f"Unknown tool called: {name}")
                    raise ValueError(f"Unknown tool: {name}")
                
                logger.info(f"Tool {name} executed successfully. Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
                
            except Exception as e:
                logger.exception(f"Error calling tool {name}: {e}")
                error_result = {"error": str(e), "tool": name, "arguments": arguments}
                return [TextContent(type="text", text=json.dumps(error_result, indent=2))]
    
    async def _connect_database(self, args: dict) -> dict:
        """Connect to the database"""
        database_url = args["database_url"]
        async_url = args.get("async_url")
        
        try:
            # Sync engine
            self.engine = create_engine(database_url)
            
            # Async engine
            if async_url:
                self.async_engine = create_async_engine(async_url)
            else:
                # Convert sync URL to async URL
                async_database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
                self.async_engine = create_async_engine(async_database_url)
            
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
            
            # Create session factories
            self.session_factory = sessionmaker(bind=self.engine)
            self.async_session_factory = sessionmaker(
                bind=self.async_engine, 
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            return {
                "status": "success",
                "message": "Successfully connected to database",
                "database_version": version,
                "connection_url": database_url.split("@")[1] if "@" in database_url else "hidden"
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to connect: {str(e)}"}
    
    async def _create_tables(self, args: dict) -> dict:
        """Create cybersecurity platform tables"""
        include_sample_data = args.get("include_sample_data", False)
        
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            # Define cybersecurity platform tables
            tables_created = []
            
            # Users table
            users_table = Table(
                'users', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('email', String(255), unique=True, nullable=False),
                Column('password_hash', String(255), nullable=False),
                Column('full_name', String(255), nullable=False),
                Column('role', String(50), nullable=False, default='analyst'),
                Column('is_active', Boolean, default=True),
                Column('created_at', DateTime, default=datetime.utcnow),
                Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
            )
            
            # Organizations table
            organizations_table = Table(
                'organizations', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(255), nullable=False),
                Column('domain', String(255)),
                Column('created_at', DateTime, default=datetime.utcnow),
            )
            
            # Assets table
            assets_table = Table(
                'assets', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(255), nullable=False),
                Column('asset_type', String(100), nullable=False),
                Column('ip_address', String(45)),
                Column('mac_address', String(17)),
                Column('os_info', String(255)),
                Column('criticality', String(20), default='medium'),
                Column('organization_id', Integer, ForeignKey('organizations.id')),
                Column('is_active', Boolean, default=True),
                Column('last_seen', DateTime),
                Column('created_at', DateTime, default=datetime.utcnow),
            )
            
            # Threats table
            threats_table = Table(
                'threats', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('threat_type', String(100), nullable=False),
                Column('severity', String(20), nullable=False),
                Column('status', String(50), default='active'),
                Column('source_ip', String(45)),
                Column('target_ip', String(45)),
                Column('description', Text),
                Column('ioc_data', Text),  # JSON field for IOCs
                Column('detected_at', DateTime, default=datetime.utcnow),
                Column('resolved_at', DateTime),
            )
            
            # Vulnerabilities table
            vulnerabilities_table = Table(
                'vulnerabilities', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('cve_id', String(20)),
                Column('title', String(500), nullable=False),
                Column('severity', String(20), nullable=False),
                Column('cvss_score', String(10)),
                Column('description', Text),
                Column('asset_id', Integer, ForeignKey('assets.id')),
                Column('status', String(50), default='open'),
                Column('discovered_at', DateTime, default=datetime.utcnow),
                Column('patched_at', DateTime),
            )
            
            # Security Events table
            security_events_table = Table(
                'security_events', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('event_type', String(100), nullable=False),
                Column('severity', String(20), nullable=False),
                Column('source', String(255)),
                Column('message', Text),
                Column('event_data', Text),  # JSON field
                Column('asset_id', Integer, ForeignKey('assets.id')),
                Column('timestamp', DateTime, default=datetime.utcnow),
            )
            
            # Network Monitoring table
            network_monitoring_table = Table(
                'network_monitoring', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('device_ip', String(45), nullable=False),
                Column('device_type', String(100)),
                Column('status', String(20), default='online'),
                Column('cpu_usage', Integer),
                Column('memory_usage', Integer),
                Column('bandwidth_in', Integer),
                Column('bandwidth_out', Integer),
                Column('timestamp', DateTime, default=datetime.utcnow),
            )
            
            # Create all tables
            self.metadata.create_all(self.engine)
            
            tables_created = [
                'users', 'organizations', 'assets', 'threats', 
                'vulnerabilities', 'security_events', 'network_monitoring'
            ]
            
            result = {
                "status": "success",
                "message": "Database tables created successfully",
                "tables_created": tables_created
            }
            
            if include_sample_data:
                sample_result = await self._seed_sample_data({"data_type": "minimal"})
                result["sample_data"] = sample_result
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create tables: {str(e)}"}
    
    async def _create_user(self, args: dict) -> dict:
        """Create a new user with hashed password"""
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            email = args["email"]
            password = args["password"]
            full_name = args["full_name"]
            role = args.get("role", "analyst")
            is_active = args.get("is_active", True)
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                        INSERT INTO users (email, password_hash, full_name, role, is_active)
                        VALUES (:email, :password_hash, :full_name, :role, :is_active)
                        RETURNING id, email, full_name, role, is_active, created_at
                    """),
                    {
                        "email": email,
                        "password_hash": password_hash,
                        "full_name": full_name,
                        "role": role,
                        "is_active": is_active
                    }
                )
                conn.commit()
                user_data = result.fetchone()
            
            return {
                "status": "success",
                "message": "User created successfully",
                "user": {
                    "id": user_data[0],
                    "email": user_data[1],
                    "full_name": user_data[2],
                    "role": user_data[3],
                    "is_active": user_data[4],
                    "created_at": user_data[5]
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create user: {str(e)}"}
    
    async def _authenticate_user(self, args: dict) -> dict:
        """Authenticate user and generate JWT token"""
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            email = args["email"]
            password = args["password"]
            
            # Get user from database
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT id, email, password_hash, full_name, role, is_active FROM users WHERE email = :email"),
                    {"email": email}
                )
                user_data = result.fetchone()
            
            if not user_data:
                return {"status": "error", "message": "User not found"}
            
            if not user_data[5]:  # is_active
                return {"status": "error", "message": "User account is inactive"}
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
                return {"status": "error", "message": "Invalid password"}
            
            # Generate JWT token
            payload = {
                "user_id": user_data[0],
                "email": user_data[1],
                "role": user_data[4],
                "exp": datetime.utcnow() + timedelta(hours=self.jwt_expiration_hours)
            }
            
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            
            return {
                "status": "success",
                "message": "Authentication successful",
                "token": token,
                "user": {
                    "id": user_data[0],
                    "email": user_data[1],
                    "full_name": user_data[3],
                    "role": user_data[4]
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Authentication failed: {str(e)}"}
    
    async def _verify_token(self, args: dict) -> dict:
        """Verify JWT token and return user info"""
        try:
            token = args["token"]
            
            # Decode token
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            return {
                "status": "success",
                "message": "Token is valid",
                "user": {
                    "id": payload["user_id"],
                    "email": payload["email"],
                    "role": payload["role"]
                }
            }
            
        except jwt.ExpiredSignatureError:
            return {"status": "error", "message": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"status": "error", "message": "Invalid token"}
        except Exception as e:
            return {"status": "error", "message": f"Token verification failed: {str(e)}"}
    
    async def _execute_query(self, args: dict) -> dict:
        """Execute raw SQL query"""
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            query = args["query"]
            params = args.get("params", {})
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                
                if result.returns_rows:
                    rows = result.fetchall()
                    columns = list(result.keys())
                    data = [dict(zip(columns, row)) for row in rows]
                    
                    return {
                        "status": "success",
                        "message": f"Query executed successfully, {len(data)} rows returned",
                        "data": data,
                        "columns": columns
                    }
                else:
                    conn.commit()
                    return {
                        "status": "success",
                        "message": f"Query executed successfully, {result.rowcount} rows affected"
                    }
                    
        except Exception as e:
            return {"status": "error", "message": f"Query execution failed: {str(e)}"}
    
    async def _get_table_info(self, args: dict) -> dict:
        """Get information about database tables"""
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            table_name = args.get("table_name")
            inspector = inspect(self.engine)
            
            if table_name:
                # Get info for specific table
                if table_name not in inspector.get_table_names():
                    return {"status": "error", "message": f"Table '{table_name}' not found"}
                
                columns = inspector.get_columns(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)
                indexes = inspector.get_indexes(table_name)
                
                return {
                    "status": "success",
                    "table": table_name,
                    "columns": columns,
                    "foreign_keys": foreign_keys,
                    "indexes": indexes
                }
            else:
                # Get info for all tables
                table_names = inspector.get_table_names()
                tables_info = {}
                
                for table in table_names:
                    columns = inspector.get_columns(table)
                    tables_info[table] = {
                        "columns": len(columns),
                        "column_names": [col["name"] for col in columns]
                    }
                
                return {
                    "status": "success",
                    "message": f"Found {len(table_names)} tables",
                    "tables": tables_info
                }
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to get table info: {str(e)}"}
    
    async def _seed_sample_data(self, args: dict) -> dict:
        """Insert sample data for development/testing"""
        if not self.engine:
            return {"status": "error", "message": "Database not connected"}
        
        try:
            data_type = args.get("data_type", "minimal")
            
            with self.engine.connect() as conn:
                # Insert sample organization
                org_result = conn.execute(
                    text("INSERT INTO organizations (name, domain) VALUES (:name, :domain) RETURNING id"),
                    {"name": "Sample Corp", "domain": "samplecorp.com"}
                )
                org_id = org_result.fetchone()[0]
                
                # Insert sample assets
                assets_data = [
                    ("Web Server", "server", "192.168.1.100", "00:1B:44:11:3A:B7", "Ubuntu 20.04", "high"),
                    ("Database Server", "server", "192.168.1.101", "00:1B:44:11:3A:B8", "CentOS 8", "critical"),
                    ("Workstation", "desktop", "192.168.1.50", "00:1B:44:11:3A:B9", "Windows 10", "medium"),
                ]
                
                for asset in assets_data:
                    conn.execute(
                        text("""INSERT INTO assets (name, asset_type, ip_address, mac_address, os_info, criticality, organization_id)
                               VALUES (:name, :type, :ip, :mac, :os, :crit, :org_id)"""),
                        {"name": asset[0], "type": asset[1], "ip": asset[2], "mac": asset[3], "os": asset[4], "crit": asset[5], "org_id": org_id}
                    )
                
                # Insert sample threats
                threats_data = [
                    ("malware", "high", "active", "10.0.0.5", "192.168.1.100", "Suspicious executable detected"),
                    ("intrusion", "critical", "active", "203.0.113.5", "192.168.1.101", "Unauthorized access attempt"),
                    ("phishing", "medium", "resolved", "198.51.100.3", "192.168.1.50", "Phishing email detected"),
                ]
                
                for threat in threats_data:
                    conn.execute(
                        text("""INSERT INTO threats (threat_type, severity, status, source_ip, target_ip, description)
                               VALUES (:type, :severity, :status, :src_ip, :tgt_ip, :desc)"""),
                        {"type": threat[0], "severity": threat[1], "status": threat[2], "src_ip": threat[3], "tgt_ip": threat[4], "desc": threat[5]}
                    )
                
                # Insert sample security events
                events_data = [
                    ("login_failure", "medium", "auth", "Failed login attempt from suspicious IP"),
                    ("file_access", "low", "system", "Unusual file access pattern detected"),
                    ("network_scan", "high", "network", "Port scan detected from external source"),
                ]
                
                for event in events_data:
                    conn.execute(
                        text("""INSERT INTO security_events (event_type, severity, source, message)
                               VALUES (:type, :severity, :source, :message)"""),
                        {"type": event[0], "severity": event[1], "source": event[2], "message": event[3]}
                    )
                
                conn.commit()
            
            return {
                "status": "success",
                "message": f"Sample data ({data_type}) inserted successfully",
                "data_inserted": {
                    "organizations": 1,
                    "assets": 3,
                    "threats": 3,
                    "security_events": 3
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to seed sample data: {str(e)}"}
    
    async def _get_connection_info(self) -> str:
        """Get database connection information"""
        if not self.engine:
            return json.dumps({"status": "disconnected", "message": "No database connection"})
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version(), current_database(), current_user"))
                version, database, user = result.fetchone()
            
            return json.dumps({
                "status": "connected",
                "database_version": version,
                "current_database": database,
                "current_user": user,
                "engine_info": str(self.engine.url).replace(self.engine.url.password or "", "***")
            }, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
    
    async def _get_schema_info(self) -> str:
        """Get database schema information"""
        if not self.engine:
            return json.dumps({"status": "error", "message": "Database not connected"})
        
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            schema_info = {"tables": {}}
            for table in tables:
                columns = inspector.get_columns(table)
                schema_info["tables"][table] = {
                    "columns": [{"name": col["name"], "type": str(col["type"]), "nullable": col["nullable"]} for col in columns]
                }
            
            return json.dumps(schema_info, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
    
    async def _get_migration_status(self) -> str:
        """Get migration status (placeholder for Alembic integration)"""
        return json.dumps({
            "status": "info",
            "message": "Migration system not yet configured",
            "suggestion": "Set up Alembic for proper migration management"
        })
    
    async def _run_migrations(self, args: dict) -> dict:
        """Run database migrations (placeholder)"""
        return {
            "status": "info",
            "message": "Migration system not yet configured",
            "suggestion": "Set up Alembic configuration and migration files"
        }
    
    async def _backup_database(self, args: dict) -> dict:
        """Create database backup (placeholder)"""
        return {
            "status": "info",
            "message": "Backup functionality not yet implemented",
            "suggestion": "Use pg_dump for PostgreSQL backups"
        }

async def main():
    """Run the MCP database server"""
    logger.info("main() function called.")

    server_instance = DatabaseMCPServer()
    logger.info("DatabaseMCPServer instance created in main().")

    options = NotificationOptions(show_information=True, show_warning=True, show_error=True)
    logger.info(f"NotificationOptions created: {options}")

    try:
        logger.info("Attempting to start server with stdio_server context manager...")
        async with server_instance.server.stdio_server(options=options) as server_protocol:
            logger.info(f"stdio_server context acquired. Protocol: {server_protocol}. About to call server_instance.server.run()...")
            await server_instance.server.run()
            logger.info("server_instance.server.run() completed.")
    except Exception as e:
        logger.critical(f"CRITICAL ERROR during server run: {e}", exc_info=True)
    finally:
        logger.info("main() function finished.")
        logging.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 