import os
import json
import logging
import re
import shutil
from datetime import timedelta

import coloredlogs
import requests
from dotenv import load_dotenv, set_key

from plugins import style, movie, show, audiobook
from plugins import preferences_directories as path
from plugins import preferences_config as config


def welcome_message():
    print("WELCOME")

def setup_logging():
    coloredlogs.install(level="INFO", logger=logging.getLogger(), fmt="%(levelname)s: %(message)s")

    # console log setup
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # file logs setup
    file_handler = logging.FileHandler(os.path.join(path.app_dir, 'log_errors.log'))
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter("---\n%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)

    # call logger
    logging.getLogger().addHandler(file_handler)

    return logging


def create_api():
    # check if .env file exists
    if not os.path.exists(config.get_env_path()):
        with open(config.get_env_path(), "w"):
            logging.warning("TMDB API key not found...")
        input_api()

    else:
        print(style.dark("Checking TMDB API..."))
        check_api_file()


def input_api():
    load_dotenv(config.get_env_path())
    os.environ["TMDB_API_KEY"] = input("Input a valid TMDB API key: ")
    set_key(config.get_env_path(), "TMDB_API_KEY", os.environ["TMDB_API_KEY"])


def read_api():
    load_dotenv(config.get_env_path())
    api_key = os.environ.get("TMDB_API_KEY")
    return api_key


def check_api_file():
    load_dotenv(config.get_env_path())

    try:
        api_key = os.environ.get("TMDB_API_KEY")
        if api_key is None:
            raise ValueError ("TMDB API ket not found...")

    except ValueError as e:
        logging.warning(e)
        input_api()


def check_api_key():
    create_api()

    while True:
        api_key = read_api()
        api_test_url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"

        response = requests.get(api_test_url)

        if response.status_code == 200:
            print(style.green("TMDB API Check: OK!"))
            return api_key

        else:
            status_message = response.json()["status_message"]
            logging.warning(status_message)
            input_api()


def move_file(file_path, new_path):
    print("Moving File...", end="\r")
    style.clear_line()
    try:
        shutil.move(file_path, new_path)
        
    except (OSError, TypeError) as e:
        logging.error(e)
        
    else:
        check_file(new_path)


def check_file(new_path):
    if os.path.exists(new_path):
        msg = "File processed"
        success = style.green(style.bold("SUCCESS:"))
        location = os.path.dirname(new_path)
        filename = style.bold(os.path.basename(new_path))

        style.clear_line()
        print(f"{success} {msg} → {location} → {filename}")

# MAIN FUNCTION - Call from another script using the args
def process_file(file_path, api_key):
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_path)[1]
    pattern = re.search("(?i)(S(\d+))(E(\d+))", file_name, re.IGNORECASE)

    if extension != '.mkv' and extension != '.mp4' and extension !='.m4b':
        logging.info(f"{extension} is not a valid file type for pyButler to process. Skipping file...")
        pass

    elif extension == '.m4b':
        try:
            new_path = audiobook.process(file_path, path.books)
            move_file(file_path, new_path)
        except UnboundLocalError:
            logging.info("Skipping file...")
            pass
        
    elif pattern is not None:
        try:
            new_path = show.process(file_path, api_key)
            move_file(file_path, new_path)
        except UnboundLocalError:
            logging.info("Skipping file...")
            pass
        
    else:
        try:
            new_path = movie.process(file_path, api_key)
            move_file(file_path, new_path)
        except UnboundLocalError:
            logging.info("Skipping file...")
            pass


def main():
    logging = setup_logging()
    api_key = check_api_key()
    welcome_message()

    input(f"\nPress {style.bold('ENTER')} to start...")
    count = 0

    for file in os.listdir(path.source):
        file_path = os.path.join(path.source, file)
        extension = extension = os.path.splitext(file)[1]
        
        if extension == '.mkv' or extension == '.mp4' or extension =='.m4b':
            print (f"\nFile: {style.bold(style.dark_grey(file))}")
            process_file(file_path, api_key)
            count += 1
            
        else:
            pass

    if count < 1:
        logging.info("No valid files were found!")
    else:
        print(f"\n{style.blue('Complete.')}")


#   Solo Run.
if __name__ == "__main__":
    main()