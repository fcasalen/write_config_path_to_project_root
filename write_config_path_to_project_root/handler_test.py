from sys import path
from os.path import dirname, abspath, join
path.insert(0, abspath(dirname(__file__)))
import pytest
from unittest.mock import patch
import handler

def test_checks_valid_paths():
    with patch("handler.exists") as mock_exists:
        mock_exists.side_effect = lambda path: path == "valid_project_root_path"
        handler.HANDLER.checks("valid_project_root_path", "valid_config_path.txt")

def test_checks_invalid_project_root():
    with pytest.raises(ValueError, match="project_root_path not found: invalid_project_root"):
        handler.HANDLER.checks("invalid_project_root", "valid_config_path.txt")

def test_checks_invalid_config_file_extension():
    with patch("handler.exists") as mock_exists:
        mock_exists.side_effect = lambda path: path == "valid_project_root_path"
        with pytest.raises(ValueError, match="project_config_file_path must be a .txt file"):
            handler.HANDLER.checks("valid_project_root_path", "invalid_config_path.cfg")

@patch("handler.askopenfilename")
@patch("handler.FileHandler.write")
@patch("handler.exists")
def test_set_new_config_path_to_project_root(mock_exists, mock_write, mock_askopenfilename):
    mock_exists.return_value = True
    mock_askopenfilename.return_value = "selected_config_path"
    
    result = handler.HANDLER.set_new_config_path_to_project_root("valid_project_root", "project_name", "config_path.txt")
    
    assert result == "selected_config_path"
    mock_write.assert_called_once_with({join("valid_project_root", "config_path.txt"): "selected_config_path"})

@patch("handler.askopenfilename")
@patch("handler.FileHandler.write")
@patch("handler.exists")
def test_set_new_config_path_to_project_root_no_file_selected(mock_exists, mock_write, mock_askopenfilename):
    mock_exists.return_value = True
    mock_askopenfilename.return_value = ""
    
    result = handler.HANDLER.set_new_config_path_to_project_root("valid_project_root", "project_name", "config_path.txt")
    
    assert result == ""
    mock_write.assert_not_called()

@patch("handler.exists")
@patch("handler.FileHandler.load")
@patch("handler.CLIPPrinter.red")
@patch("handler.HANDLER.set_new_config_path_to_project_root")
def test_load_config_path_to_project_root_file_exists(mock_set_new_config, mock_printer, mock_load, mock_exists):
    mock_exists.side_effect = lambda path: path in ["valid_path", join("valid_path", "config_fake_path.txt"), "valid_config_path"]
    mock_load.return_value = "valid_config_path"
    result = handler.HANDLER.load_config_path_to_project_root("valid_path", "project_name", "config_fake_path.txt")
    assert result == "valid_config_path"
    mock_set_new_config.assert_not_called()
    mock_printer.assert_not_called()

@patch("handler.exists")
@patch("handler.FileHandler.load")
@patch("handler.CLIPPrinter.red")
@patch("handler.HANDLER.set_new_config_path_to_project_root")
def test_load_config_path_to_project_root_file_not_exists(mock_set_new_config, mock_printer, mock_load, mock_exists):
    mock_exists.side_effect = lambda path: path in ["valid_path", join("valid_path", "config_fake_path.txt")]
    mock_set_new_config.return_value = "new_config_path"
    mock_load.return_value = "new_config_path"
    result = handler.HANDLER.load_config_path_to_project_root("valid_path", "project_name", "config_fake_path.txt")
    assert result == "new_config_path"
    mock_printer.assert_called_once_with("Saved config_path (new_config_path) not found! You will be asked to pass a new one.")
    mock_set_new_config.assert_called_once()


