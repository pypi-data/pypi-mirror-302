"""Fernet key management CLI."""

from typing_extensions import Annotated
from typing import Optional

import typer

import ai4_api_keys.fernet

app = typer.Typer(help="AI4 Fernet keys management CLI.")


@app.command(name="generate")
def generate_cli(
    output: Annotated[
        Optional[str],
        typer.Option("--output", "-o", help="Output file for the generated key."),
    ] = None,
) -> None:
    """Generate a new Fernet key."""
    key = ai4_api_keys.fernet.generate()
    if output is None:
        typer.echo(key.decode())
    else:
        with open(output, "wb") as key_file:
            key_file.write(key)


@app.command(name="encrypt")
def encrypt_cli(
    key: str = typer.Argument(..., help="The Fernet key to use."),
    data: str = typer.Argument(..., help="The data to encrypt."),
) -> None:
    """Encrypt data using a Fernet key (CLI)."""
    typer.echo(ai4_api_keys.fernet.encrypt(key, data))


@app.command(name="decrypt")
def decrypt_cli(
    key: str = typer.Argument(..., help="The Fernet key to use."),
    data: str = typer.Argument(..., help="The data to decrypt."),
) -> None:
    """Decrypt data using a Fernet key (CLI)."""
    typer.echo(ai4_api_keys.fernet.decrypt(key, data))
