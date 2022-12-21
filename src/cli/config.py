from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    input_dir: Path
    output_dir: Path
