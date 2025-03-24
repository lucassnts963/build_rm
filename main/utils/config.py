import configparser, os

class Settings:
    def __init__(self) -> None:
        self.config = self.read_config()

    def read_config(self):
        config_path = os.path.join(os.getcwd(), 'config.ini')
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            return config
        except Exception as e:
            print(e)
            return None
        
    def write_config(self, config):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def change_materials_path(self, newpath, project = 'CALDEIRAS'):
        config = self.read_config()

        if project == 'CALDEIRAS':
            config['Path']['material_data_path_caldeiras'] = newpath
        else:
            config['Path']['material_data_path_utility'] = newpath

        self.write_config(config)

    def change_project_path(self, newpath, project = 'CALDEIRAS'):
        config = self.read_config()

        if project == 'CALDEIRAS':
            config['Path']['project_data_path_caldeiras'] = newpath
        else:
            config['Path']['project_data_path_utility'] = newpath

        self.write_config(config)
    
    def change_report_path(self, newpath):
        config = self.read_config()
        config['Path']['path_report'] = newpath
        self.write_config(config)
    
    def get_report_path(self):
        config = self.read_config()

        report_path = config['Path']['path_report']

        try:
            if not os.path.exists(report_path):
                os.makedirs(report_path)
        except Exception as e:
            print(f'Erro ao criar a pastas {report_path} [{e}]')

        return report_path

    def get_database_path(self):
        config = self.read_config()
        return config['Database']['db_name']

    def get_materials_data_path(self, project = 'CALDEIRAS'):
        config = self.read_config()

        if not config:
            return

        if project == 'CALDEIRAS':
            return config['Path']['material_data_path_caldeiras']
        else:
            return config['Path']['material_data_path_utility']
        
    def get_projects_data_path(self, project = 'CALDEIRAS'):
        config = self.read_config()

        if not config:
            return

        if project == 'CALDEIRAS':
            return config['Path']['project_data_path_caldeiras']
        else:
            return config['Path']['project_data_path_utility']
    
    def change_default_project(self, project = 'CALDEIRAS'):
        config = self.read_config()
        config['Path']['project'] = project

        self.write_config(config)

