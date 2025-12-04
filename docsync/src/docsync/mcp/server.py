import sys
import logging
from pathlib import Path
from typing import Any, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, EmbeddedResource

# Add parent directory to sys.path to import ai_processor
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ai_processor import DocumentProcessor

from docsync.integrations.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)

class DocSyncMCP:
    """DocSync MCP Server."""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.processor = DocumentProcessor()
        self.server = Server("docsync-mcp")
        
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="list_docs",
                    description="List all markdown documentation files in the project.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="read_doc",
                    description="Read the content of a documentation file.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the document (e.g., 'README.md')",
                            }
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="improve_doc",
                    description="Analyze a document and get AI suggestions for improvement.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the document",
                            },
                            "provider": {
                                "type": "string",
                                "enum": ["openai", "claude", "gemini"],
                                "description": "LLM provider to use (default: openai)",
                                "default": "openai"
                            },
                            "model": {
                                "type": "string",
                                "description": "LLM model to use (provider-specific defaults)",
                                "default": None
                            }
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="get_stats",
                    description="Get project documentation statistics.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent | EmbeddedResource]:
            if name == "list_docs":
                files = list(self.root_path.glob("**/*.md"))
                rel_files = [str(f.relative_to(self.root_path)) for f in files]
                return [TextContent(type="text", text="\n".join(rel_files))]

            elif name == "read_doc":
                path = arguments["path"]
                full_path = self.root_path / path
                if not full_path.exists():
                    return [TextContent(type="text", text=f"Error: File {path} not found.")]
                return [TextContent(type="text", text=full_path.read_text(encoding="utf-8"))]

            elif name == "improve_doc":
                path = arguments["path"]
                provider_name = arguments.get("provider", "openai")
                model = arguments.get("model")
                full_path = self.root_path / path
                
                if not full_path.exists():
                    return [TextContent(type="text", text=f"Error: File {path} not found.")]

                try:
                    # Initialize the appropriate provider
                    if provider_name == "openai":
                        from docsync.integrations.openai_provider import OpenAIProvider
                        provider = OpenAIProvider(model=model or "gpt-4o-mini")
                    elif provider_name == "claude":
                        from docsync.integrations.claude_provider import ClaudeProvider
                        provider = ClaudeProvider(model=model or "claude-3-5-haiku-20241022")
                    elif provider_name == "gemini":
                        from docsync.integrations.gemini_provider import GeminiProvider
                        provider = GeminiProvider(model=model or "gemini-2.0-flash-exp")
                    else:
                        return [TextContent(type="text", text=f"Error: Unknown provider {provider_name}")]
                    
                    content = full_path.read_text(encoding="utf-8")
                    
                    system_prompt = (
                        "You are an expert technical writer. Analyze this document and provide "
                        "improvements. Return in Markdown."
                    )
                    
                    response = provider.generate(content, system_prompt=system_prompt)
                    return [TextContent(type="text", text=response.content)]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error: {str(e)}")]

            elif name == "get_stats":
                # Simple stats for now
                files = list(self.root_path.glob("**/*.md"))
                return [TextContent(type="text", text=f"Total documents: {len(files)}")]

            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def serve(root_path: Path):
    """Entry point for the server."""
    server = DocSyncMCP(root_path)
    await server.run()
