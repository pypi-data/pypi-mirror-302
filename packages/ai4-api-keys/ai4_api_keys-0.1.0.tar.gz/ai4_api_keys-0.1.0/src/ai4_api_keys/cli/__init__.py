"""Command line interface for the ai4-api-keys package."""

import typer

import ai4_api_keys
from ai4_api_keys.cli import fernet as fernet_cli
from ai4_api_keys.cli import keys as keys_cli

app = typer.Typer(help="AI4 API Keys management CLI.")
app.add_typer(fernet_cli.app, name="fernet")
app.add_typer(keys_cli.app, name="keys")


def version_callback(value: bool):
    """Return the version for the --version option."""
    if value:
        typer.echo(ai4_api_keys.extract_version())
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    )
):
    """Show version and exit."""
    pass
