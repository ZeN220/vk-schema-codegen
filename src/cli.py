from pathlib import Path

import click


@click.command()
@click.option(
    "-m",
    "--methods-dir",
    show_default=True,
    default="methods",
    help="Directory containing API methods in the form of Python functions.",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "-r",
    "--responses-dir",
    show_default=True,
    default="responses",
    help="Directory containing responses of API methods in the form of Python classes.",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "-o",
    "--objects-dir",
    show_default=True,
    default="objects",
    help="Directory containing objects of API in the form of Python classes.",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
def cli():
    pass
