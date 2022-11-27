from pathlib import Path

import click


@click.command()
@click.option(
	"-e",
	"--errors",
	show_default=True,
	default="errors.json",
	help=(
		"Path to the file with errors of API "
		"(https://github.com/VKCOM/vk-api-schema/blob/master/errors.json)"
	),
	type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
	"-o",
	"--output-dir",
	show_default=True,
	default="output",
	help="Directory to save the output files",
	type=click.Path(exists=True, file_okay=False, path_type=Path),
)
def cli():
	pass
