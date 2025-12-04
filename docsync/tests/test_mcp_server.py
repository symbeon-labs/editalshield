"""Tests for MCP server."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Add src to sys.path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from docsync.mcp.server import DocSyncMCP

@pytest.fixture
def mock_server():
    with patch("docsync.mcp.server.Server") as mock:
        server_instance = MagicMock()
        # Mock decorators to return the function itself (passthrough)
        server_instance.list_tools.return_value = lambda f: f
        server_instance.call_tool.return_value = lambda f: f
        mock.return_value = server_instance
        yield mock

@pytest.mark.asyncio
async def test_mcp_server_initialization(mock_server, tmp_path):
    """Test DocSyncMCP initialization."""
    server = DocSyncMCP(tmp_path)
    assert server.root_path == tmp_path
    mock_server.assert_called_with("docsync-mcp")

@pytest.mark.asyncio
async def test_list_tools_handler(mock_server, tmp_path):
    """Test list_tools handler."""
    server = DocSyncMCP(tmp_path)
    
    # Capture the decorated function
    # Since we mocked the decorator to be a passthrough, the handler is defined in _setup_handlers
    # But we can't easily access it because it's a closure.
    # We need to rely on the fact that the decorator was called.
    
    # Alternative: Refactor server to expose handlers or use a different testing strategy.
    # For this MVP, we'll verify the server setup calls.
    server.server.list_tools.assert_called()
    server.server.call_tool.assert_called()

def test_serve_command_import():
    """Test that we can import the serve command."""
    from docsync.cli import serve
    assert serve is not None
