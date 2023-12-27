# pyButler
pyButler is a Python command line application designed for the automatic organization of your TV show and movie files. It leverages The Movie Database (TMDB) API to gather information about movies and TV shows, facilitating the renaming and moving of media files to a structured directory.  


## Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Application Data & Files](#application-data--configuration-files)
5. [File Processing](#file-processing)
6. [Plugins](#plugins)
7. [Support & Notes](#support)
8. [To Do](#to-do-plans)


## Features
* Automatic organization of TV show, movie and audiobook files.
* Utilizes TMDB API for fetching movie and TV show information.
* Supports processing of various file types, including MKV, MP4, and M4B.


## Installation
> ⚠️ You **will** need a TMDB API key. You can obtain one from the [TMDB website](https://developer.themoviedb.org/docs/getting-started).
1. Clone the repo:
```bash
git clone https://github.com/looperecho/pyButler.git
```
2. Create a virtual environment and activate it (optional)
```bash
$ python -m venv /path/to/virtual/environment
$ source /path/to/virtual/environment/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the python file:
```bash
$ cd /path/to/pyButler  
$ python pybutler.py
```
2. Follow the on-screen prompts to input your TMDB API key and setup your directory preferences.
3. pyButler will scan the source directory for supported file types, and do the rest!  
> Supported filetypes: `.mkv` `.mp4` `.m4b`


## Application Data & Configuration Files
pyButler will create an application directory along with `config.json` and `.env` files to store your configurations. If you want to edit them at any time, they can be found at:
* Linux
```
/home/user/.config/pyButler
```
* macOS
```
/Users/user/Library/Application Support/pyButler
```
* Windows
```
C:\Users\user\AppData\Roaming\pyButler
```


## File Processing
pyButler processes files based on their extensions. After the intial setup and on subsequent runs, pyButler will scan your source directory for the supported file types. Currently supported file types are .mkv, .mp4, and .m4b.
The script automatically renames these files using information obtained from the TMDB API. As long as your source files have some information in them, such as movie name, year, tv show season number and episode number, it should be able to determine the correct media.  
Examples of file names could be:

```
Source_Directory
    ├── cool.tv.show.s01e01.mkv
    ├── cool tv show s02e01.mkv
    ├── some movie title 2017.mkv
    ├── movie.title.sequel.2018.mkv
    └── Amazing Audiobook (Unabridged).m4b
```


## Plugins
I've seperated each processing category into seperate modules that can be easily modified or allows for integration of futher media types in the future.
pyButler will automatically determin which plugin to call for futher processing.

* **Movie Plugin**  
The movie plugin is responsible for processing movie files. It uses some regex logic to detirmine the release year and title and fetches futher information about the movie from TMDB and renames the file in the following format:
```
Movie_Directory
    ├── Some Movie Title (2017).ext
    └── Movie Title Sqeuel (2018).ext
```

* **Show Plugin**  
Arguably the most useful plugin here. The Show plugin is responsible for naming episodes from TV Shows. It uses regex to determine the show name, year, and episode and season numbers to fetch all information from TMDB (including episode title). It then uses this information to rename the file, and create a directory structure to follow the format of popular media server management platforms (such as Plex or Jellyfin)
The file and directory output is:  
```
Show_Directory
    └── Cool TV Show
        ├── Season 01
        │   └── Cool TV Show - S01E01 - Episode Title.ext
        └── Season 02
            └── Cool TV Show - S02E01 - Episode Title.ext
```

* **Audiobook Plugin**  
This one is pretty basic, as it doesn't leverage any 3rd party databases, but relies on ID3 tags being present in the file already, (due to the fact that I couldnt not find any realiable databses to leverage). It is designed for single-file audiobooks, not those that have a seperate file for each chapter.
It will remove the term `(Unabridged)` if present, then create a directory based on the authors name, and rename the file as follows:
```
Audiobook_Directory
    └── Author
        └── Amazing Audiobook.m4b
```


## Support
I can offer limited support, but this script isn't very complex anyway. However if you do find any bugs etc. Please create an issue on the GitHub repository.


## Notes
Initially I wrote this for myself to run on a headless server, with a goal to improving my python knowledge whilst making something usefull at the same time. I know a lot of other similar applications exist out there, but feel free to use it and drop any suggestions for improvements if you feel like it. I had a lot of fun making this, and learned a lot of new things along the way. Thanks for reading!


### To Do Plans
* `audiobook.py`
	- [ ] Add authors name to the file
	- [ ] Futher add subdirectories for series (and add those to the filename)
* `movie.py`  
	- [ ] Add options for organisation preferences 
	- [ ] Organise by genre or simply giving the movie file it's own sub-directory
	- [ ] Add resolution to the end of the filename
* Package the script for better distro and real CLI arguments (or maybe a TUI?)
    - [ ] Add a toggle option to automatically create user set directories, if they do not exist
    - [ ] Add the ability to edit particular directories that have been set, rather than having going through to set them all at once  
    