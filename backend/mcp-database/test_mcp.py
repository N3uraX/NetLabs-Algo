#!/usr/bin/env python3
"""
Test script to verify MCP Database Server functionality
Run this to ensure everything is working before Cursor integration
"""

import asyncio
import json
import sys

# Import MCP client components
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Keep the stderr reader for server-side logs
async def read_stderr_continuously(process_stderr, stop_event):
    """Read from stderr stream and print lines until stop_event is set."""
    while not stop_event.is_set():
        try:
            line = await asyncio.wait_for(process_stderr.readline(), timeout=0.1)
            if line:
                print(f"[SERVER STDERR]: {line.decode(errors='ignore').strip()}", flush=True)
            else:
                if not process_stderr.at_eof():
                    await asyncio.sleep(0.05)
                else:
                    print("[SERVER STDERR]: EOF reached.", flush=True)
                    break 
        except asyncio.TimeoutError:
            pass
        except Exception as e_stderr_read:
            print(f"[SERVER STDERR]: Error reading: {type(e_stderr_read).__name__}: {e_stderr_read}", flush=True)
            break
    print("[SERVER STDERR]: Exiting continuous stderr reader task.", flush=True)


async def test_mcp_server_with_sdk_client():
    """Test MCP server functionality using the MCP client SDK."""
    print("🧪 Testing MCP Database Server with SDK Client...")
    
    # StdioServerParameters takes the command to run the server
    # It will manage the subprocess internally.
    server_params = StdioServerParameters(
        command=sys.executable, # Path to Python interpreter
        args=['server.py'],      # Script to run
        cwd='backend/mcp-database' # Working directory for the server script
    )

    # We still want to capture server.py's direct stderr if stdio_client doesn't expose it easily
    # However, stdio_client manages the subprocess, so direct stderr capture needs care.
    # For now, let's rely on server.py printing to its stderr and hope it appears on console
    # if stdio_client itself doesn't redirect/capture it in a hidden way.
    # The previous read_stderr_continuously was for a manually managed process.
    # Simpler approach: The MCP client itself might log server stderr if configured or if errors occur.

    try:
        print(f"🚀 Launching server via StdioServerParameters: {server_params.command} {server_params.args}")
        # stdio_client handles starting and stopping the server subprocess
        async with stdio_client(server_params) as (read_stream, write_stream):
            print("🤝 MCP client transport connected (read/write streams acquired).")
            async with ClientSession(read_stream, write_stream) as session:
                print("📡 Initializing MCP session with server...")
                # Initialize the connection (sends initialize request and waits for response)
                init_response = await session.initialize()
                print(f"✅ MCP Session Initialized. Server capabilities: {init_response.capabilities}")

                print("📋 Requesting tools list from server...")
                tools_list_result = await session.list_tools()
                
                if tools_list_result and tools_list_result.tools:
                    tools = tools_list_result.tools
                    print(f"🛠️ MCP Server responded with {len(tools)} tools:")
                    for tool_info in tools[:5]: # Print up to 5 tools
                        print(f"  - Name: {tool_info.name}, Desc: {tool_info.description}")
                    if len(tools) > 5:
                        print("    ... and more.")
                    return True # Test successful
                else:
                    print("❌ Server returned no tools or an unexpected result for list_tools.")
                    return False

    except asyncio.TimeoutError as toe:
        print(f"❌ Test timed out: {toe}")
        return False
    except Exception as e:
        print(f"❌ Test failed with MCP client SDK error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("Test execution finished.")


if __name__ == "__main__":
    print("Attempting to run test_mcp_server_with_sdk_client from test_mcp.py...")
    # Ensure any prints from server.py (to its stderr) are visible if they happen before client connects
    # or if the client/SDK surfaces them.
    success = asyncio.run(test_mcp_server_with_sdk_client())
    if success:
        print("\n🎉 MCP Server (tested with SDK client) appears to be working!")
    else:
        print("\n❌ MCP Server test failed. Please check logs.") 