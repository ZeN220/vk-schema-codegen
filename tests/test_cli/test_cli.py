import pytest
from click.testing import CliRunner

from src.cli.cli import cli


def test_cli(tmp_path_factory: pytest.TempPathFactory):
    input_dir = tmp_path_factory.mktemp("input")
    output_dir = tmp_path_factory.mktemp("output")
    runner = CliRunner()
    result = runner.invoke(
        cli,  # noqa
        [
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
    )
    # Because we don't have any commands, it should fail
    assert result.exit_code == 2
    assert "Error: Missing command." in result.output
