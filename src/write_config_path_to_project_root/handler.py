import json
from pathlib import Path
from tkinter import filedialog
from typing import Any


def checks(
    project_root_path: str, project_config_path_locator: str = "config_path.txt"
) -> None:
    """checks if project_root_path exists and if project_config_path_locator is a
    txt file

    Args:
        project_root_path (str): project root path to the txt file that contains
            the config_path
        project_config_path_locator (str): txt file where the path to config_path
            will be saved. Defaults to config_path.txt

    Raises:
        ValueError: if project_root_path doesn't exists or project_config_path_locator
            is not a txt file
    """
    project_root_path = Path(project_root_path)
    if not project_root_path.exists():
        raise ValueError(f"project_root_path not found: {project_root_path}")
    if not project_config_path_locator.endswith(".txt"):
        raise ValueError(
            f"project_config_path_locator must be a .txt file. Passed "
            f"{project_config_path_locator}"
        )


def set_new_config_path_to_project_root(
    project_root_path: str, project_config_path_locator: str = "config_path.txt"
) -> str:
    """write a file_path in a txt file in a project, so the project can use this saved
    path without the need to implement a function in each project

    Args:
        project_root_path (str): project root path to the txt file that contains the
            config_path
        project_config_path_locator (str): txt file where the path to config_path
            will be saved. Defaults to config_path.txt

    Raises:
        ValueError: if file_path selected doesn't exist

    Returns:
        str: returns the config_path so it can be used outside this method
    """
    file_path = filedialog.askopenfilename(
        title=f"Select config_path to project at {project_root_path}"
    )
    if file_path != "":
        if not Path(file_path).exists():
            raise ValueError(f"file_path selected doesn't exist: {file_path}")
        with open(
            Path(project_root_path) / project_config_path_locator, "w", encoding="utf-8"
        ) as f:
            f.write(file_path)
    return file_path


def load_json_config(file_path: str, config_class: Any = None):
    """load json file from a path to a config_class. If config_class is None,
    returns the json as a dict.

    Args:
        file_path (str): path to the json file
        config_class (Any): config class to load the json file. Defaults to None.

    :return: config_class instance or dict or list
    :rtype: dict | list | config_class
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if config_class is None:
        return data
    return config_class(**data)


def get_config(
    project_root_path: str,
    project_config_path_locator: str = "config_path.txt",
    config_class: Any = None,
):
    """load config_path from project_config_path_locator, so the project can use
    this saved path without the need to implement a function in each project

    Args:
        project_root_path (str): project root path to the txt file that contains
            the config_path
        project_config_path_locator (str): txt file where the path to config_path
            will be saved. Defaults to config_path.txt

    return: config_class instance or dict or list
    :rtype: dict | list | config_class
    """
    path = Path(project_root_path) / project_config_path_locator
    if not path.exists():
        path.touch()
    file_path = None
    while file_path is None:
        with open(path, "r", encoding="utf-8") as f:
            file_path = f.read().strip()
        if file_path in ["", ".", ".."] or not Path(file_path).exists():
            print(
                f"Saved config_path ({str(file_path)}) not found! "
                "You will be asked to pass a new one."
            )
            set_new_config_path_to_project_root(
                project_root_path=project_root_path,
                project_config_path_locator=project_config_path_locator,
            )
            file_path = None
    return load_json_config(
        file_path=str(file_path),
        config_class=config_class,
    )
