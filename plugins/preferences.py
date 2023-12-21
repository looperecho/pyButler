import os
import json
from pathlib import Path
from sys import platform

# Get OS and set a relevent app data dir
def get_app_dir():
	if platform == 'linux': # Linux
		app_dir = Path.home() / '.config' / 'pybutler'

	elif platform == 'darwin': # macOS
		app_dir = Path.home() / 'Library' / 'Application Support' / 'pybutler'

	elif platform == 'win32': # Windows
		app_dir = Path(os.getenv('APPDATA')) / 'pybutler'

	if os.path.exists(app_dir):
		return app_dir
	else:
		app_dir.mkdir(parents=True, exist_ok=True)
		return app_dir

# Create a path for config.json
def get_config(app_dir):
	config_path = app_dir / '.config.json'
	return config_path

# Create path for .env (This is where we will store the TMDB API Key)
def get_env(app_dir):
	env_path = app_dir / '.env'
	return env_path

# From user input, create the configs to send to write_config 
def create_config(config_path):
	source_dir = input("Source folder: ")
	movie_dir = input("Movie target folder: ")
	show_dir = input("TV Show target folder: ")
	audiobook_dir = input("Audiobook target folder: ")

	configs = {
		"source": source_dir,
		"movie": movie_dir,
		"show": show_dir,
		"audiobook": audiobook_dir
		}
	
	write_config(config_path, configs)
	return configs


def write_config(config_path, configs):
	with open(config_path, 'w+') as file:
		json.dump(configs, file, indent=2)


def read_config(config_path):
	with open(config_path, 'r') as file:
		configs = json.load(file)
	return configs


def verify_config(config_path):
	with open(config_path, 'r') as file:
		try:
			json.load(file)
			return True
		except json.JSONDecodeError:
			# !! + error log
			return False
		
def check_config():
	app_dir = get_app_dir()
	config_path = get_config(app_dir)

	if config_path.exists():
		return verify_config(config_path)
	else:
		# !! + error log
		return False

if __name__ == '__main__':
	pass