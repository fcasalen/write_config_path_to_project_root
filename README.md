# Python

Write configuration path to a project root so it can be used by the project.
A txt file will be created in the project root with the path to the configuration file.
Can create multiple txt files pointing to different configuration files.
Just call the function get_config with the project root path and the configuration file name.
If the file already exists and pinpoints to a existing configuration file, the data from the
configuration file will be returned.
If the file pinpoints to a nont existing configuration file, the function will create a new
txt file and asks for the configuration file path.
If the file does not exist, the function will create a new txt file and asks for the
configuration file path.

## Example of usage

```python
from write_config_path_to_project_root import handler

handler.get_config("path/to/project", "config_file.txt")
```
