"""AI4 API Keys management CLI."""

import pathlib
from typing_extensions import Annotated
from typing import Optional

import typer

from ai4_api_keys import exceptions
import ai4_api_keys.fernet
import ai4_api_keys.keys

app = typer.Typer(help="AI4 API Keys management CLI.")


@app.command(name="create")
def create_cli(
    key_file: Annotated[
        Optional[pathlib.Path],
        typer.Option("--key-file", "-k", help="Read fernet key from a file."),
    ] = None,
    key: Annotated[
        Optional[str], typer.Option("--key", "-K", help="Use a specific fernet key.")
    ] = None,
    level: Annotated[
        ai4_api_keys.keys.APILevels,
        typer.Option("--level", "-l", help="The level of the API key."),
    ] = ai4_api_keys.keys.APILevels.BRONZE,
    scope: Annotated[
        str, typer.Option("--scope", "-s", help="The scope of the API key.")
    ] = "ai4eosc",
) -> None:
    """Create a new API key (CLI)."""
    if key_file and key:
        raise typer.BadParameter("Cannot use both --key-file and --key.")

    if key_file is not None:
        with open(key_file, "r") as f:
            key = f.read().strip()

    if key is None:
        raise typer.BadParameter("Either --key-file or --key must be provided.")

    typer.echo(ai4_api_keys.keys.create(key, scope, level))


@app.command(name="validate")
def validate_cli(
    key_file: Annotated[
        Optional[pathlib.Path],
        typer.Option("--key-file", "-k", help="Read fernet key from a file."),
    ] = None,
    key: Annotated[
        Optional[str], typer.Option("--key", "-K", help="Use a specific fernet key.")
    ] = None,
    quiet: Annotated[
        bool, typer.Option("--quiet", "-q", help="Do not print the result.")
    ] = False,
    scope: str = typer.Argument("ai4eosc", help="The scope of the API key."),
    api_key: str = typer.Argument(..., help="The API key to validate."),
) -> None:
    """Validate an API key (CLI)."""
    if key_file and key:
        raise typer.BadParameter("Cannot use both --key-file and --key.")

    if key_file is not None:
        with open(key_file, "r") as f:
            key = f.read().strip()

    if key is None:
        raise typer.BadParameter("Either --key-file or --key must be provided.")

    try:
        ai4_api_keys.keys.validate(key, api_key, scope)
    except exceptions.BaseError as e:
        if not quiet:
            typer.echo(e)
        raise typer.Exit(code=1)
    else:
        if not quiet:
            typer.echo("API key is valid.")


@app.command(name="dump")
def dump_key_contents(
    key_file: Annotated[
        Optional[pathlib.Path],
        typer.Option("--key-file", "-k", help="Read fernet key from a file."),
    ] = None,
    key: Annotated[
        Optional[str], typer.Option("--key", "-K", help="Use a specific fernet key.")
    ] = None,
    scope: str = typer.Argument("ai4eosc", help="The scope of the API key."),
    api_key: str = typer.Argument(..., help="The API key to dump."),
) -> None:
    """Validate and dump the key contents (CLI).

    If the key is valid, the contents will be printed to the console. Otherwise the
    command will exit with a non-zero status code.
    """
    if key_file and key:
        raise typer.BadParameter("Cannot use both --key-file and --key.")

    if key_file is not None:
        with open(key_file, "r") as f:
            key = f.read().strip()

    if key is None:
        raise typer.BadParameter("Either --key-file or --key must be provided.")

    try:
        ai4_api_keys.keys.validate(key, api_key, scope)
        decrypted = ai4_api_keys.fernet.decrypt(key, api_key)
        typer.echo(decrypted)
    except exceptions.BaseError as e:
        typer.echo(e)
        raise typer.Exit(code=1)
