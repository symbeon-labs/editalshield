"""DocSync command line interface."""

import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from . import __version__

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """DocSync - Documentation synchronization and management system."""


@cli.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="YAML configuration file",
)
def sync(path: Path, config: Optional[Path] = None) -> None:
    """Synchronize documentation directory."""
    try:
        import asyncio
        from docsync.core import DocSync
        
        console.print(f"🔄 Initializing DocSync for [bold]{path}[/bold]...", style="blue")
        doc_sync = DocSync(path, config_path=config)
        
        console.print(f"DEBUG: DocSync attributes: {dir(doc_sync)}")
        console.print("🚀 Starting synchronization...", style="blue")
        asyncio.run(doc_sync.sync_manager.start())
        
        console.print("✨ Synchronization completed!", style="green")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort


@cli.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openai", "claude", "gemini"]),
    default="openai",
    help="LLM provider to use (default: openai)",
)
@click.option(
    "--model",
    "-m",
    default=None,
    help="LLM model to use (provider-specific defaults if not specified)",
)
def improve(path: Path, provider: str, model: Optional[str]) -> None:
    """Improve documentation using AI."""
    try:
        console.print(f"🤖 Analyzing [bold]{path.name}[/bold] with {provider}...", style="blue")
        
        # Initialize provider
        try:
            if provider == "openai":
                from docsync.integrations.openai_provider import OpenAIProvider
                llm = OpenAIProvider(model=model or "gpt-4o-mini")
            elif provider == "claude":
                from docsync.integrations.claude_provider import ClaudeProvider
                llm = ClaudeProvider(model=model or "claude-3-5-haiku-20241022")
            elif provider == "gemini":
                from docsync.integrations.gemini_provider import GeminiProvider
                llm = GeminiProvider(model=model or "gemini-2.0-flash-exp")
        except ValueError as e:
            console.print(f"❌ Configuration Error: {e}", style="red")
            console.print(f"💡 Tip: Set {provider.upper()}_API_KEY environment variable.", style="yellow")
            return

        # Read file
        content = path.read_text(encoding="utf-8")
        
        # Generate improvement suggestions
        system_prompt = (
            "You are an expert technical writer and software engineer. "
            "Analyze the following documentation and provide specific, actionable improvements. "
            "Focus on clarity, completeness, and examples. "
            "Return the response in Markdown format."
        )
        
        response = llm.generate(content, system_prompt=system_prompt)
        
        # Display results
        console.print("\n✨ AI Suggestions:\n", style="green")
        console.print(response.content)
        
        # Show usage stats
        if response.usage:
            tokens = response.usage.get("total_tokens", 0)
            console.print(f"\n📊 Tokens used: {tokens}", style="dim")

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort


@cli.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=".",
)
def serve(path: Path) -> None:
    """Start MCP server."""
    import asyncio
    from docsync.mcp.server import serve as run_server

    try:
        console.print(f"🔌 Starting MCP server for [bold]{path.resolve()}[/bold]...", style="blue")
        asyncio.run(run_server(path))
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort


def main() -> None:
    """Main entry point."""
    try:
        cli()
    except Exception as e:
        console.print(f"❌ Fatal error: {e}", style="red")
        raise click.Abort
