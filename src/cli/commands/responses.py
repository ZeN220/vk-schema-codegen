import click

from src.cli.config import Config
from src.codegen import generate_responses


@click.command("responses", help="Generate responses from API schema")
@click.option("--objects-package", help="Package, that contains objects of schema", required=True)
@click.pass_obj
def command_generate_responses(config: Config, objects_package: str) -> None:
    generate_responses(config.input_dir, config.output_dir, objects_package)
