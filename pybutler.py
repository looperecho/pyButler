import os
import logging
import re
import shutil

import coloredlogs
import requests
from dotenv import load_dotenv, set_key

from preferences import paths, config, style
from plugins.movie import movie
from plugins.show import show
from plugins.audiobook import audiobook


def welcome_message():
    logo_art = style.logo()
    version = "1.0"
    hr = style.hr()
    tagline = style.blue("Automatic organisation for your media files.")
    card = f"{logo_art}\nv{version}\n{tagline}{hr}"
    print(card)


def setup_logging():
    coloredlogs.install(level="INFO", logger=logging.getLogger(__name__), fmt="%(levelname)s: %(message)s")

    # console log setup
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # file logs setup
    file_handler = logging.FileHandler(os.path.join(paths.app(), 'log_errors.log'))
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter("---\n%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)

    # call logger
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)

    return logger


def move_file(file_path, new_path):
    print("Moving File...", end="\r")
    style.clear_line()
    try:
        shutil.move(file_path, new_path)
        
    except (OSError, TypeError) as e:
        logger.error(e)
        
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
def process_file(file_path, api_key, configs):
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_path)[1]
    pattern = re.search("(?i)(S(\d+))(E(\d+))", file_name, re.IGNORECASE)

    if extension != '.mkv' and extension != '.mp4' and extension !='.m4b':
        logger.info(f"{extension} is not a valid file type for pyButler to process. Skipping file...")
        pass

    elif extension == '.m4b':
        try:
            new_path = audiobook.process(file_path, book_path=configs['audiobook'])
            move_file(file_path, new_path)
        except UnboundLocalError:
            logger.info("Skipping file...")
            pass
        
    elif pattern is not None:
        try:
            new_path = show.process(file_path, api_key, show_path=configs['show'])
            move_file(file_path, new_path)
        except UnboundLocalError:
            logger.info("Skipping file...")
            pass
        
    else:
        try:
            new_path = movie.process(file_path, api_key, movie_path=configs['movie'])
            move_file(file_path, new_path)
        except UnboundLocalError:
            logger.info("Skipping file...")
            pass


def main():
    # Setup Logging
    logger = setup_logging()

    # Setup TMDB API Key
    api = config.Auth()

    # Setup config / paths to directories
    prefs = config.Config()

    # Read the directories
    configs = prefs.read()
    
    welcome_message()
    prefs.display()

    input(f"\nPress {style.bold('ENTER')} to start...")
    count = 0

    for file in os.listdir(configs['source']):
        file_path = os.path.join(configs['source'], file)
        extension = extension = os.path.splitext(file)[1]
        
        if extension == '.mkv' or extension == '.mp4' or extension =='.m4b':
            print (f"\nFile: {style.bold(style.dark_grey(file))}")
            process_file(file_path, api.key, configs)
            count += 1
            
        else:
            pass

    if count < 1:
        logger.info("No valid files were found!")
    else:
        print(f"\n{style.blue('Complete.')}")


#   Solo Run.
if __name__ == "__main__":
    main()