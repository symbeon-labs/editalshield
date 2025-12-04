"""EditalShield CLI - Command Line Interface.

Provides command-line tools for EditalShield framework.
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """EditalShield - Framework para proteção de PI em editais brasileiros."""
    pass


@cli.group()
def docs():
    """Comandos para gerenciamento de documentação."""
    pass


@docs.command()
@click.option('--path', '-p', type=click.Path(exists=True), default='.',
              help='Caminho do projeto')
def sync(path):
    """Sincroniza e valida documentação do projeto."""
    from editalshield.docs_manager import sync_documentation
    
    console.print("🔄 Sincronizando documentação...", style="blue")
    
    stats = sync_documentation(Path(path))
    
    table = Table(title="Resultado da Sincronização")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="green")
    
    table.add_row("Arquivos encontrados", str(stats["files_found"]))
    table.add_row("Arquivos validados", str(stats["files_validated"]))
    table.add_row("Erros", str(stats["errors"]))
    
    console.print(table)
    console.print("✨ Sincronização concluída!", style="green")


@docs.command()
@click.option('--path', '-p', type=click.Path(exists=True), default='.',
              help='Caminho do projeto')
def validate(path):
    """Valida estrutura de documentação."""
    from editalshield.docs_manager import validate_documentation
    
    console.print("🔍 Validando estrutura...", style="blue")
    
    results = validate_documentation(Path(path))
    
    table = Table(title="Validação de Estrutura")
    table.add_column("Item", style="cyan")
    table.add_column("Status", style="green")
    
    for key, value in results.items():
        status = "✅ OK" if value else "❌ Ausente"
        style = "green" if value else "red"
        table.add_row(key, status)
    
    console.print(table)
    
    all_valid = all(results.values())
    if all_valid:
        console.print("✨ Estrutura válida!", style="green")
    else:
        console.print("⚠️  Alguns itens estão ausentes", style="yellow")


@docs.command()
@click.option('--path', '-p', type=click.Path(exists=True), default='.',
              help='Caminho do projeto')
@click.option('--output', '-o', type=click.Path(), default='docs/INDEX.md',
              help='Arquivo de saída para o índice')
def index(path, output):
    """Gera índice de documentação."""
    from editalshield.docs_manager import generate_documentation_index
    
    console.print("📝 Gerando índice...", style="blue")
    
    index_content = generate_documentation_index(Path(path))
    
    output_path = Path(path) / output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(index_content, encoding="utf-8")
    
    console.print(f"✨ Índice gerado em: {output_path}", style="green")


if __name__ == "__main__":
    cli()
