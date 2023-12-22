import json
import logging
import os
import re
from datetime import timedelta

import requests_cache
from dotenv import load_dotenv, set_key

import plugins.path_setup as path
import plugins.style as style


'''Process a TV Show File'''
#   This can be called from another script with the args.
def process(file_path, api_key):
    file_name = os.path.basename(file_path)
    ext = get_file_extension(file_name)

    # Search info with TMDB and return vars needed for renaming file.
    try:
        show_name, show_year, season_num, episode_num, episode_title = get_show_info(file_name, api_key)
    except TypeError:
        style.clear_line()
        logging.error(f"Show information returned no results. Please check the title and year is correct.")
    else:
        # Create dirs and rename file
        season_dir = create_show_dirs(show_name, show_year, season_num)
        new_file_name = rename_show_file(show_name, season_num, episode_num, episode_title, ext)

        # move the file to new location
        new_path = os.path.join(season_dir, new_file_name)
        return new_path
    

def get_file_extension(file_name):
    splitext = os.path.splitext(file_name)
    file_extension = splitext[1]
    return file_extension


def check_for_year(file_name):
    show_name = ""
    
    show_search = re.search("(.*)((\(|\.)([0-9]{4})(\)|\.))", file_name)
    # (^.*)(?=S\d+) <--- old reg-ex pattern
    
    if show_search is not None:
        show_name = (show_search.group(1)).strip()
        show_year = (show_search.group(4))
        print(show_year, show_name)
    else:
        show_name = get_show_name(file_name)
        show_year = ""

    return show_name, show_year


def get_show_name(file_name):
    # Check if year is present in show name as (YYYY)
    show_name_search = re.search("(?i)(^.*)(?=S\d+)", file_name)

    if show_name_search is not None:
        show_name = (show_name_search.group(1)).strip()

    else:
        style.clear_line()
        logging.error("Unable to parse show title from file name.")
    
    # Check for dots and replace
    re_dots = re.search("\.", show_name)
    if re_dots is not None:
        show_name = show_name.replace(".", " ")
        show_name = show_name.strip()

    # Cleanup - removes any extra dashes that seem to be included in previous replace)
    re_dash = re.search("-", show_name)
    if re_dash is not None:
        show_name = show_name.replace("-", "")
        show_name = show_name.strip()

    return show_name


def get_season_num(file_name):
    season_search = re.search("(?i)(S(\d+))(E(\d+))", file_name, re.IGNORECASE)
    season_num = season_search.group(2)
    return season_num


def get_episode_num(file_name):
    episode_search = re.search("(?i)(S(\d+))(E(\d+))", file_name, re.IGNORECASE)
    episode_num = episode_search.group(4)
    return episode_num


def remove_colon(source_info):
    source_info = source_info.replace(": ", " - ")
    return source_info


#   This function calls the others to get_show_name, season_num, episode_num, episode_title 
#   and returns them all to process_file. Most of the flow of information happens here.
def get_show_info(file_name, api_key):
    
    show_name, show_year = check_for_year(file_name)

    # Use more accurate url if show year is present
    if show_year:
        search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={show_name}&include_adult=false&first_air_date_year={show_year}"
    
    else:
        search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={show_name}&include_adult=false"

    # Cache and fetch results. Call from cache first.
    session = requests_cache.CachedSession(f"pydown_show_query", use_temp=True, expire_after=timedelta(days=30))
    search_results = json.loads(session.get(search_url).text)["results"]

    if len(search_results) > 0:
            # Return top result
            info = search_results[0]

            # parse these results to get proper show info
            show_id, show_name, show_year = parse_show_info(info)

            # Get season and episode num
            season_num = get_season_num(file_name)
            episode_num = get_episode_num(file_name)

            # get episode title
            episode_title = get_episode_title(show_id, season_num, episode_num, api_key)

            return show_name, show_year, season_num, episode_num, episode_title


def parse_show_info(info):
    show_id = info["id"]
    show_name = remove_colon(info["name"])
    show_year = info["first_air_date"].split("-")[0]

    return show_id, show_name, show_year


def get_episode_title(show_id, season_num, episode_num, api_key):
    # get episode title
    episode_url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_num}/episode/{episode_num}?api_key={api_key}&language=en-US"

    # Cache and fetch results. Call from cache first.
    session = requests_cache.CachedSession("pydown_episode_query", use_temp=True, expire_after=timedelta(days=30))
    episode_info = json.loads(session.get(episode_url).text)

    # Episode Check
    if episode_info.get("success") == False:
        logging.error("Show results were found but season or epiosde numbers may be wrong.")
        episode_title = ""

    else:
        # Get episode title from result
        episode_title = episode_info["name"]

        # Remove invalid chars
        invalid_chars = "\\/:*`‘’“”?!\"<>|"
        trans = str.maketrans("", "", invalid_chars)
        episode_title = episode_title.translate(trans)
    
    return episode_title


#   Create the show directories. 
#   We do not need to return the show_dir itself as it's part of the season_dir path
def create_show_dirs(show_name, show_year, season_num):
    show_dir_name = f"{show_name} ({show_year})"
    show_dir = os.path.join(path.shows, show_dir_name)

    season_dir_name = f"Season {season_num}"
    season_dir = os.path.join(show_dir, season_dir_name)

    if not os.path.exists(season_dir):
        os.makedirs(season_dir, exist_ok=True)

    return season_dir


def rename_show_file(show_name, season_num, episode_num, episode_title, ext):
    new_file_name = f"{show_name} - S{season_num}E{episode_num} - {episode_title}{ext}"

    return new_file_name


if __name__ == '__main__':
    print("Please run 'butler.py'")