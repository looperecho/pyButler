import os
import re
import shutil
import sys

from preferences import logging, config, style
from plugins import audiobook, movie, show


def welcome_message():
    logo_art = style.logo()
    version = "1.0"
    hr = style.hr()
    tagline = style.blue("Automatic organisation for your media files.")
    card = f"{logo_art}\nv{version}\n{tagline}{hr}"
    print(card)


def warn():
    logger.warning("pyButler will move & rename files. It's advisable to have a backup.")
    supported = f"Supported: {style.bold('.mkv .mp4 .m4b')}"
    print(supported)


def move_file(file_path, new_path, logger):
    print("Moving File...", end="\r")
    style.clear_line()
    try:
        shutil.move(file_path, new_path)

    except OSError as e:
        logger.error(e)
    except TypeError:
        logger.info("File not processed. Skipping File..")

    else:
        check_file(new_path)

# Make sure the new_file made it to the destination folder after `move_file()`
def check_file(new_path):
    if os.path.exists(new_path):
        msg = "File processed"
        success = style.green("    ✔")
        location = os.path.dirname(new_path)
        filename = style.bold(os.path.basename(new_path))

        style.clear_line()
        print(f"{success} {msg} | {location} > {filename}")

# MAIN FUNCTION - Call from another script using the args
def process_file(file_path, api_key, configs, logger):
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_path)[1]
    pattern = re.search(r"(?i)(S(\d+))(E(\d+))", file_name, re.IGNORECASE)

    if extension not in ('.mkv', '.mp4', '.m4b'):
        logger.info("%s is not a valid file type. Skipping file...", extension)

    # m4b must be an audiobook file
    elif extension == '.m4b':
        try:
            new_path = audiobook.process(file_path, book_path=configs['audiobook'])
            move_file(file_path, new_path, logger)
        except UnboundLocalError:
            logger.info("Skipping file...")

    # Figure out if the video file is a TV show or not
    elif pattern is not None:
        try:
            new_path = show.process(file_path, api_key, show_path=configs['show'])
            move_file(file_path, new_path, logger)
        except UnboundLocalError:
            logger.info("Skipping file...")

    # Conclude at this point, the file must be a movie
    else:
        try:
            new_path = movie.process(file_path, api_key, movie_path=configs['movie'])
            move_file(file_path, new_path, logger)
        except UnboundLocalError:
            logger.info("Skipping file...")


def main():
    try:
        # Warning message
        warn()

        # Setup TMDB API Key
        api = config.Auth()

        # Setup config / paths to directories
        prefs = config.Config()

        # Read the directories from config file
        configs = prefs.read()

        # Display logo card
        welcome_message()
        prefs.display()

        enter = style.bold("ENTER")
        input(f"\nPress {enter} to start...")
        count = 0

        for file in os.listdir(configs['source']):
            file_path = os.path.join(configs['source'], file)
            extension = extension = os.path.splitext(file)[1]

            # Quick and dirty check for supported file types
            if extension in ('.mkv', '.mp4', '.m4b'):
                print (f"\nFile: {style.bold(style.dark_grey(file))}")
                process_file(file_path, api.key, configs, logger)
                count += 1

            else:
                pass

        if count < 1:
            logger.info("No valid files were found!")

        else:
            print(f"\n{style.blue('Complete.')}")

    # Ctrl + C handling
    except KeyboardInterrupt:
        print('')
        logger.info("pyButler interrupted by user. Exiting app..")
        sys.exit(0)

#   Solo Run.
if __name__ == "__main__":
    # Setup logging on the outside
    logger = logging.setup()

    # Run
    main()
