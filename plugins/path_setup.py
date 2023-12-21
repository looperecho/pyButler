import os
import logging

import plugins.preferences as config
import plugins.style as style


# Create data directory
def setup_data(app_data):
	try:
		os.mkdir(app_data)
	except FileExistsError:
		print(f"Data directory → {app_data}\n")
	else:
		print(f"Directory created → {app_data}\n")


def get_config_data(config_path):
	if config.check_config() == True:
		return config.read_config(config_path)
	else:
		print("No config found. Let's make a new one!")
		ask_auto(config_path)

# Create user set directories
def setup_dirs(configs):
	dir_names = ['source', 'movie', 'show', 'audiobook']
	
	for dir_name in dir_names:
		dir_path = configs[dir_name]
		try:
			os.mkdir(dir_path)
		except FileExistsError:
			exist_msg = f"Directory exists! {path}"
			print(f"{style.dark(exist_msg)}")
		else:
			print(f"Directory created: {path}")

# Setup directories via menu and ask to auto-create the directories or not
def ask_auto(config_path):
	while True:
		bold_y = f"{style.bold(style.blue('Y'))}" # Default
		ask = input(f"Would you like pyButler to create the directories you setup here? {bold_y}/n: ").lower()
		if ask in ['yes', 'y', '']:
			configs = config.create_config(config_path)
			print_configs(configs)
			setup_dirs(configs)
			return configs

		elif ask in ['no', 'n']:
			input("Please create the directories manually. Hit 'Enter' when done... ")
			configs = config.create_config(config_path)
			get_config_data(config_path)
			return configs

		else:
			print("Please provide a valid answer.")
			pass

# Check for missing directory paths if any
def check_dirs():
	dir_names = ['source', 'movie', 'show', 'audiobook']
	missing = []

	for dir_name in dir_names:
		dir_path = configs[dir_name]
		if not os.path.exists(dir_path):
			missing.append(dir_path)

	if missing:
		missing_ask(missing)
	
	else:
		print(style.green("Directory checks: OK!"))

# Ask user what to do when directories are missing
def missing_ask(missing, configs):
    nl = "\n" # newline
    while True:
        print(f"The following directories could not be found: {nl}{nl.join(missing)}")
        ask = input("Automatically re-create the directories? Y/n: ")
        if ask in ['yes', 'y']:
            setup_dirs(configs)
            break

        elif ask in ['no', 'n']:
            print(style.red("Please re-create the directories yourself"))
            wait = input(f"Press {style.bold('Enter')} when done...\n")
            check_dirs()
            break
        
        else:
            print("please provide valid answer")
            pass


def print_configs(configs):
    source_msg = style.bold(f"Source 	→ {configs['source']}")
    movie_msg = f"Movies 	→ {configs['movie']}"
    shows_msg = f"Shows 	→ {configs['show']}"
    books_msg = f"Books 	→ {configs['audiobook']}"
    print(f"{source_msg}\n{movie_msg}\n{shows_msg}\n{books_msg}")


app_dir = config.get_app_dir()

# set supplimentary data directory (for logs and env) & create it
app_data = os.path.join(app_dir, 'data')
setup_data(app_data)

# fetch env path
auth = config.get_env(app_dir)

# next, read & check the configs
config_path = config.get_config(app_dir)
get_config_data(config_path)


# set config path vars for easier syntax
source = configs['source']
movies = configs['movie']
shows = configs['show']
books = configs['audiobook']


if __name__ == '__main__':
	pass