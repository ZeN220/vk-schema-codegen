from pathlib import Path

from src.cli.config import Config


class TestConfig:
    def test___init__(self):
        test_input_dir = Path.cwd() / "input"
        test_output_dir = Path.cwd() / "output"
        config = Config(input_dir=test_input_dir, output_dir=test_output_dir)
        assert config.input_dir == test_input_dir
        assert config.output_dir == test_output_dir
