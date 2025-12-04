"""
EditalShield CLI - Command Line Interface
Main entry point for the EditalShield framework
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@click.group()
@click.version_option(version="0.2.0", prog_name="EditalShield")
def cli():
    """
    🛡️ EditalShield - Protect your IP in innovation grant submissions
    
    Framework for analyzing and protecting intellectual property
    in Brazilian innovation grant applications.
    """
    pass


# ============================================================================
# ANALYZE Command
# ============================================================================

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text',
              help='Output format')
@click.option('--output', '-o', type=click.Path(), default=None,
              help='Save report to file')
def analyze(file, format, output):
    """
    📊 Analyze a memorial for IP exposure risk
    
    Example: editalshield analyze memorial.txt
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] - Memorial Analysis",
        subtitle="🔍 Scanning for IP exposure..."
    ))
    
    try:
        from editalshield.modules.memorial_protector import MemorialProtector
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing memorial...", total=None)
            
            # Read file
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Analyze
            protector = MemorialProtector()
            analysis = protector.analyze_memorial(text)
            report = protector.generate_report(analysis, format)
            
            progress.remove_task(task)
        
        # Output
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            console.print(f"\n[green]✓ Report saved to: {output}[/green]")
        else:
            console.print(report)
        
        # Summary table
        table = Table(title="Analysis Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Paragraphs", str(analysis.total_paragraphs))
        table.add_row("Risk Score", f"{analysis.overall_risk_score}/100")
        table.add_row("High Risk", f"🔴 {analysis.high_risk_paragraphs}")
        table.add_row("Medium Risk", f"🟡 {analysis.medium_risk_paragraphs}")
        table.add_row("Low Risk", f"🟢 {analysis.low_risk_paragraphs}")
        
        console.print(table)
        
    except ImportError:
        console.print("[red]Error: Memorial Protector module not found[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# PROTECT Command
# ============================================================================

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default=None,
              help='Output file path')
@click.option('--report', '-r', is_flag=True, help='Also generate report')
def protect(file, output, report):
    """
    🛡️ Protect a memorial by replacing sensitive content
    
    Example: editalshield protect memorial.txt -o protected.txt
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] - Memorial Protection",
        subtitle="🛡️ Applying IP protection..."
    ))
    
    try:
        from editalshield.modules.memorial_protector import MemorialProtector
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Protecting memorial...", total=None)
            
            # Read file
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Protect
            protector = MemorialProtector()
            protected_text, analysis = protector.generate_protected_memorial(text)
            
            progress.remove_task(task)
        
        # Determine output path
        if output is None:
            input_path = Path(file)
            output = str(input_path.parent / f"{input_path.stem}_protected{input_path.suffix}")
        
        # Save protected version
        with open(output, 'w', encoding='utf-8') as f:
            f.write(protected_text)
        
        console.print(f"\n[green]✓ Protected memorial saved to: {output}[/green]")
        
        # Show stats
        console.print(f"\n📊 Protection Stats:")
        console.print(f"   Original risk: {analysis.overall_risk_score}/100")
        console.print(f"   Paragraphs modified: {analysis.high_risk_paragraphs + analysis.medium_risk_paragraphs}")
        
        if report:
            report_text = protector.generate_report(analysis)
            report_path = output.replace('.txt', '_report.txt').replace('.md', '_report.md')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            console.print(f"   Report saved to: {report_path}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# TRAIN Command
# ============================================================================

@cli.command()
@click.option('--data', '-d', type=click.Path(), default='data/synthetic_dataset.json',
              help='Training data path')
@click.option('--output', '-o', type=click.Path(), default='models/',
              help='Model output directory')
def train(data, output):
    """
    🧠 Train the Bayesian risk model
    
    Example: editalshield train --data data/synthetic_dataset.json
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] - Model Training",
        subtitle="🧠 Training Bayesian model..."
    ))
    
    try:
        import sys
        sys.path.insert(0, '.')
        from models.train_bayesian_model import BayesianModelTrainer
        
        trainer = BayesianModelTrainer(output_dir=output)
        
        console.print("\n[cyan]Loading training data...[/cyan]")
        df = trainer.load_training_data_from_json(data)
        
        if df.empty:
            console.print("[red]No data found. Generate data first.[/red]")
            return
        
        console.print("[cyan]Preparing features...[/cyan]")
        X, y, features = trainer.prepare_features(df)
        
        console.print("[cyan]Training model...[/cyan]")
        trainer.train(X, y)
        
        console.print("[cyan]Evaluating...[/cyan]")
        kfold = trainer.evaluate_kfold(X, y, k=5)
        full = trainer.evaluate_full(X, y)
        
        trainer.metrics = full
        trainer.save_model()
        trainer.save_report(full, kfold)
        
        console.print(f"\n[green]✓ Training complete![/green]")
        console.print(f"   AUC: {kfold['auc_mean']:.3f} ± {kfold['auc_std']:.3f}")
        console.print(f"   F1: {kfold['f1_mean']:.3f}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# GENERATE Command
# ============================================================================

@cli.command()
@click.option('--memorials', '-m', type=int, default=50, help='Number of memorials')
@click.option('--editals', '-e', type=int, default=80, help='Number of editals')
@click.option('--output', '-o', type=click.Path(), default='data/',
              help='Output directory')
def generate(memorials, editals, output):
    """
    📊 Generate synthetic training data
    
    Example: editalshield generate --memorials 100 --editals 150
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] - Data Generation",
        subtitle="📊 Generating synthetic data..."
    ))
    
    try:
        import sys
        sys.path.insert(0, '.')
        from database.generate_synthetic_data import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(seed=42)
        
        console.print(f"\n[cyan]Generating {editals} editals and {memorials} memorials...[/cyan]")
        
        dataset = generator.generate_dataset(num_memorials=memorials, num_editals=editals)
        
        generator.to_json(dataset, f"{output}/synthetic_dataset.json")
        generator.to_sql_inserts(dataset, f"{output}/synthetic_inserts.sql")
        
        total_paragraphs = sum(len(m['paragraphs']) for m in dataset['memorials'])
        
        console.print(f"\n[green]✓ Data generated![/green]")
        console.print(f"   Editals: {len(dataset['editals'])}")
        console.print(f"   Memorials: {len(dataset['memorials'])}")
        console.print(f"   Paragraphs: {total_paragraphs}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# SCRAPE Command
# ============================================================================

@cli.command()
@click.option('--output', '-o', type=click.Path(), default='data/',
              help='Output directory')
def scrape(output):
    """
    🌐 Scrape real Brazilian innovation grants
    
    Example: editalshield scrape --output data/
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] - Edital Scraper",
        subtitle="🌐 Collecting real grants..."
    ))
    
    try:
        import sys
        sys.path.insert(0, '.')
        from database.scraper_editais_reais import EditalScraper
        
        scraper = EditalScraper(output_dir=output)
        editals = scraper.run_all()
        
        scraper.save_to_json()
        scraper.save_to_sql()
        
        console.print(f"\n[green]✓ Scraped {len(editals)} real editals![/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# INFO Command
# ============================================================================

@cli.command()
def info():
    """
    ℹ️ Show EditalShield information and status
    """
    console.print(Panel.fit(
        "[bold blue]EditalShield[/bold blue] v0.2.0",
        subtitle="🛡️ IP Protection Framework"
    ))
    
    console.print("\n[bold]Available Commands:[/bold]")
    console.print("  analyze  - Analyze memorial for IP exposure")
    console.print("  protect  - Protect memorial by replacing sensitive content")
    console.print("  train    - Train the Bayesian risk model")
    console.print("  generate - Generate synthetic training data")
    console.print("  scrape   - Scrape real Brazilian grants")
    
    # Check model status
    model_path = Path("models/bayesian_model_latest.pkl")
    if model_path.exists():
        console.print("\n[green]✓ Model: Trained and ready[/green]")
    else:
        console.print("\n[yellow]⚠ Model: Not trained. Run 'editalshield train'[/yellow]")
    
    # Check data status
    data_path = Path("data/synthetic_dataset.json")
    if data_path.exists():
        console.print("[green]✓ Data: Available[/green]")
    else:
        console.print("[yellow]⚠ Data: Not generated. Run 'editalshield generate'[/yellow]")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
