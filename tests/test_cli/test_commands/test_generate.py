import pytest
from click.testing import CliRunner

from src.cli.commands.generate import command_generate
from src.cli.config import Config


def test_command_generate(tmp_path_factory: pytest.TempPathFactory):
    input_dir = tmp_path_factory.mktemp("input")
    output_dir = tmp_path_factory.mktemp("output")
    test_config = Config(input_dir=input_dir, output_dir=output_dir)

    runner = CliRunner()
    result = runner.invoke(command_generate, obj=test_config)  # noqa
    assert result.exit_code == 0
