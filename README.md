# vk-schema-codegen
This CLI application needs for generating Python code on base VK API schema.

## Usage
Command `python -m src` show help message:
```bash
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  -o, --output-dir DIRECTORY  Directory to save the output files  [default:
                              output]
  -i, --input-dir DIRECTORY   Directory with the schemas of API methods
  --help                      Show this message and exit.

Commands:
  objects  Generate objects from API schema
```

### Generate objects
For generating objects you need to run the following command:
```bash
python -m src objects --input-dir <path to directory with schema files>
```
