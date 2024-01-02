import json
import os
import re
from datetime import timedelta

import requests_cache
from preferences import logging


logger = logging.setup()

'''Process a Movie file'''
#   This can be called from another script with the args.
def process(file_path, api_key, movie_path):
    file_name = os.path.basename(file_path)
    ext = get_file_extension(file_name)
    
	# Search info with TMDB and return vars needed for renaming file.
    try:
        movie_name, movie_year = get_movie_info(file_name, api_key)
    except TypeError:
        logger.error("Movie information returned no results. Please check the title and year is correct.")
    else:
        new_file_name = rename_movie_file(movie_name, movie_year, ext)
        
        # move the file to new location
        new_path = os.path.join(movie_path, new_file_name)
        return new_path


def get_file_extension(file_name):
    splitext = os.path.splitext(file_name)
    file_extension = splitext[1]
    return file_extension


def format_movie_name(file_name):
	file_name = file_name.replace('(', '').replace(')', '')
	# Replace spaces with dots for consistent formatting, important later when using regex.
	file_name = file_name.replace(' ', '.')
	return file_name


def get_movie_name(file_name):
    file_name = format_movie_name(file_name)
    # get movie year
    year_match = re.findall(r'(19|20\d{2})', file_name)
    if year_match:
        movie_year = year_match[-1]
    else:
        logger.error("Unable to parse movie year from file name.")

    if movie_year:
        # Use the assigned movie_year in the regex pattern for movie_name
        movie_name_pattern = re.compile(rf'^(.*?)(?=\b{re.escape(movie_year)}\b)')
        movie_name_match = movie_name_pattern.search(file_name)

        if movie_name_match:
            # Replace the dots with spaces not
            movie_name = movie_name_match.group(1).replace(".", " ")
            return movie_name, movie_year
        else:
            logger.error("Unable to parse movie name from file name.")
    else:
        logger.error(f"Unable to continue for {file_name}.")


def get_movie_info(file_name, api_key):
    movie_name, movie_year = get_movie_name(file_name)

    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}&include_adult=false&year={movie_year}"

    # Cache and fetch results. Call from cache first.
    session = requests_cache.CachedSession(f"pybutler_movie_query", use_temp=True, expire_after=timedelta(days=30))
    search_results = json.loads(session.get(search_url).text)["results"]

    if len(search_results) > 0:
            # Return top result
            info = search_results[0]

            # Parse these results to get properly formatted movie info
            movie_name, movie_year = parse_movie_info(info)
            return movie_name, movie_year


def parse_movie_info(info):
    # Replace colon with dash
    movie_name = remove_colon(info["title"])
    # Remove further invalid chars
    invalid_chars = "\\/:*`‘’“”?!\"<>|"
    trans = str.maketrans("", "", invalid_chars)
    movie_name = movie_name.translate(trans)
    
    movie_year = info["release_date"].split("-")[0]
    return movie_name, movie_year


def remove_colon(source_info):
    source_info = source_info.replace(": ", " - ")
    return source_info


def rename_movie_file(movie_name, movie_year, ext):
    new_file_name = f"{movie_name} ({movie_year}){ext}"
    return new_file_name


if __name__ == '__main__':
    # Will add some input functions here to be ran seperately if desired.
    print("Please run 'butler.py'")