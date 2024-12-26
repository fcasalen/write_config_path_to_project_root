from os.path import exists, join
from cli_pprinter import CLIPPrinter
from file_handler import FileHandler
from tkinter.filedialog import askopenfilename

class HANDLER:
    @staticmethod
    def checks(project_root_path:str, project_config_file_path:str = "config_path.txt"):
        """checks if project_root_path exists and if project_config_file_path is a txt file

        Args:
            project_root_path (str): project root path to the txt file that contains the config_path
            project_config_file_path (str): txt file where the path to config_path will be saved. Defaults to config_path.txt

        Raises:
            ValueError: if project_root_path doesn't exists or project_config_file_path is not a txt file
        """
        if not exists(project_root_path):
            raise ValueError(f'project_root_path not found: {project_root_path}')
        if not project_config_file_path.endswith('.txt'):
            raise ValueError(f'project_config_file_path must be a .txt file. Passed {project_config_file_path}')
        
    @staticmethod
    def load_config_path_to_project_root(project_root_path:str, project_name:str, project_config_file_path:str = "config_path.txt"):
        """load config_path from project_config_file_path, so the project can use this saved path without the need to implement a function in each project

        Args:
            project_root_path (str): project root path to the txt file that contains the config_path
            project_name (str): project name
            project_config_file_path (str): txt file where the path to config_path will be saved. Defaults to config_path.txt
            
        Returns:
            str: returs the config_path saved in the project_config_file so it can be used outside this method
        """
        HANDLER.checks(project_config_file_path=project_config_file_path, project_root_path=project_root_path)
        path = join(project_root_path, project_config_file_path)
        if not exists(path):
            return HANDLER.set_new_config_path_to_project_root(project_root_path=project_root_path, project_name=project_name, project_config_file_path=project_config_file_path)
        file_path = FileHandler.load(path, load_first_value=True)
        if not exists(file_path):
            CLIPPrinter.red(f"Saved config_path ({file_path}) not found! You will be asked to pass a new one.")
            return HANDLER.set_new_config_path_to_project_root(project_root_path=project_root_path, project_name=project_name, project_config_file_path=project_config_file_path)
        return file_path
    
    @staticmethod
    def set_new_config_path_to_project_root(project_root_path:str, project_name:str, project_config_file_path:str = "config_path.txt"):
        """write a file_path in a txt file in a project, so the project can use this saved path without the need to implement a function in each project

        Args:
            project_root_path (str): project root path to the txt file that contains the config_path
            project_name (str): project name
            project_config_file_path (str): txt file where the path to config_path will be saved. Defaults to config_path.txt

        Returns:
            str: returs the config_path so it can be used outside this method
        """
        HANDLER.checks(project_config_file_path=project_config_file_path, project_root_path=project_root_path)
        file_path = askopenfilename(title=f"Select config_path to project {project_name}")
        if file_path != '':
            FileHandler.write({join(project_root_path, project_config_file_path): file_path})
        return file_path
        
        