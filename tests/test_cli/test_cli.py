import click
import pytest
from click.testing import CliRunner

from src.cli.cli import cli


@click.command("test_command")
def cli_test_command():
    pass


def test_cli(tmp_path_factory: pytest.TempPathFactory):
    input_dir = tmp_path_factory.mktemp("input")
    output_dir = tmp_path_factory.mktemp("output")
    runner = CliRunner()
    cli.add_command(cli_test_command)
    result = runner.invoke(
        cli,  # noqa
        [
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "test_command",
        ],
    )
    assert result.exit_code == 0
