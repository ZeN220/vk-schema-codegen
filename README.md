# vk-schema-codegen
This CLI application needs for generating Python code on base VK API schema.

## Installation
For installing you need to have installed Python 3.8+. Then you need to install dependencies:
```bash
pip install -r requirements/requirements.txt
```
Or you can use `poetry`:
```bash
poetry install
```

## Usage
Command `python -m src` show help message:
```bash
Usage: python -m src [OPTIONS] COMMAND [ARGS]...

Options:
  -o, --output-dir DIRECTORY  Directory to save the output files  [default:
                              output]
  -i, --input-dir DIRECTORY   Directory with the schemas of the VK API
                              [default: vk-api-schema]
  --help                      Show this message and exit.

Commands:
  objects    Generate objects from API schema
  responses  Generate objects from API schema
```

### Generate objects
For generating objects you need to run the following command:
```bash
python -m src objects
```

### Generate responses
For generating responses you need to run the following command:
```bash
python -m src responses --objects-package <package>
```
Where `<package>` is a package with generated objects.py file.
