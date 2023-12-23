import json
from pathlib import Path

from plugins import preferences_directories as dir

class Config:
    def __init__(self, config_file=dir.config_file()):
        self.config_file = config_file
        self.configs = self.load_configs()

    def load_configs(self):
        if validate() == True:
            # Check the contents first
            with open(self.config_file, 'r') as file:
                valid_configs = json.load(file)
                return valid_configs
        else:
            pass # create a new config.json file

    def validate(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as file:
                    configs = json.load(file)
                    for key, directory in configs.itmes():
                        if key.endswith('_dir') and not(Path(directory).is_dir()):
                            e = f"{key} directory does not exist or is not valid: "
                            logging.error(e)
                            return False
                        else:
                            return True

            except json.JSONDecodeError:
                e = "Unable to read the contents of the file"
                logging.error(e)
            except FileNotFoundError:
                e = "Config file not found"
                logging.error(e)
            except Exception as e:
                e = f"Unexpected error: {e}"
                logging.error(e)
            return False
        
    def write(self, configs):
    with open(self.config_file, 'w+') as file:
        json.dump(configs, file, indent=2)