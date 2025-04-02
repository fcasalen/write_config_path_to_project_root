# Python

```python
from handler import HANDLER

HANDLER.checks("path/to/project", "config_file.txt")

config_path = HANDLER.load_config_path_to_project_root(
    "path/to/project", 
    "MyProject", 
    "my_config.txt"
)
print(f"Loaded config path: {config_path}")


new_config_path = HANDLER.set_new_config_path_to_project_root(
    "path/to/project", 
    "MyProject", 
    "my_config.txt"
)
print(f"New config path set: {new_config_path}")

config_class = HANDLER.load_json_config(
    file_path="config.json",
    class_name="MyConfigClass"
)
```
