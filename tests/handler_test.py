from pathlib import Path
from unittest.mock import patch

import pytest

from src.write_config_path_to_project_root import handler


class TestChecks:
    def test_invalid_project_root(self):
        with pytest.raises(
            ValueError, match="project_root_path not found: invalid_project_root"
        ):
            handler.checks("invalid_project_root")

    def test_invalid_project_config_path_locator(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project_root"
        valid_project_root.mkdir()
        with pytest.raises(
            ValueError,
            match="project_config_path_locator must be a .txt file. "
            "Passed invalid_config_path.cfg",
        ):
            handler.checks(str(valid_project_root), "invalid_config_path.cfg")

    def test_valid_inputs(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        handler.checks(str(valid_project_root), "valid_config_path.txt")


class TestSetNewConfigPathToProjectRoot:
    def test_emtpy(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        with patch("tkinter.filedialog.askopenfilename", return_value=""):
            result = handler.set_new_config_path_to_project_root(
                str(valid_project_root), "config_path.txt"
            )
        assert result == ""

    def test_invalid_path(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        with (
            patch("tkinter.filedialog.askopenfilename", return_value="invalid_path"),
            pytest.raises(
                ValueError, match="file_path selected doesn't exist: invalid_path"
            ),
        ):
            handler.set_new_config_path_to_project_root(
                str(valid_project_root), "config_path.txt"
            )

    def test_valid_path(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        valid_file_path = tmp_path / "valid_file_path.json"
        valid_file_path.touch()
        with patch(
            "tkinter.filedialog.askopenfilename", return_value=str(valid_file_path)
        ):
            result = handler.set_new_config_path_to_project_root(
                str(valid_project_root), "config_path.txt"
            )
        assert result == str(valid_file_path)


class TestLoadJsonConfig:
    def test_valid_path(self, tmp_path: Path):
        class ConfigMock:
            def __init__(self, data):
                self.data = data

        valid_file_path = tmp_path / "valid_path.json"
        valid_file_path.write_text('{"data": "data"}', encoding="utf-8")
        result = handler.load_json_config(str(valid_file_path), ConfigMock)
        assert result.__dict__ == ConfigMock("data").__dict__

    def test_valid_path_no_config_class(self, tmp_path: Path):
        valid_file_path = tmp_path / "valid_path.json"
        valid_file_path.write_text('{"data": "data"}', encoding="utf-8")
        result = handler.load_json_config(str(valid_file_path))
        assert result == {"data": "data"}


class TestGetConfig:
    def test_path_not_exists(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        valid_file_path = tmp_path / "valid_file_path.json"
        valid_file_path.touch()
        with patch(
            "src.write_config_path_to_project_root.handler.set_new_config_path_to_project_root",
            return_value=str(valid_file_path),
        ):
            result = handler.get_config(str(valid_project_root), "config_path.txt")
        assert result == str(valid_file_path)

    def test_path_not_existing_anymore(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        config_path_locator = valid_project_root / "config_path.txt"
        config_path_locator.write_text(
            str(tmp_path / "non_existing_path.json"), encoding="utf-8"
        )
        valid_file_path = tmp_path / "valid_file_path.json"
        valid_file_path.touch()
        with patch(
            "src.write_config_path_to_project_root.handler.set_new_config_path_to_project_root",
            return_value=str(valid_file_path),
        ):
            result = handler.get_config(str(valid_project_root), "config_path.txt")
        assert result == str(valid_file_path)

    def test_path_exists(self, tmp_path: Path):
        valid_project_root = tmp_path / "valid_project"
        valid_project_root.mkdir()
        config_path_locator = valid_project_root / "config_path.txt"
        valid_file_path = tmp_path / "valid_file_path.json"
        valid_file_path.write_text('{"data": "data"}', encoding="utf-8")
        config_path_locator.write_text(str(valid_file_path), encoding="utf-8")
        result = handler.get_config(str(valid_project_root), "config_path.txt")
        assert result == {"data": "data"}
