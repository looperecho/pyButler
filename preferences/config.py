import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key

from preferences import paths
from preferences import style

class Config:
    def __init__(self, config_file=paths.config_file()):
        self.config_file = config_file
        self.configs = self.load()


    def load(self):
        if self.validate() == True: # Check the contents first
            print("config check OK!")
            with open(self.config_file, 'r') as file:
                valid_configs = json.load(file)
                return valid_configs
        else:
            self.create()


    def validate(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as file:
                    temp_configs = json.load(file)
                    for key, directory in temp_configs.items():
                        if key is not Path(directory).is_dir():
                            e = f"{key} directory does not exist or is not valid: "
                            logging.error(e)
                        else:
                            return True

            except json.JSONDecodeError:
                e = "Unable to read the contents of the config file"
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
        print("No config file, let's create a new one!")

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


    def display(self):
        if self.configs:
            source_msg = style.bold(f"Source 	→ {self.configs['source']}")
            movie_msg = f"Movies 	→ {self.configs['movie']}"
            shows_msg = f"Shows 	→ {self.configs['show']}"
            books_msg = f"Books 	→ {self.configs['audiobook']}"
            print(f"{source_msg}\n{movie_msg}\n{shows_msg}\n{books_msg}")
        else:
            e = "Configs not loaded or invalid"
            logging.error(e)


class Auth:
    def __init__(self, auth_file=paths.auth_file()):
        self.auth_file = auth_file
        self.key = self.load()


    def load(self):
        if self.validate() == True:
            load_dotenv(self.auth_file)
            key = os.environ.get('tmdb_api_key')
            return key


    def validate(self):
        if self.auth_file.exists():
            while True:
                load_dotenv(self.auth_file)

                if 'tmdb_api_key' in os.environ:
                    key = os.environ.get('tmdb_api_key')
                    test_url = f"https://api.themoviedb.org/3/movie/550?api_key={key}"

                    print(style.dark("Validating TMDB API key..."), end='\r')
                    style.clear_line()
                    
                    response = requests.get(test_url)

                    if response.status_code == 200:
                        print(style.green("TMDB API check: OK!"))
                        return True

                    else:
                        status_message = response.json()['status_message']
                        logging.warning(status_message)
                        self.input()
                else:
                    self.input()
        else:
            self.create()


    def create(self):
        with open(self.auth_file, 'w+'):
            logging.warning("No key found!")
            self.input()
            self.validate()


    def input(self):
        load_dotenv(self.auth_file)
        os.environ['tmdb_api_key'] = input("Please input a valid TMDB API key: ")
        set_key(self.auth_file, 'tmdb_api_key', os.environ['tmdb_api_key'])


if __name__ == '__main__':
    pass