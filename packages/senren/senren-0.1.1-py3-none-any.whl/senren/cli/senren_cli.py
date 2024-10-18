from pathlib import Path
from typing import Optional

import typer

from senren.cli.batch_job_cli import batch_job_app
from senren.cli.python_env_cli import python_env_app
from senren.cli.state_cli import state_app
from senren.logging_config import setup_logging

app = typer.Typer()

app.add_typer(state_app, name="state")
app.add_typer(python_env_app, name="python-env")
app.add_typer(batch_job_app, name="batch-job")


@app.callback()
def main(config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to config file")):
    """Senren CLI"""
    if config:
        # TODO: Implement config loading
        pass
    setup_logging()


@app.command("shell-completion")
def shell_completion(
    shell: str = typer.Option(..., help="Shell type"),
    install: bool = typer.Option(False, "--install", help="Install completion script"),
    script: bool = typer.Option(False, "--script", help="Output completion script"),
):
    """Handle shell completion"""
    typer.echo(f"Handling shell completion for {shell} shell")
    if install:
        typer.echo("Installing completion script")
        # TODO: Implement install completion script logic
    if script:
        typer.echo("Outputting completion script")
        # TODO: Implement output completion script logic


if __name__ == "__main__":
    app()
