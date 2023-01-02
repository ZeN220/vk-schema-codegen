import click

from src.cli.config import Config
from src.codegen import generate_objects


@click.command("objects", help="Generate objects from API schema")
@click.pass_obj
def command_generate_objects(config: Config) -> None:
    generate_objects(config.input_dir, config.output_dir)
