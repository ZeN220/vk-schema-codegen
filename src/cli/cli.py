import logging
from pathlib import Path

import click

from .commands import (
    command_generate,
    command_generate_objects,
    command_generate_responses,
)
from .config import Config


@click.group()
@click.option(
    "-o",
    "--output-dir",
    show_default=True,
    default="output",
    help="Directory to save the output files",
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "-i",
    "--input-dir",
    show_default=True,
    default="vk-api-schema",
    help="Directory with the schemas of the VK API",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.pass_context
def cli(ctx: click.Context, output_dir: Path, input_dir: Path):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
    )
    config = Config(input_dir=input_dir, output_dir=output_dir)
    ctx.obj = config


def main():
    for command in [command_generate_objects, command_generate_responses, command_generate]:
        cli.add_command(command)  # noqa
    cli()


if __name__ == "__main__":
    main()
