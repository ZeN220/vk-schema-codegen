from pathlib import Path
import logging

import click


@click.group()
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
@click.option(
	"-i",
	"--input-dir",
	help="Directory with the schemas of API methods",
)
def cli():
	pass


def main():
	logging.basicConfig(
		level=logging.INFO,
		format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
	)
	cli()


if __name__ == '__main__':
	main()
