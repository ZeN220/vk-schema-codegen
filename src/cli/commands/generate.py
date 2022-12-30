import click

from src.cli.config import Config
from src.codegen import generate_objects, generate_responses


@click.command("generate", help="Generate code for all entities from API schema")
@click.pass_obj
def command_generate(config: Config):
    generate_objects(input_dir=config.input_dir, output_dir=config.output_dir)
    generate_responses(
        input_dir=config.input_dir,
        output_dir=config.output_dir / "responses",
        objects_package=config.output_dir.name,
    )
