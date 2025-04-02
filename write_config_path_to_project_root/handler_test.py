from . import handler

from unittest.mock import patch
import pytest
import os

def test_checks():
    with pytest.raises(ValueError, match="project_root_path not found: invalid_project_root"):
        handler.HANDLER.checks("invalid_project_root")
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        handler.HANDLER.checks("valid_project_root_path", "valid_config_path.txt")
        with pytest.raises(ValueError, match="project_config_file_path must be a .txt file"):
            handler.HANDLER.checks("valid_project_root_path", "invalid_config_path.cfg")

def test_set_new_config_path_to_project_root():
    with patch("os.path.exists", return_value=True), \
        patch("file_handler.FileHandler.write") as mock_write, \
        patch("tkinter.filedialog.askopenfilename", return_value='selected_config_path') as mock_askopenfilename:
        result = handler.HANDLER.set_new_config_path_to_project_root("valid_project_root", "project_name", "config_path.txt")
        assert result == "selected_config_path"
        mock_write.assert_called_once_with({os.path.join("valid_project_root", "config_path.txt"): "selected_config_path"})
        mock_askopenfilename.return_value = ""
        result = handler.HANDLER.set_new_config_path_to_project_root("valid_project_root", "project_name", "config_path.txt")
        assert result == ""
        mock_write.call_count == 2

def test_load_config_path_to_project_root():
    with patch("os.path.exists", return_value=True) as mock_exists, \
        patch("file_handler.FileHandler.load") as mock_load, \
        patch("cli_pprinter.CLIPPrinter.red") as mock_printer, \
        patch("write_config_path_to_project_root.handler.HANDLER.set_new_config_path_to_project_root") as mock_set_new_config:
        mock_exists.side_effect = lambda path: path in ["valid_path", os.path.join("valid_path", "config_fake_path.txt"), "valid_config_path"]
        mock_load.return_value = "valid_config_path"
        result = handler.HANDLER.load_config_path_to_project_root("valid_path", "project_name", "config_fake_path.txt")
        assert result == "valid_config_path"
        mock_set_new_config.assert_not_called()
        mock_printer.assert_not_called()
        mock_exists.side_effect = lambda path: path in ["valid_path", os.path.join("valid_path", "config_fake_path.txt")]
        mock_set_new_config.return_value = "new_config_path"
        mock_load.return_value = "new_config_path"
        result = handler.HANDLER.load_config_path_to_project_root("valid_path", "project_name", "config_fake_path.txt")
        assert result == "new_config_path"
        mock_printer.assert_called_once_with("Saved config_path (new_config_path) not found! You will be asked to pass a new one.")
        mock_set_new_config.assert_called_once()

def test_load_json_config():
    class ConfigMock:
        def __init__(self, data):
            self.data = data
    with pytest.raises(ValueError, match="path to valid_path doesn't exist!"):
        handler.HANDLER.load_json_config("valid_path", ConfigMock)
    with patch("os.path.exists") as mock_exists, patch('file_handler.FileHandler.load') as mock_load:
        mock_load.return_value = {'data': 'data'}
        mock_exists.return_value = True
        result = handler.HANDLER.load_json_config("valid_path", ConfigMock)
        assert result.__dict__ == ConfigMock('data').__dict__

