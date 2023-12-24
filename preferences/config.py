import json
import logging
from pathlib import Path
import sys
print('\n\n')
print(sys.path)
print('\n\n')

from preferences import paths
from preferences import style

class Config:
    def __init__(self, config_file=paths.config_file()):
        self.config_file = config_file
        self.configs = self.load()


    def load(self):
        if self.validate() == True:
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
                    for key, directory in configs.items():
                        if key.endswith('_dir') and not Path(directory).is_dir():
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


    def create(self):
        source_dir = input("Source folder: ")
        movie_dir = input("Movie target folder: ")
        show_dir = input("TV Show target folder: ")
        audiobook_dir = input("Audiobook target folder: ")

        new_configs = {
            "source": source_dir,
            "movie": movie_dir,
            "show": show_dir,
            "audiobook": audiobook_dir
            }
        
        self.write(new_configs)
        self.configs = new_configs
        return new_configs
    

    def print(self):
        if self.configs:
            source_msg = style.bold(f"Source 	→ {self.configs['source']}")
            movie_msg = f"Movies 	→ {self.configs['movie']}"
            shows_msg = f"Shows 	→ {self.configs['show']}"
            books_msg = f"Books 	→ {self.configs['audiobook']}"
            print(f"{source_msg}\n{movie_msg}\n{shows_msg}\n{books_msg}")
        else:
            e = "Preferences not loaded or invalid"
            logging.error(e)


if __name__ == '__main__':
    config = Config()

    if config.configs:
        config.print()
    else:
        config.create()