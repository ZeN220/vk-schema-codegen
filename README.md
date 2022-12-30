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
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  -o, --output-dir DIRECTORY  Directory to save the output files  [default:
                              output]
  -i, --input-dir DIRECTORY   Directory with the schemas of the VK API
                              [default: vk-api-schema]
  --help                      Show this message and exit.

Commands:
  generate   Generate all entities from API schema
  objects    Generate objects from API schema
  responses  Generate responses from API schema
```
For generating code you need to use `generate` command:
```bash
python -m src generate
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
